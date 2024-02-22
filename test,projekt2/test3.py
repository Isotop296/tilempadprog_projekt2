
import tkinter as tk
import speech_recognition as sr
from tkinter import messagebox
import os
import openai
import requests  # To send HTTP requests
from gtts import gTTS  # Googles text to speech library
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def speech_to_text():
   r = sr.Recognizer()
   with sr.Microphone() as source:
      r.adjust_for_ambient_noise(source)
      try:
        audio = r.listen(source)
        recognized_text = r.recognize_google(audio)
        print("Recognized text: " + recognized_text)
        return recognized_text
      except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
      except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
        return None
  
  
def exit_text_to_speech():
    result = messagebox.askquestion("exit system", "confirm if you want to exit")
    if result == 'yes':
      messagebox.showinfo("goodbye", "good bye")
      root.destroy()


def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            engine="gpt-3.5-turbo",  # You can use a different engine if needed
            prompt=prompt,
            max_tokens=100 , # Adjust as needed
        ) 
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def main(input1):
    user_input = input1
    prompt = f"You: {user_input}\nChatGPT Bot:"
    try:     
       response = chat_with_gpt(prompt)
       print(response)
       return response
    except sr.RequestError:
        print("could not get an answer")
        return ("I can not answer that, try agian or ask another question.")
        


def test():
    try:
       stt = speech_to_text()
       generated_text = main(stt)
       tts = gTTS(generated_text)
       tts.save("generated_text.mp3")
       return os.system("start generated_text.mp3")
    except sr.RequestError:
        print("kunde inte skapa ljud fil")
        return None
        


root = tk.Tk()
root.title("speech to text")
   
   
MainFrame = tk.Frame(root, bd =20, width =900, height =300)  
MainFrame.pack()

lblTitle = tk.Label(MainFrame, font = ("ariel", 40, "bold"), text = ("speech to text"), width = 28)
lblTitle.pack()

generated_text = tk.Text(MainFrame, font = ("ariel", 25, "bold"),width = 34, height=8)
generated_text.pack()

btnConvert = tk.Button(MainFrame, font = ("ariel", 30, "bold"), text = ("convert to text"), width = 20, height=2, command = speech_to_text)
btnConvert.pack(side = tk.LEFT, padx=5)

btnConv = tk.Button(MainFrame, font = ("ariel", 30, "bold"), text = ("convert"), width = 20, height=2, command = test)
btnConv.pack(side = tk.LEFT, padx=5)

btnExit = tk.Button(MainFrame, font = ("ariel", 30, "bold"), text = ("exit"), width = 20, height=2, command = exit_text_to_speech)
btnExit.pack(side = tk.LEFT, padx=5)

root.mainloop()


