import gymnasium as gym
from lunar_lander import policy_parser as policy
import subprocess
from lula_game import LulaGame
from lunar_lander.lander import Lander

LUNAR_LANDER_PATH = 'lunar_lander/'

ACTION_DICT = {
    'idle' : 0,
    'left_engine' : 1,
    'main_engine' : 2,
    'right_engine' : 3
}

CUSTOM_DICT = {
    'novelocity' : {
        'low' : '2',
        'high' : '10',
        'middle' : '6',
        'left' : '-8',
        'right' : '8',
        'center' : '0'},
    'mini' : {
        'low' : '0',
        'high' : '2',
        'middle' : '1',
        'left' : '-1',
        'right' : '1',
        'center' : '0'
    },
    'simplified' : {
        'low' : '1',
        'high' : '3',
        'middle' : '2',
        'left' : '-2',
        'right' : '2',
        'center' : '0'
    }    
}

class LulaSim:
    
    def __init__(self):
        self.domain = None
        self.problem = None
        self.policy = None
        self.env = None
        self.state = 'none' # none model goal custom planning questions quitting
        self.restore = 'none' # same as above
        self.custom = 'none' # none init goal game story
        self.pddl_values = [None, None, None, None] # 4 values for [init_x, init_y, goal_x, goal_y]
        self.last_sentence = None
        self.observations = []
        self.actions = []
        self.rewards = []
        self.process = None
        self.game = None
        self.line = 0

    def reset(self):
        #self.env.close()
        self.domain = None
        self.problem = None
        self.policy = None
        self.env.close()
        self.env = None
        self.state = 'none'
        self.restore = 'none' 
        self.custom = 'none'
        self.pddl_values = [None, None, None, None]
        self.last_sentence = None
        self.observations = []
        self.actions = []
        self.rewards = []
        self.process = None
        self.game = None
        self.line = 0

    def start(self, model, sentences):
        self.model = model
        self.sentences = sentences
        print(f'Starting the Simulator task..')
        #self.env = gym.make('LunarLander-v2', render_mode='human')
        #self.env.reset()
        response_type = 'text'
        response = 'start_simulator'
        self.state = 'model'
        return response_type, response
    
    def process_quit(self, input):
        label = self.model(input, candidate_labels=['yes', 'no'])['labels'][0]
        print(f'label predicted: {label}')
        if label == 'yes':
            self.reset()
            response_type = 'reset'
            response = 'reset'
            self.state = 'none'
        else:
            response_type = 'text'
            response = self.last_sentence
            self.state = self.restore
        return response_type, response
    
    def process_model(self, input):
        label = self.model(input, candidate_labels=['quit', 'info', 'novelocity', 'mini', 'simplified'])['labels'][0]
        print(f'label predicted: {label}')
        if label == 'quit':
            response_type = 'text'
            response = 'confirm'
            self.restore = self.state
            self.state = 'quitting'
        elif label == 'info':
            response_type = 'text'
            response = 'models'
        elif label == 'novelocity' or label == 'mini' or label == 'simplified':
            self.domain = label
            response_type = 'direct'
            response = f'{self.domain} selected, now please tell me if you want the defaul or custom goal. {self.sentences["goals"]}'
            self.state = 'goal'
        if response != 'confirm':     
            self.last_sentence = response
        return response_type, response
    
    def process_goal(self, input):
        label = self.model(input, candidate_labels=['quit', 'info', 'default', 'custom'])['labels'][0]
        print(f'label predicted: {label}')
        if label == 'quit':
            response = 'confirm'
            self.restore = self.state
            self.state = 'quitting'
        elif label == 'info':
            response = 'goals_info'
        elif label == 'default':
            self.policy = policy.get_policy(f'{LUNAR_LANDER_PATH}{self.domain}')
            self.play_simulator()
            response = 'plan_ready'
            self.state = 'questions'
        elif label == 'custom':
            response = 'define_prob'
            self.custom = 'init'
            self.state = 'custom'
        if response != 'confirm':     
            self.last_sentence = response 
        response_type = 'text'   
        return response_type, response
    
    def process_custom(self, input):
        if self.custom == 'init' and self.last_sentence == 'define_prob':
            label = self.model(input, candidate_labels=['quit', 'default', 'custom'])['labels'][0]
            print(f'label predicted: {label}')
            if label == 'quit':
                response = 'confirm'
                self.restore = self.state
                self.state = 'quitting'
            if label == 'default':
                self.custom = 'goal'
                response = 'ask_goal_x'
                self.pddl_values[0] = 'center'
                self.pddl_values[1] = 'high'
            elif label == 'custom':
                response = 'ask_init_x'
        elif self.custom == 'init' and self.last_sentence.startswith('ask_init'):
            if self.last_sentence[-1] == 'x':
                label = self.model(input, candidate_labels=['quit', 'left', 'right', 'center'])['labels'][0]
                print(f'label predicted: {label}')
            else:
                label = self.model(input, candidate_labels=['quit', 'low', 'high', 'middle'])['labels'][0]
                print(f'label predicted: {label}')
            if label == 'quit':
                response = 'confirm'
                self.restore = self.state
                self.state = 'quitting'
            else:
                if self.last_sentence[-1] == 'x':
                    self.pddl_values[0] = label
                    response = 'ask_init_y'
                else:
                    self.pddl_values[1] = label
                    self.custom = 'goal'
                    response = 'ask_goal_x'
        elif self.custom == 'goal':
            if self.last_sentence[-1] == 'x':
                label = self.model(input, candidate_labels=['quit', 'left', 'right', 'center'])['labels'][0]
                print(f'label predicted: {label}')
            else:
                label = self.model(input, candidate_labels=['quit', 'low', 'high', 'center'])['labels'][0]
                print(f'label predicted: {label}')
            if label == 'quit':
                response = 'confirm'
                self.restore = self.state
                self.state = 'quitting'
            else:
                if self.last_sentence[-1] == 'x':
                    self.pddl_values[2] = label
                    response = 'ask_goal_y'
                else:
                    self.pddl_values[3] = label
                    response = self.plan()
                    self.state = 'planning'
        if response != 'confirm':     
            self.last_sentence = response
        response_type = 'text'
        return response_type, response
    
    def process_questions(self, input):
        label = self.model(input, candidate_labels=['quit', 'info', 'max velocity', 'average velocity', 'reward', 'corrections', 'trajectory', 'actions', 'steps', 'how long'])['labels'][0]
        print(f'label predicted: {label}')
        if label == 'quit':
            response_type = 'text'
            response = 'confirm'
            self.restore = self.state
            self.state = 'quitting'
        elif label == 'info':
            response_type = 'text'
            response = 'questions'
        elif label == 'max velocity':
            response = self.max_velocity()
            response_type = 'direct'
        elif label == 'average velocity':
            response = self.avg_velocity()
            response_type = 'direct'
        elif label == 'reward':
            response = self.get_reward()
            response_type = 'direct'
        elif label in ['corrections', 'trajectory', 'actions']:
            response = self.get_corrections()
            response_type = 'direct'
        elif label in ['steps', 'how long']:
            response = f'I cannot tell the exact number because it depends on the starting force applied to me, but it should take around {len(self.actions)} steps.'
            response_type = 'direct'
        if response != 'confirm':     
            self.last_sentence = response
        return response_type, response
    
    def process_planning(self, input):
        response_type = None
        if self.custom == 'goal':
            label = self.model(input, candidate_labels=['quit', 'play', 'story'])['labels'][0]
            print(f'label predicted: {label}')
            if label == 'quit':
                response = 'confirm'
                self.restore = self.state
                self.state = 'quitting'
            elif label == 'play':
                response = 'start_game'
                self.custom = 'game'
                self.game = LulaGame()
                self.game.start(self.model)
                self.game.state = 'running'
            elif label == 'story':
                # read a file with the story one line at the time while checking for self.process
                response = self.read_story()
                response_type = 'loop'
                self.custom = 'story'
        elif self.process.poll() is None:
            if self.custom == 'game':
                # esegui azione stessa cosa di lula_game, ma prima fai check se ha finito self.process
                label = self.model(input, candidate_labels=['go up', 'idle', 'go left', 'go right', 'quit'])['labels'][0]
                print(f'label predicted: {label}')
                if label == 'quit':
                    self.custom = 'goal'
                    response = 'wait'
                    self.game.reset()
                else:
                    response_type, response = self.game.play_action(label)
            elif self.custom == 'story':
                response = self.read_story()
                if response != 'end':
                    response_type = 'loop'
                else:
                    self.custom = 'goal'                  
        else:
            # planning done.
            response = 'planned'
            self.policy = policy.get_policy(f'{LUNAR_LANDER_PATH}{self.domain}', custom=True)
            self.play_simulator(self.pddl_values[0], self.pddl_values[1])
            self.state = 'questions'
        if response_type not in ['direct', 'loop']:
            response_type = 'text'
        if response != 'confirm':     
            self.last_sentence = response
        return response_type, response

    
    def process_input(self, input):
        if self.state == 'quitting':
            response_type, response = self.process_quit(input)        
        elif self.state == 'model':
            response_type, response = self.process_model(input)            
        elif self.state == 'goal':
            response_type, response = self.process_goal(input)        
        elif self.state == 'custom':
            response_type, response = self.process_custom(input)          
        elif self.state == 'questions':
            response_type, response = self.process_questions(input)
        elif self.state == 'planning':
            response_type, response = self.process_planning(input)
        return response_type, response
            
    def play_simulator(self, init_x = 'center', init_y = 'high'):
        self.env = Lander(gym.make('LunarLander-v2', render_mode='human'))
        observation, info = self.env.reset(init_x, init_y)
        terminated = False
        while not terminated:
            next_action = policy.get_action(observation, self.domain, self.policy)
            if next_action == 'goal':
                return
            self.actions.append(next_action)
            observation, reward, terminated, truncated, info = self.env.step(ACTION_DICT[next_action])
            if observation[-1] or observation[-2]:
                continue
            else:
                o = []
                for i in range(6):
                    o.append(float('{:.8f}'.format(observation[i])))
                self.observations.append(o)
                self.rewards.append(reward)

    def max_velocity(self):
        max_vx, max_vy, max_vt = self.observations[0][2], self.observations[0][3], self.observations[0][5]
        for obs in self.observations:
            if abs(obs[2]) > abs(max_vx):
                max_vx = obs[2]
            if abs(obs[3]) > abs(max_vy):
                max_vy = obs[3]
            if abs(obs[5]) > abs(max_vt):
                max_vt = obs[5]
        max_vx = round(float(max_vx), 3)
        max_vy = round(float(max_vy), 3)
        max_vt = round(float(max_vt), 3)
        return f'I will tell you all. The maximum velocity reached in the horizontal component is {max_vx}, for the vertical component it is {max_vy} and the max angular velocity is {max_vt}.'
    
    def avg_velocity(self):
        avg_vx, avg_vy, avg_vt = 0, 0, 0
        length = len(self.observations)
        for obs in self.observations:
            avg_vx += obs[2]
            avg_vy += obs[3]
            avg_vt += obs[4]
        avg_vx = round(float(avg_vx/length), 3)
        avg_vy = round(float(avg_vy/length), 3)
        avg_vt = round(float(avg_vt/length), 3)
        return f'The average for horizontal, vertical and angular velocities are {avg_vx}, {avg_vy} and {avg_vt} respectively.'
    
    def get_reward(self):
        tot_reward = sum(self.rewards)
        length = len(self.rewards)
        avg_reward = tot_reward/length
        return f'The extected reward is {tot_reward}, while the average reward in step is {avg_reward}, for an episode that should take {length} steps.'
    
    def get_corrections(self):
        main, idle, left, right = 0, 0, 0, 0
        for a in self.actions:
            if a == 'main_engine':
                main += 1
            if a == 'idle':
                idle += 1
            if a == 'left_engine':
                left += 1
            if a == 'right_engine':
                right += 1
        answer = f'Given a starting point at the center of the environment, with a random force applied to me, i would make around {left + right} corrections to the trajectory, while {main} executions of the main engine to counterbalance the gravity.'
        if main < 5:
            answer = answer + " This is because I just plan in the neighboring states of the trajectory, I should do some Reinforcement Learning to reach optimal performances."
        return answer

    def read_story(self):
        with open('sentences/story.txt', 'r') as f:
            lines = f.readlines()
        if self.line < len(lines):
            current = lines[self.line]
            self.line += 1
            return current
        else:
            self.line = 0
            return 'end'
    
    def plan(self):
        init = 5
        if self.domain == 'novelocity':
            goal = 17
        else:
            goal = 29
        with open(f'{LUNAR_LANDER_PATH}{self.domain}/template.pddl', 'r') as re:
            with open(f'{LUNAR_LANDER_PATH}{self.domain}/custom_prob.pddl', 'w') as wr:
                lines = re.readlines()
                for i, line in enumerate(lines):
                    if i == init and self.pddl_values[0] is not None:
                        line = line.replace('(current_x x_0)', f'(current_x x_{CUSTOM_DICT[self.domain][self.pddl_values[0]]})')
                        line = line.replace('(current_y y_0)', f'(current_y y_{CUSTOM_DICT[self.domain][self.pddl_values[1]]})')
                    elif i == goal and self.pddl_values[2] is not None:
                        line = line.replace('(current_x x_0)', f'(current_x x_{CUSTOM_DICT[self.domain][self.pddl_values[2]]})')
                        if line.find('(current_y y_0)') != -1:
                            line = line.replace('(current_y y_0)', f'(current_y y_{CUSTOM_DICT[self.domain][self.pddl_values[3]]})')
                        else:
                            line = line.replace('(ground)', f'(current_y y_{CUSTOM_DICT[self.domain][self.pddl_values[3]]})')
                    wr.write(line)
        command = ['./../../prp/prp', './domain.pddl', './custom_prob.pddl', '--jic-limit', '10', '--dump-policy', '2']
        self.process = subprocess.Popen(command, shell=False, cwd=f'lunar_lander/{self.domain}', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        return 'wait'
        
