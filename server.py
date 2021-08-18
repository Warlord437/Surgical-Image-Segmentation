from vosk import Model, KaldiRecognizer
import os
import pyaudio
import subprocess
import socket

def takeCommand():
    if not os.path.exists("model1"):
        print(
            "Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
        exit(1)

    model = Model("model1")
    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("Start SPEAKING:-")
    subprocess.call(['/usr/bin/canberra-gtk-play', '--id', 'bell'])

    while True:
        final_string = ''
        data = stream.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            curr = eval(rec.Result())['text']
            final_string = final_string + curr
            print(final_string)
            return final_string.lower()
        else:
            continue


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    msg = takeCommand()
    clientsocket, address = s.accept()
    print("Connection has been established !")
    clientsocket.send(bytes(msg, "utf-8"))
    clientsocket.close()
