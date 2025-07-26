# A little different from the cfond-asp solution, here the resulting policy
# of each domain is a union of multiple runs with different initial states
# and the result is in the policy.out file so we need just the variable parsing
# from the output.sas.
import json
import pickle
import os
import numpy as np
import random

class Rule:
    def __init__(self, action = None, x = None, y = None, vx = None, 
                 vy = None, t = None, vt = None):
        self.action = action
        if x != None:
            self.x = str(x)
        else:
            self.x = x
        if y != None:
            self.y = str(y)
        else:
            self.y = y
        if vx != None:
            self.vx = str(vx)
        else:
            self.vx = vx
        if vy != None:
            self.vy = str(vy)
        else:
            self.vy = vy
        if t != None:
            self.t = str(t)
        else:
            self.t = t
        if vt != None:
            self.vt = str(vt)
        else:
            self.vt = vt

    def __str__(self):
        return "State: x={0}, y={1}, t={2}, vx={3}, vy={4}, vt={5}; Action: {6}".format(
            self.x, self.y, self.t, self.vx, self.vy, self.vt, self.action)

    # the self rule will be always the actual rule, while oher the value from observation
    def __eq__(self, other):
        if isinstance(other, Rule):
            if self.x != None and other.x != None:
                if self.x.startswith('not'):
                    if self.x[4:] == other.x:
                        return False
                elif self.x != other.x:
                    return False
            if self.y != None and other.y != None:
                if self.y.startswith('not'):
                    if self.y[4:] == other.y:
                        return False
                elif self.y != other.y:
                    return False
            if self.t != None and other.t != None:
                if self.t.startswith('not'):
                    if self.t[4:] == other.t:
                        return False
                elif self.t != other.t:
                    return False
            if self.vx != None and other.vx != None:
                if self.vx.startswith('not'):
                    if self.vx[4:] == other.vx:
                        return False
                elif self.vx != other.vx:
                    return False
            if self.vy != None and other.vy != None:
                if self.vy.startswith('not'):
                    if self.vy[4:] == other.vy:
                        return False
                elif self.vy != other.vy:
                    return False
            if self.vt != None and other.vt != None:
                if self.vt.startswith('not'):
                    if self.vt[4:] == other.vt:
                        return False
                elif self.vt != other.vt:
                    return False
        return True

    def set_value(self, value: str):
        index = value.find('(')
        specs = value[index+1:-1].split('_')
        if specs[0] == 'x':
            if value.startswith('Atom'):
                self.x = specs[1]
            else:
                self.x = f'not {specs[1]}'
        if specs[0] == 'y':
            if value.startswith('Atom'):
                self.y = specs[1]
            else:
                self.y = f'not {specs[1]}'
        if specs[0] == 't':
            if value.startswith('Atom'):
                self.t = specs[1]
            else:
                self.t = f'not {specs[1]}'
        if specs[0] == 'vx':
            if value.startswith('Atom'):
                self.vx = specs[1]
            else:
                self.vx = f'not {specs[1]}'
        if specs[0] == 'vy':
            if value.startswith('Atom'):
                self.vy = specs[1]
            else:
                self.vy = f'not {specs[1]}'
        if specs[0] == 'vt':
            if value.startswith('Atom'):
                self.vt = specs[1]
            else:
                self.vt = f'not {specs[1]}'

# path should be just the folder, then go to path/output.sas
def get_variables(path):
    with open(f'{path}/output.sas', 'r') as f:
        lines = f.readlines()
    start_indices = [i for i, x in enumerate(lines) if x.strip().startswith('begin_variable')]
    end_indices = [i for i, x in enumerate(lines) if x.strip().startswith('end_variable')]
    indices = list(zip(start_indices, end_indices))
    variables = {}
    for start, end in indices:
        values = []
        for line in lines[start+1:end]:
            if line.startswith('var'):
                name = str(line)[:-1]
            if line.startswith('Atom') or line.startswith('NegatedAtom'):
             values.append(str(line)[:-1])
        variables[name] = values
    return variables

# path should be just the folder, then go to path/policy.out
def parse_policy(path, variables, custom = False):
    if custom:
        full_path = f'{path}/policy.out'
        pkl_path = f'{path}/custom_policy.pkl'
        json_path = f'{path}/custom_policy.json'
    else:
        full_path = f'{path}/policy.txt'
        pkl_path = f'{path}/policy.pkl'
        json_path = f'{path}/policy.json'
    with open(full_path, 'r') as f:
        lines = f.readlines()
    rules = []
    for i in range(len(lines)):
        if lines[i].startswith('If'):
            rule = Rule()
            for couple in lines[i].split(' ')[2:]:
                variable = couple.split(':')
                atom = variables[variable[0]][int(variable[1])]
                rule.set_value(atom)
            action = lines[i+1].split(' ')[1]
            rule.action = action
            if rule not in rules:
                rules.append(rule)

    with open(pkl_path, 'wb') as f:
        pickle.dump(rules, f)
    with open(json_path, 'w') as f:
        json.dump(rules, f, default=lambda o: o.__dict__, indent=4)
    print('Policy parsed and saved..')
    return rules

def get_policy(path, custom = False):
    if not custom:
        full_path = f'{path}/policy.pkl'
    else:
        full_path = f'{path}/custom_policy.pkl'
    if os.path.exists(full_path) and custom == False:
        with open(full_path, 'rb') as f:
            rules = pickle.load(f)
    else:
        variables = get_variables(path)
        rules = parse_policy(path, variables, custom)

    return rules

def discretize_simplified(obs):
    # x = [-3, -2, -1, 0, 1, 2, 3]
    # y = [-1, 0, 1, 2, 3]
    # t = [-2, -1, 0, 1, 2]
    # vx = [-2, -1, 0, 1, 2]
    # vy = [-2, -1, 0, 1]
    # vt = [-2, -1, 0, 1, 2]
    values = obs[:6]
    for i,v in enumerate(values):
        # if vx, vy, t or vt
        if i in [2, 3, 4, 5]:
            if v < -0.7:
                values[i] = -2
            elif v < -0.15:
                values[i] = -1
            elif v < 0.15:
                values[i] = 0
            elif i == 3:
                values[i] = 1
            elif v < 0.7:
                values[i] = 1
            else:
                values[i] = 2
        # if x
        elif i == 0:
            if v < -0.7:
                values[i] = -3
            elif v < -0.4:
                values[i] = -2
            elif v < -0.15:
                values[i] = -1
            elif v < 0.15:
                values[i] = 0
            elif v < 0.4:
                values[i] = 1
            elif v < 0.7:
                values[i] = 2
            else:
                values[i] = 3
        # if y
        else:
            if v < -0.15:
                values[i] = -1
            elif v < 0.15:
                values[i] = 0
            elif v < 0.6:
                values[i] = 1
            elif v < 1.1:
                values[i] = 2
            else:
                values[i] = 3
                
    return Rule(x=int(values[0]), y=int(values[1]), vx=int(values[2]), vy=int(values[3]), t=int(values[4]), vt=int(values[5]))

def discretize_mini(obs):
    # x = [-1, 0, 1]
    # y = [0, 1, 2]
    # t = [-1, 0, 1]
    # vx = [-1, 0, 1]
    # vy = [-2, -1, 0, 1]
    # vt = [-1, 0, 1]
    values = obs[:6]
    # x value
    if values[0] > 0.4:
        values[0] = 1
    elif values[0] < -0.4:
        values[0] = -1
    else:
        values[0] = 0
    # y value
    if values[1] > 1.1:
        values[1] = 2
    elif values[1] < 0.6:
        values[1] = 0
    else:
        values[1] = 1
    # other values
    for i,v in enumerate(values):
        if i in [2, 4, 5]:
            if v > 0.15:
                values[i] = 1
            elif v < -0.15:
                values[i] = -1
            else:
                values[i] = 0
        elif i == 3:
            if v > 0.1:
                values[i] = 1
            elif v > -0.15:
                values[i] = 0
            elif v > -0.7:
                values[i] = -1
            else:
                values[i] = -2
    return Rule(x=int(values[0]), y=int(values[1]), vx=int(values[2]), vy=int(values[3]), t=int(values[4]), vt=int(values[5]))

def discretize_novelocity(obs):
    # x = {-10, 10}
    # y = {-1, 10}
    # t = {-4, 4}
    values = [obs[0], obs[1], obs[4]]
    # t
    if values[2] < -1.2:
        values[2] = -4
    elif values[2] < -0.8:
        values[2] = -3
    elif values[2] < -0.4:
        values[2] = -2
    elif values[2] < -0.10:
        values[2] = -1
    elif values[2] < 0.10:
        values[2] = 0
    elif values[2] < 0.4:
        values[2] = 1
    elif values[2] < 0.8:
        values[2] = 2
    elif values[2] < 1.2:
        values[2] = 3
    else:
        values[2] = 4
    # x and y
    for i in [0,1]:
        if i == 1 and values[i] < 0.05:
            if values[i] < -0.05:
                values[i] = -1
            else:
                values[i] = 0
        elif i == 0 and abs(values[i]) < 0.1:
            values[i] = 0
        elif values[i] > 0:
            values[i] = np.ceil(6.66*values[i])
        else:
            values[i] = np.floor(6.66*values[i])
        if values[i] > 10:
            values[i] = 10
        if values[i] < -10:
            values[i] = -10
    return Rule(x=int(values[0]), y=int(values[1]), t=int(values[2]))

def get_action(observation, model, policy):
    print(f'Observation: {observation[:6]}')
    if model == 'mini':
        state = discretize_mini(observation)
    elif model == 'simplified':
        state = discretize_simplified(observation)
    else:
        state = discretize_novelocity(observation)
    print(f'State discretized = {state}')
    for rule in policy:
        if rule == state:
            print(f'Rule found, action {rule.action} selected..')
            return rule.action
    relaxed_state = Rule(x=state.x, y=state.y, t=state.t)
    rules = []
    for rule in policy:
        if rule == relaxed_state:
            rules.append(rule)
    if len(rules) > 0:
        action = random.choice(rules).action
        print(f'Rule found for the relaxed state, action {rule.action} selected..')
        return rule.action
    print('No rule found for this state.. returning idle action')
    return 'idle'
