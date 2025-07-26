import gymnasium as gym

ACTION_DICT = {
    'idle' : 0,
    'go left' : 1,
    'go up' : 2,
    'go right' : 3
}

class LulaGame:

    def __init__(self):
        self.labels = ['go up', 'idle', 'go left', 'go right', 'quit']
        self.env = None
        self.state = 'none' # can be: 'none', 'starting', 'running', 'quitting'
        self.running = False
        self.observations = []
        self.goal_state = [0, 0, 1, 1, 0, 0.5]
        self.value_names = ['x-coordinate', 'y-coordinate', 'horizontal velocity', 'vertical velocity', 'theta angle', 'angular velocity']

    def reset(self):
        self.state = 'none'
        self.running = False
        if self.env is not None:
            self.env.close()
            self.env = None

    def start(self, model):
        self.model = model
        print(f'Starting the Game task..')
        self.env = gym.make('LunarLander-v2', render_mode='human')
        self.env.reset()
        response_type = 'text'
        response = 'ready'
        self.state = 'starting'
        return response_type, response
    
    def process_input(self, input):
        if self.state == 'quitting':
            label = self.model(input, candidate_labels=['yes', 'no'])['labels'][0]
            print(f'label predicted: {label}')
            if label == 'yes':
                self.reset()
                response_type = 'reset'
                response = 'reset'
                self.state = 'none'
                self.running = False
            else:
                response_type = 'text'
                response = 'continue'
                self.state = 'running'
            return response_type, response
        
        elif self.state == 'starting':
            label = self.model(input, candidate_labels=['yes', 'no'])['labels'][0]
            print(f'label predicted: {label}')
            if label == 'yes':
                self.state = 'running'
                response_type, response = self.play_action(describe=False)
                response_type = 'text'
                response = 'start_game'
                self.running = True
                return response_type, response
            else:
                response_type = 'reset'
                response = 'reset'
                self.reset()
            return response_type, response
        else:
            label = self.model(input, candidate_labels=self.labels)['labels'][0]
            print(f'label predicted: {label}')
            if label == 'quit':
                #self.quitting = True
                response_type = 'text'
                response = 'confirm'
                self.state = 'quitting'
                return response_type, response
            else:
                # Call method for using inferred action on the Lunar Lander
                return self.play_action(label)
        
    def describe_state(self, observation):
        descr = f'My current position is {round(float(observation[0]), 3)} as X and {round(float(observation[1]), 3)} as Y. ' + \
                f'My angle with respect to ground is {round(float(observation[4]), 3)}, velocities are {round(float(observation[2]), 3)}, ' + \
                f'{round(float(observation[3]), 3)} and {round(float(observation[5]), 3)}.'
        check = 0
        if abs(self.goal_state[0] - observation[0]) > 0.35:
            descr += f', the {self.value_names[0]}'
            check += 1
        if abs(self.goal_state[4] - observation[4]) > 0.5:
            descr += f', the {self.value_names[4]}'
            check += 1
        if check == 2:
            descr += f' are'
        elif check == 1:
            descr += f' is'
        if check > 0:
            descr += ' not aligned with the goal, you should solve that as soon as possible. '
        check = 0
        if abs(observation[2]) > 0.6 or abs(observation[3]) > 0.6 or abs(observation[5]) > 0.6:
            descr += f' But first watch out'
            if abs(observation[2]) > 0.6:
                check += 1
                descr += f' the {self.value_names[2]},'
            if abs(observation[3]) > 0.6:
                check += 1
                if check > 1:
                    descr += ','
                descr += f' the {self.value_names[3]},'
            if abs(observation[5]) > 0.6: 
                check += 1
                if check > 1:
                    descr += ','
                descr += f' the {self.value_names[5]},'
            descr += ' because you could reach critically high values impossible to correct in time.'
        return descr

    def play_action(self, input = None, describe = True):
        if input is not None:
            action = ACTION_DICT[input]
            # to make more than 1 action at a time start a loop diong the same action, maybe 3-5 times
            for i in range(3):
                observation, reward, terminated, truncated, info = self.env.step(action)
                #self.env.render()
                self.observations.append(observation[:6])

            if terminated and reward == 100:
                self.state = 'starting'
                response_type = 'text'
                response = 'win'
                return response_type, response
            
            if terminated:
                self.state = 'starting'
                response_type = 'text'
                response = 'lose'
                self.state = 'starting'
                self.reset()
                return response_type, response
        
        if describe:
            response_type = 'direct'
            response = self.describe_state(observation)
        else:
            response_type = 'text'
            response = 'move'
        return response_type, response