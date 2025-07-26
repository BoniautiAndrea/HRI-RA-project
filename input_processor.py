from transformers import pipeline
from gtts import gTTS
#from playsound import playsound
from play_sounds import play_file
import numpy as np
import json
import random
from lula_sim import LulaSim
from lula_game import LulaGame
import os

class IO_Processor:
    def __init__(self):
        self.model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.quitting = False
        self.sentences = {}
        with open('sentences/sentences.json', 'r') as f:
            self.sentences = json.load(f)
        self.tasks = {}
        self.tasks['game'] = LulaGame()
        self.tasks['sim'] = LulaSim()
        self.current_task = 'none'
        self.labels = ['information', 'close', 'quit', 'simulation', 'planning', 'manual', 'game', 'service', 'greetings']
    
    def set_stop(self, stop):
        self.stop = stop

    def terminate_input(self):
        self.say_something('goodbye')
        # UNCOMMENT WHEN USING MICROPHONE
        #self.stop()
        self.quitting = True
        
    def speak(self, txt, lang='en'):
        print(f'LuLa: {txt}')
        tts = gTTS(text=txt, lang="en")
        filename = "voice.mp3"
        tts.save(filename)
        #playsound(filename, block=True)
        play_file(filename)
        os.remove("voice.mp3")
        print('Speech completed..')

    def say_something(self, title):
        sentence = self.sentences[title]
        self.speak(sentence)

    def process_input(self, input):
        # if there are no running tasks
        if self.current_task == 'none':
            results = self.model(input, candidate_labels=self.labels)
            label = results['labels'][0]
            print('Input processed, command found: '+ label)
            if label in ['close', 'quit']:
                self.terminate_input()
            elif label in  ['information', 'service']:
                self.say_something('info')
            elif label in  ['game', 'manual']:
                self.current_task = 'game'
                response_type, response = self.tasks['game'].start(self.model)
                self.say_something(response)
            elif label in ['simulation', 'planning']:
                self.current_task = 'sim'
                response_type, response = self.tasks['sim'].start(self.model, self.sentences)
                self.say_something(response)
            elif label == 'greetings':
                self.say_something('greetings2')
            else:
                self.say_something('repeat')
        # if there is a running task
        else:
            response_type, response = self.tasks[self.current_task].process_input(input)
            if response_type == 'text':
                self.say_something(response)
            elif response_type == 'reset':
                self.current_task = 'none'
                self.say_something(response)
            # In case of dynamic messages
            if response_type == 'direct':
                self.speak(response)
            # Check planning subprocess
            if response_type == 'loop':
                self.speak(response)
                while response_type == 'loop':
                    response_type, response = self.tasks[self.current_task].process_input('continue')
                    if response_type == 'loop':
                        self.speak(response)
                    else:
                        self.say_something(response)
