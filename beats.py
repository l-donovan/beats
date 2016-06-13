#!/usr/local/bin/python3

from tkinter import *

import pyaudio
import wave
import threading

CHUNK = 2**10
p = pyaudio.PyAudio()

clips = [
	"audio/Wet_Dreamz_Loop_Kick.wav",
	"audio/Wet_Dreamz_Loop_Snare.wav",
	"audio/Wet_Dreamz_Loop_Strings_3.wav",
	"audio/Wet_Dreamz_Loop_Strings_2.wav",
	"audio/Wet_Dreamz_Loop_Strings_1.wav"
	]

clipsKeys = {}

reset = False
playThread = None

def playClipThread(path):
	wf = wave.open(path, 'rb')
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
			channels=wf.getnchannels(),
			rate=wf.getframerate(),
			output=True)

	data = wf.readframes(CHUNK)

	while (data and not reset):
		stream.write(data)
		data = wf.readframes(CHUNK)

def killThread():
	global reset
	global playThread

	if (threading.active_count() > 1):
		reset = True
		playThread.join()
		reset = False

def playClip(clip):
	global playThread

	killThread()

	playThread = threading.Thread(target=playClipThread, args=(clip,))
	playThread.start()

def keydown(e):
	if (e.char == ' '):
		killThread()
		return
	clipId = clipsKeys.get(e.char, -1)
	if (clipId != -1): playClip(clips[clipId])

root = Tk()
frame = Frame(root, width=100, height=100)
frame.bind("<KeyPress>", keydown)
frame.focus_set()

buttons = [None] * 16
for i in range(len(buttons)):
	buttons[i] = Button(frame, text='', width=2, height=2)
	buttons[i].grid(row=i // 4, column=i % 4)

def assignButton(i, clipId):
	buttons[i].config(command=lambda j=clipId+0: playClip(clips[clipId]))

def assignKey(char, clipId):
	clipsKeys[char] = clipId

# KEY ASSIGNMENTS
assignKey('a', 0)
assignKey('s', 1)
assignKey('c', 2)
assignKey('x', 3)
assignKey('z', 4)

# BUTTON ASSIGNMENTS
assignButton(0, 0)
assignButton(1, 1)
assignButton(4, 4)
assignButton(5, 3)
assignButton(6, 2)

frame.pack()
root.mainloop()
