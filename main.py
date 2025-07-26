import speech_recognition as sr
from input_processor import IO_Processor


def capture_audio(recognizer, audio, io):
    try:
        input = r.recognize_sphinx(audio)
        print("Audio input: " + input)
        io.process_input(input)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

def init():
    io = IO_Processor()
    #r = sr.Recognizer()
    #mic = sr.Microphone()
    #print(sr.Microphone.list_microphone_names())
    return io#, r, mic

#MAIN
#io, r, mic = init()
io = init()

#stop_listening = r.listen_in_background(mic, capture_audio(io))
#io.set_stop(stop_listening)
io.say_something('greetings')

while not io.quitting:
    text = input('Type here: ')
    if text == '':
        continue
    io.process_input(text)