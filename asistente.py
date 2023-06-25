import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
import colors
import subprocess as sub 
import os 
from pygame import mixer
import threading as tr
 

name = 'Tym'
listener = sr.Recognizer()
engine = pyttsx3.init()


voices = engine.getProperty('voices')      
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)


sites={
                'google':'google.com',
                'youtube':'youtube.com',
                'facebook':'facebook.com',
                'whatsapp':'web.whatsapp.com'
            }


def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:
            print('Te escucho ...')
            talk("Te escucho")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es')
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name,'')
                print(rec)
    except:
        pass
    return rec


def write(f):
    talk('¿Qué quieres que escriba?')
    print('¿Qué quieres que escriba?')
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk('Listo, puedes revisarlo')
    print('Listo, puedes revisarlo')
    sub.Popen('nota.txt', shell=True)


def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk('Alarma activada' + num + 'horas')
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print('Tu hora solicitada ha llegado')
            mixer.init()
            mixer.music.load('alarma.mp3')
            mixer.music.play()
        else: 
            continue
        if keyboard.read_key() == 's':
            mixer.music.stop()
            break

    
def run():
    while True: 
     rec = listen()
    #Para yt y poner música
     if 'reproduce' in rec:
        music = rec.replace('reproduce', '' )
        talk('Reproduciendo'+ music)
        print('Reproduciendo'+ music)
        pywhatkit.playonyt(music)
     
    #Para decir la hora
     elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk('Son las' +hora) 
        print('Son las' +hora)

    #Para buscar en wikipedia
     elif 'busca' in rec:
        search = rec.replace('busca','')
        wikipedia.set_lang('es')
        wiki = wikipedia.summary(search, 1)
        print(search +': ' + wiki)
        talk(wiki)

    #Para poner alarma
     elif 'alarma' in rec:
        t = tr.Thread(target=clock, args=(rec,))
        t.start()

    #Para colores
     elif 'colores' in rec:
        talk('Enseguida')
        print('Enseguida')
        colors.capture()

    #Para abrir páginas
     elif 'abre' in rec:
         for site in sites:
             if site in rec:
                 sub.call(f'start chrome.exe {sites[site]}', shell=True)
                 talk(f'Abriendo {site}')
                 print(f'Abriendo {site}')

    #Para escribir
     elif 'escribe' in rec:
         try:
             with open('nota.txt', 'a') as f:
                 write(f)
         except FileNotFoundError as e:
            file = open('nota.txt', 'w')
            write(file)


run() 