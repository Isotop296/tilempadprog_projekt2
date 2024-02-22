
import tkinter as tk # used to creat the gui
import speech_recognition as sr
from tkinter import messagebox #to creat the gui
import os 
import openai #used for open ai, dont know i its relly neded
import requests  # To send HTTP requests
from gtts import gTTS  # Googles text to speech library
from dotenv import load_dotenv #this is used to take in the api key from another file, i used it so that me api key to chat gpt would be safe and not be upploaded to github. gitignore is used so that .env isent upploaded to github witch contains my api key

load_dotenv()# starts the dotenv 
openai.api_key = os.getenv("OPENAI_API_KEY")#gets the api key an sets it as a wolrld key within the openai import


def speech_to_text():
   r = sr.Recognizer() 
   with sr.Microphone() as source:  #sets the microphone as input source when then doing the stt
      r.adjust_for_ambient_noise(source) #to adjust and work better with backgrund noise
      try: # it starts by traying all this tp exept and if it doesent work it sends back one of the exepts
        audio = r.listen(source) #sets varieble audio to what you say, the r.listen(source) records a prhase from source
        recognized_text = r.recognize_google(audio) #her it takes the audio file and uses the speech recognition(recognize_google) to make the audio inte text
        print("Recognized text: " + recognized_text)#only used to be able to check that it works
        return recognized_text #returns the speech to text
      except sr.UnknownValueError: #only starts if try gets an unknown value error
        print("Google Speech Recognition could not understand audio")#prints the message
        return None #returns nothing
      except sr.RequestError as e:#only starts if the try gets a request error
        print("Could not request results from Google Speech Recognition service; {0}".format(e)) #prints the message
        return None#returns nothing
  
  
def exit_text_to_speech():#is used to close down the gui without needing to do it with the x
    result = messagebox.askquestion("exit system", "confirm if you want to exit") #creates a message box that is showned to the user
    if result == 'yes': #creates an if sats that if you press yes it will pop upp another message and then close the gui
      messagebox.showinfo("goodbye", "good bye")
      root.destroy()


def chat_with_gpt(prompt):#creates a funktion that also need varibel
    try:
       response = openai.ChatCompletion.create(#this sends the request to open ai, to have the model gpt-3.5-turbo send back answers
       model="gpt-3.5-turbo",
       messages=[
          {"role": "system", "content": "You are a sport nerd, that knows alot about sports."},#sends to the models who and how the model should act
          {"role": "user", "content": "who won the world cup in fotboll 2022?"}, # sends in a pre used question to have the modeld more tuned to the first string
          {"role": "assistant", "content": "Argentina won the world cup in 2022 and they beat France in the final."},# sets how the model should answer the already set question so that the modeld is more tuned to the first string
          {"role": "user", "content": "who won the premier league in 2023?"},# sends in a pre used question to have the modeld more tuned to the first string
          {"role": "assistant", "content": "it was manchester city, that got a total of 89 points."},# sets how the model should answer the already set question so that the modeld is more tuned to the first string
          {"role": "user", "content": prompt},#sends in the varibel that was sent in with the funktion to the ai model, so that the model can answer
        ] 
)
       return response['choices'][0]['message']['content']#takes ut the answer from the ai model adn returns it
    except Exception as e: #if the try doesent work this will instead happen
        print(f"Error: {e}")#prints error
        return None #returns none

def main(input1):
    user_input = input1 #sätter variabeln som är input, som i detta läget är det man får från speech_to_text funktionen
    prompt = f"You: {user_input}\nChatGPT Bot:" #sätter manningen och user inputen lika med variabeln prompt
    try:     
       response = chat_with_gpt(prompt)#sätter in menningen(prompt)och skickar den till funktionen chat_with_gpt och sätter den till variabeln respons
       print(response) #sedan printar jag respons bara som test för mig.
       return response #returnar respons
    except sr.RequestError: #Ifal det blev något fel så kommer det nedan istället skickas
        print("could not get an answer")
        return ("I can not answer that, try agian or ask another question.")
        


def test():
    try:
       stt = speech_to_text() #sätter variabeln stt till funktionen speech_to_text() och kör den
       generated_text = main(stt)# skickar sedan in stt in i funktionen main och sätter det till variabel  generated_text
       answer_chat.insert(tk.END , generated_text + "\n") #sedan sätter jag detta så att svaret som man får ut ska skrivas ut på gui skärmen
       tts = gTTS(generated_text) #detta skickar in svaret/generated_text in till google text to speech och sätter den på variabeln tts
       tts.save("generated_text.mp3") #sparar tss som generated_text.mp3
       return os.system("start generated_text.mp3") #skickar sedan ut mp3 filen och spelar upp den med os.system
    except sr.RequestError: #om det skulle bli något fel i try så kommer exept köras
        print("kunde inte skapa ljud fil")
        return None
        


root = tk.Tk() #creats the frame for the gui
root.title("speech to text")
   
   
MainFrame = tk.Frame(root, bd =20, width =900, height =300)  #gives specifiks like the height and the width to the main frame
MainFrame.pack()

lblTitle = tk.Label(MainFrame, font = ("ariel", 40, "bold"), text = ("speech to text"), width = 28) #creates the head text for the gui
lblTitle.pack() 

answer_chat = tk.Text(MainFrame, font = ("ariel", 25, "bold"),width = 34, height=8) #makes it so that if answer_chat gets an input text it will be displayed on the mainframe
answer_chat.pack()

btnConvert = tk.Button(MainFrame, font = ("ariel", 30, "bold"), text = ("convert to text"), width = 20, height=2, command = speech_to_text) #button that aktivates the funktion speech_to_text
btnConvert.pack(side = tk.LEFT, padx=5)

btnConv = tk.Button(MainFrame, font = ("ariel", 30, "bold"), text = ("convert"), width = 20, height=2, command = test) #button that aktivates the funktion test
btnConv.pack(side = tk.LEFT, padx=5)

btnExit = tk.Button(MainFrame, font = ("ariel", 30, "bold"), text = ("exit"), width = 20, height=2, command = exit_text_to_speech) #button that aktivates the funktion exit_text_to_speech
btnExit.pack(side = tk.LEFT, padx=5)

root.mainloop() #starts the gui


