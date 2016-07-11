#!/usr/local/bin/python3

from tkinter import *

import pyaudio
import wave
import threading

titleFont = ("Helvetica", 14)
chunkSize = 2**10
p = pyaudio.PyAudio()

class BeatsApp(Tk):
    def openView(self, view):
        view.focus_set()
        view.tkraise()

    def playClipThread(self, path):
        wf = wave.open(path, 'rb')
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

        data = wf.readframes(chunkSize)

        while (data and not self.reset):
            stream.write(data)
            data = wf.readframes(chunkSize)

    def killThread(self):
        if (threading.active_count() > 1):
            self.reset = True
            self.playThread.join()
            self.reset = False

    def playClip(self, clip):
        global playThread

        self.killThread()

        self.playThread = threading.Thread(target=self.playClipThread, args=(clip,))
        self.playThread.start()

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.reset = False
        self.playThread = None

        tabFrame = Frame(self, height=20)
        tabFrame.grid(row=0, column=0)

        contentFrame = Frame(self, height=80)
        contentFrame.grid(row=1, column=0)

        contentFrame.grid_rowconfigure(0, weight=1)
        contentFrame.grid_columnconfigure(0, weight=1)

        self.padView = PadView(parent=contentFrame, app=self)
        self.padView.grid(row=0, column=0, sticky="nsew")

        self.otherView = OtherView(parent=contentFrame, app=self)
        self.otherView.grid(row=0, column=0, sticky="nsew")

        padViewButton = Button(tabFrame, text="Pad", command=lambda: self.openView(self.padView))
        padViewButton.grid(row=0, column=0)

        otherViewButton = Button(tabFrame, text="Other", command=lambda: self.openView(self.otherView))
        otherViewButton.grid(row=0, column=1)

        self.openView(self.padView)

class OtherView(Frame):
    def __init__(self, parent, app):
        Frame.__init__(self, parent)

        label = Label(self, text="Another view will\ngo here eventually", font=titleFont)
        label.pack(side="top", fill="x", pady=10)

class PadView(Frame):
    def keydown(self, e):
        if (e.char == ' '):
            app.killThread()
            return
        clipId = self.keyMap.get(e.char, -1)
        if (clipId != -1): app.playClip(self.clips[clipId])

    def assignButton(self, i, clipId):
        self.buttons[i].config(command=lambda j=clipId+0: app.playClip(self.clips[clipId]))

    def assignKey(self, char, clipId):
        self.keyMap[char] = clipId

    def __init__(self, parent, app):
        Frame.__init__(self, parent)

        self.bind("<KeyPress>", self.keydown)

        self.buttons = [None] * 16
        for i in range(len(self.buttons)):
            self.buttons[i] = Button(self, text='', width=2, height=2)
            self.buttons[i].grid(row=i // 4, column=i % 4)

        with open("pad.py") as f: p = eval(f.read())
        self.clips = p["clips"]
        self.keyMap = p["keyMap"]
        self.buttonMap = p["buttonMap"]
        for i in self.buttonMap: self.assignButton(i, self.buttonMap[i])

if __name__ == "__main__":
    app = BeatsApp()
    app.mainloop()
