import tkinter as tk
import speech_recognition as sr
from tkinter import messagebox
import os

def speech_to_text():
   r = sr.Recognizer()
   with sr.Microphone() as source:
      try:
        audio = r.listen(source)
        text = r.recognize_google(audio)
        txtSpeech.insert(tk.END, text + "\n")
      except sr.UnknownValueError:
        txtSpeech.insert(tk.END, "could not understand audio\n")
      except sr.RequestError as e:
        txtSpeech.insert(tk.END, "Error: {0}\n".format(e))
  
  
   
root = tk.Tk()
root.title("speech to text")
   
   
MainFrame = tk.Frame(root, bd =20, width =900, height =300)  
MainFrame.pack()

lblTitle = tk.Label(MainFrame, font = ("ariel", 40, "bold"), text = ("speech to text"), width = 28)
lblTitle.pack()

txtSpeech = tk.Text(MainFrame, font = ("ariel", 25, "bold"),width = 68, height=12)
txtSpeech.pack()

btnConvert = tk.Button(MainFrame, font = ("ariel", 30, "bold"), text = ("convert to text"), width = 20, height=2, command = speech_to_text)
btnConvert.pack(side = tk.LEFT, padx=5)

btnReset = tk.Button(MainFrame, font = ("ariel", 30, "bold"), text = ("reset text"), width = 20, height=2 )
btnReset.pack(side = tk.LEFT, padx=5)

btnExit = tk.Button(MainFrame, font = ("ariel", 30, "bold"), text = ("exit"), width = 20, height=2)
btnExit.pack(side = tk.LEFT, padx=5)

root.mainloop()
