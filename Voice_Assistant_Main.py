import os
import re
import sys
import time
import geocoder
import requests
import getpass
import wikipedia
import urllib
import keyboard
import linecache as lc
import subprocess as sp
from subprocess import PIPE
import pyttsx3 as tts
import speech_recognition as sr
import warnings
warnings.catch_warnings()
warnings.simplefilter("ignore")

AFFIRMATIVE_RESPONSE = ["yes","sure","okay","ok","definitely"]
WINDOWS_APPS = ["calculator","notepad"]

USERNAME = getpass.getuser()

temp_said = ""
speak_rate = 135

name_open = ""
path_open = ""

name_list = []
name_instance = open("File_Names.txt","a+")
NAME_str = ""

path_list = []
path_instance = open("File_Paths.txt","a+")
PATH_str = ""

input_name = ""
input_path = ""
def CONNECT(host='https://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

def find_loc_ip(ip_add):
    try:
        resp = requests.get("http://ip-api.com/json/"+ip_add).json()
        lon_lat_list = str(resp['lon'])+str(resp['lat'])
        location = "bruh"
        ans = "Status:- "+ str(resp['status'])  +"\n"+  "---Country---"+"\n"+ str(resp['country'])  +"\n"+  "---Region---"   +"\n"+   str(resp['regionName'])  +"\n"+  str(resp['city'])  +"\n"+  "ZipCode-" + str(resp['zip'])  +"\n"+   "---Latitude/Longitude---"   +"\n"+   "Latitude- " + str(resp['lat']) +"\n"+ "Longitude- " + str(resp['lon']) + "\n" + "---ISP---" + "\n"+ str(resp['isp'])
        print(ans)
    except Exception as e:
        print("Couldn't complete process, Invalid IP or Check your Internet connection\nError:- "+e)

work_mode = int('1' if CONNECT() else '0')

def search(keyword,lines):
    try:
        ans = ""
        try:
            try:
                ans = f">>Summary of the Given Keyword =>\n{wikipedia.summary(keyword,sentences=lines)}"
                print(ans)
            except Exception as e:
                print(e)
                #print("\nSuggestions -"+str(wikipedia.suggest(keyword)))
                ask = input("\n---------------------\nDo you want to continue to suggestions ? => ")
                if str(ask) in AFFIRMATIVE_RESPONSE:
                    replied = input("\n---------------------\nSelect any suggestion to view it's summary => ")
                    ans = wikipedia.summary(replied,lines)
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Error =>{e}")
    except Exception as e:
        ans = ">>Cancelled"
        print("Unable to find a viable answer")
        print("\nError:- "+str(e))

    return ans

def Start_Clear():
        print("Clearing Memory and Starting")
        speak("Clearing Memory and Starting",speak_rate)

        response = r'Connected to Internet, Work Mode will be at "Full Capacity"' if CONNECT() else r'Not Connected to Internet, please try again, Work Mode will be "Minimalistic"'
        print(response)
        speak(response,speak_rate)
        work_mode = int('1' if CONNECT() else '0')

        name_instance_seek = 0
        path_instance_seek = 0

        NAME_str = name_instance.readlines()
        PATH_str = path_instance.readlines()

        name_list = list(NAME_str)
        path_list = list(PATH_str)

        input_name = ""
        input_path = ""

        return name_instance_seek, path_instance_seek, name_list, path_list

def speak(text,talk_rate):
    voice = tts.init()
    voice.setProperty('rate',talk_rate)
    voice.say(text)
    voice.runAndWait()
    voice.stop()

def get_input_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        said = ""
        try:
            print(">>Adjusting for background noise. One second<<")
            r.adjust_for_ambient_noise(source)
            print("\nListening Audio...")
            audio = r.listen(source,phrase_time_limit=4)
            try:
                said = r.recognize_google(audio)
                said = said.lower()
                return said
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            said = ""
            exception = str(e)
            if exception == "recognition connection failed: [Errno 11001] getaddrinfo failed":
                string = "Error:" + exception + "\n[Please check your connection to Internet or type your input manually]"
                print(string)
                speak(string)
            else:
                string = "Error:" + exception
                print(string)
                speak(string)

def Save_NameandPath(name,path):
    file_name = str(name.replace("\\","\\"))
    file_path = str(path.replace("\\","\\"))

    name_list = str(open('File_Names.txt','r').read())
    path_list = str(open('File_Paths.txt','r').read())

    name_instance = open('File_Names.txt','a+')
    path_instance = open('File_Paths.txt','a+')

    if name not in name_list and path not in path_list:
        name_instance.write(name + "\n")
        path_instance.write(path + "\n")
        print("Names and Paths have been saved")
        speak("Names and Paths have been saved",speak_rate)
    else:
        print("Error :- The Name and Path already exist in My Storage")
        speak("Error :- The Name and Path already exist in My Storage",speak_rate)

    name_instance.close()
    path_instance.close()

def open_file(name,path):
    try:
        name_edit = name.replace("\n","")
        sp.Popen(path.replace("\n","")+"\\"+name_edit)
    except Exception as e:
        print("Couldn't fine the specified file \nError:-"+e)

def open_app(name):
    if name in WINDOWS_APPS:
        if name == "calculator":
            sp.Popen("calc")
        elif name == "notepad":
            sp.Popen("note")
    else:
        print("The Requested app is not a Windows Default App, retry or open using Normal Method")

def Check_Path_Loc(name):
    read_line = 1
    while lc.getline("File_Names.txt",read_line).lower().replace("\n","") != name.lower():
        read_line+=1
    path_returned = lc.getline("File_Paths.txt",read_line)
    name_returned = lc.getline("File_Names.txt",read_line)
    return path_returned.replace("\n",""),name_returned.replace("\n","")

def make_note(text,filename):
    file = open("C:\\Users\\" + USERNAME+ "\\Desktop\\"+filename+".txt","w")
    file.write(text)
    file.close()
    print("Created text file")
    speak("Created text file",speak_rate)

def interpret():
    n_in_s, p_in_s, name_list, path_list = Start_Clear()
    name_instance.seek(n_in_s)
    path_instance.seek(p_in_s)

    while True:
        if keyboard.is_pressed("e"):
            speak("Enter Input Name",speak_rate)
            input_name = input("Enter Name:-")
            speak("Enter Input Path",speak_rate)
            input_path = input("Enter Path:-")
            Save_NameandPath(input_name,input_path)

        if keyboard.is_pressed("f"):
            try:
                if work_mode == 1:
                    temp_said = get_input_audio()
                    said_word_list = list(temp_said.split())
                    print(said_word_list)
                    name_given = str(said_word_list[1])
                    print("You said - "+str(temp_said))

                    if "open" in said_word_list:
                        response = False
                        print("\nDo you want to open the requested file ?")
                        speak("Do you want to open the requested file ?",speak_rate)
                        answer = get_input_audio()
                        answer_list = list(answer.split())
                        for a in AFFIRMATIVE_RESPONSE:
                            for b in answer_list:
                                if a==b:
                                    response = True

                        print('You said - '+answer)

                        path_open, name_open = Check_Path_Loc(name_given+".exe")
                        if answer not in WINDOWS_APPS:
                            if response == True:
                                print("\n>> Opening File <<")
                                speak("Opening File",speak_rate)
                                open_file(name_open,path_open)
                            else:
                                print("\n>> Won't open file <<")
                                speak("Won't open file",speak_rate)
                        else:
                            op = open_app(answer.lower())


                    if "search" in said_word_list:
                        response = False
                        reply = search(said_word_list,"3")
                        print(reply)

                    if "note" in said_word_list:
                        said_word_list.remove('note')
                        print(">>What do you want to have as the file name ?")
                        speak("What do you want to have as the file name",speak_rate)
                        answer = get_input_audio()
                        make_note(str(said_word_list),answer)

                else:
                    response = "Can't use voice recognition without Internet, check your internet connection or Use Written text as Input"
                    print(response)
                    speak(response,speak_rate)
                    time.sleep(1)
            except Exception as e:
                response = "Couldn't complete the given process\nError: "+e
                print(response)
                speak(response,speak_rate)

interpret()
