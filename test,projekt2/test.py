
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


def chatgpt_answer(prompt):
 # API Key for OpenAI (insert your own)
    api_key = "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"

    # The API endpoint for the GPT-2 model
    url = "https://api.openai.com/v1/engines/text-davinci-002/completions"

    # The headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # The data for the API request
    data = {
        "promt": prompt,
        "max_tokens": 512,
    }

    # Send the request to the API
    response = requests.post(url, headers=headers, json=data)

    # Get the generated text from the API response
    generated_text = response["choices"][0]['message']["text"]

    print("Generated text: " + generated_text)
    return generated_text
        


def test():
    try:
       generated_text = chatgpt_answer(speech_to_text())
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



