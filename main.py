"""
SESH main script, runs program.
Created by QuirkySquid on 8/29/2019.
Made for personal use.
"""

import sys
import time
import math

import pyaudio
import wave
import keyboard

class sesh():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    Recording = 0
    frames = []

    startTime = 0

    running = True

    WAVE_OUTPUT_FILENAME = "recording "

    def init(self):
        
        keyboard.on_press_key('space', self.space_pressed)
        keyboard.on_press_key('esc', self.quit)
        
        self.p = pyaudio.PyAudio()

        print ("""
             _______   _______   _______   ___  ___
            /  ____/  / _____/  /  ____/  /  / /  /
           /  /___   / /__     /  /___   /  /_/  /
          /___   /  / ___/    /___   /  /  __   /
         ____/  /  / /____   ____/  /  /  / /  /
        /______/  /______/  /______/  /__/ /__/
            
            < CREATED BY QUIRKYSQUID >

        """)

        # sys.stdout.write("\033[F") - Go to previous line
        # sys.stdout.write("\033[K") - Clear line

        print("Space - Start/Stop Recording | Esc - Quit")
        print("Not Recording")
        print("")

        
        while self.running:
            self.record()
            continue

        sys.exit(0)

    def quit(self, event):
        if (self.Recording == 1):
            self.Recording = -2
            return

        self.p.terminate()
        self.running = False


    def space_pressed(self, event):
        if (not self.Recording): self.start_record()
        else: self.Recording = -1
        return

    def start_record(self):
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        self.replaceText2("* Recording")
        self.Recording = 1

        self.startTime = time.time()

        self.frames = []

    def record(self):
        if self.Recording == 2: return
        if self.Recording == 1:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

            currentLength = (int) (time.time() - self.startTime)
            self.replaceText2("Recording: [{}:{}]".format(
                math.floor(currentLength / 60), str(currentLength % 60).zfill(2)
            ))
        elif self.Recording == -1:
            self.end_record(True)
        elif self.Recording == -2:
            self.end_record(False)
            self.quit(None)

    def end_record(self, inputName):
        self.Recording = 2
  
        self.stream.stop_stream()
        self.stream.close()

        FILENAME = ""

        if (inputName):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.flush()
            FILENAME = input("Input File Name: ")
            sys.stdout.flush()
            sys.stdout.write("\033[E")
            sys.stdout.write("\033[E")

            if (FILENAME != ""):
                while (FILENAME[0] == " "):
                    FILENAME = FILENAME[1:]
                    if (FILENAME == ""): break

        if (FILENAME == ""): FILENAME = self.WAVE_OUTPUT_FILENAME + (str) (time.asctime())
        FILENAME = FILENAME + ".wav" 

        self.replaceText2("Saved as " + FILENAME)

        self.Recording = 0

        wf = wave.open(FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setframerate(self.RATE)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def replaceText1(self, text):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        sys.stdout.flush()
        sys.stdout.write(text)
        sys.stdout.flush()
        sys.stdout.write("\033[E")
        sys.stdout.write("\033[E")
        sys.stdout.write("\033[E")
 
    def replaceText2(self, text):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        sys.stdout.flush()
        sys.stdout.write(text)
        sys.stdout.flush()
        sys.stdout.write("\033[E")
        sys.stdout.write("\033[E")




if __name__ == '__main__':
    sesh = sesh()
    sesh.init()