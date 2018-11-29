#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile
import scipy.fftpack as sp
import pyaudio
import wave
class alexa:
    def process(self):
        # pyaudio  realtime
        # reference：https://www.programcreek.com/python/example/52624/pyaudio.PyAudio
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        #Channel number
        CHANNELS = 2
        #Sampling Rate
        RATE = 48000
        #record time
        RECORD_SECONDS = 3
        #name of record file
        WAVE_OUTPUT = "realtime.wav"
        #
        p = pyaudio.PyAudio()
        #
        stream = p.open(format=FORMAT, channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
        # the reminder of strating
        print("please say hello or action in 2s")
        # create a list to save record data
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data1 = stream.read(CHUNK)
            frames.append(data1)
        # the reminder of ending
        print("record end")
        #end recording
        stream.stop_stream()
        stream.close()
        p.terminate()
        #write the data from the frames to wav file
        wf = wave.open(WAVE_OUTPUT, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
       #read the wav file
        fs,data = wavfile.read(r"realtime.wav","rb")
        def fourier(x):
            return sp.fft(x)
        def detection(data):
            # create a list to save the left channel data
            datatest = []
            for i in range(0, len(data)):
             datatest.append(data[i][0])
            #chop the data to some chunks ,every 200ms
            data4 = []
            for i in range(0, int(len(data) / 9600)):
                data4.append(datatest[i * 9600:(i + 1) * 9600])
            #Fourier transform for each piece of data
            data4f = fourier(data4)
            #Establish the sound vector of the data (take the maximum value to form the vector)
            maxfeature = []
            for i in range(0, len(data4f)):
                maxfeature.append(np.max(data4[i]))
            #Replace the maximum value of the sound vector below 50HZ with 0
            for i in range(0, len(maxfeature)):
                if maxfeature[i] < 50:
                    maxfeature[i] = 0
                else:
                    maxfeature[i] = maxfeature[i]
            #Remove the above element with 0
            vec = []
            for i in range(0, len(maxfeature)):
                if maxfeature[i] != 0:
                    vec.append(maxfeature[i])
                else:
                    vec = vec
            #Take the first five digits of the sound vector as the judgment vector
            vec = vec[0:5]
            # Hello reference vector
            # Action reference vector
            hellovec = [(1305 + 7413) / 2, (1596 + 2137) / 2, (244 + 4133) / 2, 2176 / 2, 3118 / 2]
            actionvec = [916 / 2 + 3450 / 2, 1288 / 2 + 2461 / 2, 625 / 2 + 3100 / 2, 616 / 2 + 32767 / 2,
                         197 / 2 + 32767 / 2]
            #Calculate the Euclidean distance between the hello and the action vector
            distancehello = np.linalg.norm(np.array(vec) - np.array(hellovec))
            distanceaction = np.linalg.norm(np.array(vec) - np.array(actionvec))
            #Discriminating the distance between vectors
            if distancehello < distanceaction:
                print('hello')
            else:
                print('action')
        detection(data)
for i in range(1,100):
    a = alexa()
    a.process()






