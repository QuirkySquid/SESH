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
    # set up variables for PyAudio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    Recording = 0
    frames = []

    startTime = 0

    running = True

    WAVE_OUTPUT_FILENAME = "recording "

    # main function
    def init(self):

        # assign keyboard inputs to functions
        keyboard.on_press_key('space', self.space_pressed)
        keyboard.on_press_key('esc', self.quit)

        # init PyAudio
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

    # runs on exit
    def quit(self, event):
        # if currently recording...
        if (self.Recording == 1):
            # set state to 'quit'
            self.Recording = -2
            return

        # stop the recorder
        self.p.terminate()
        self.running = False

    # runs when space is pressed
    def space_pressed(self, event):
        # toggle recording state
        if (not self.Recording): self.start_record()
        else: self.Recording = -1
        return

    # starts the recording
    def start_record(self):
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        self.replaceTimeText("* Recording")
        # set recording state
        self.Recording = 1

        # stores the starting time for recording time display
        self.startTime = time.time()

        self.frames = []

    # records audio
    def record(self):
        # 2 is filename state- runs while filename is being entered
        if self.Recording == 2: return
        # 1 is recording state
        if self.Recording == 1:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

            # display current length
            currentLength = (int) (time.time() - self.startTime)
            self.replaceTimeText("Recording: [{}:{}]".format(
                math.floor(currentLength / 60), str(currentLength % 60).zfill(2)
            ))
        # -1 is end state
        elif self.Recording == -1:
            self.end_record(True)
        # -2 is quit state
        elif self.Recording == -2:
            self.end_record(False)
            self.quit(None)

    # ends the recording 
    def end_record(self, inputName):
        # sets filename state
        self.Recording = 2
  
        # close up pyaudio
        self.stream.stop_stream()
        self.stream.close()

        FILENAME = ""

        # prompts user for filename
        if (inputName):
            sys.stdout.write("\033[F\033[F\033[K")
            sys.stdout.flush()
            FILENAME = input("Input File Name: ")
            sys.stdout.flush()
            sys.stdout.write("\033[E\033[E")

            if (FILENAME != ""):
                # remove heading whitespace
                while (FILENAME[0] == " "):
                    FILENAME = FILENAME[1:]
                    if (FILENAME == ""): break

        # default filename is the current time
        if (FILENAME == ""): FILENAME = self.WAVE_OUTPUT_FILENAME + (str) (time.asctime())
        # add .wav extension
        FILENAME = FILENAME + ".wav" 

        self.replaceTimeText("Saved as " + FILENAME)

        # set idle state
        self.Recording = 0

        # create the file
        wf = wave.open(FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setframerate(self.RATE)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.writeframes(b''.join(self.frames))
        wf.close()

    # replaces the time text
    def replaceTimeText(self, text):
        sys.stdout.write("\033[F\033[F\033[K")
        sys.stdout.flush()
        sys.stdout.write(text)
        sys.stdout.flush()
        sys.stdout.write("\033[E\033[E")




if __name__ == '__main__':
    sesh = sesh()
    sesh.init()