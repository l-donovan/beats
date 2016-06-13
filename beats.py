#!/usr/local/bin/python3

from tkinter import *

import pyaudio
import wave
import threading

CHUNK = 2**10
p = pyaudio.PyAudio()

clips = {
	'a': "audio/Wet_Dreamz_Loop_Kick.wav",
	's': "audio/Wet_Dreamz_Loop_Snare.wav",
	'c': "audio/Wet_Dreamz_Loop_Strings_3.wav",
	'x': "audio/Wet_Dreamz_Loop_Strings_2.wav",
	'z': "audio/Wet_Dreamz_Loop_Strings_1.wav"
	}

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
	clip = clips.get(e.char, False)
	if (clip): playClip(clip)
	
root = Tk()
frame = Frame(root, width=100, height=100)
frame.bind("<KeyPress>", keydown)
frame.focus_set()

buttons = [None] * len(clips)
for i, key in enumerate(clips):
	buttons[i] = Button(root, text=key, anchor=W, justify=LEFT, padx=2, command=lambda j=key+'': playClip(clips[j]))
	buttons[i].config(activeforeground="green")
	buttons[i].config(disabledforeground="white")
	buttons[i].pack()

frame.pack()
root.mainloop()
