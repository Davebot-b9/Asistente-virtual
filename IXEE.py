import pyttsx3
import pywhatkit
import speech_recognition as sr
import urllib.request
import json
import datetime
import wikipedia

# Nombre del asistente virtual
NAME = 'cortana'

# Clave API de Google para YouTube
KEY = 'AIzaSyC9hsAezhvsHzLokgBu3ooZCIcGmUw897I'

# Reconocedor de voz
listener = sr.Recognizer()

# Motor de síntesis de voz
engine = pyttsx3.init()

# Seleccionar la primera voz disponible
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    """Habla en voz alta el texto proporcionado."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Escucha y reconoce la voz del usuario."""
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            rec = listener.recognize_google(voice)
            rec = rec.lower()
            if NAME in rec:
                rec = rec.replace(NAME, "")
                print(rec)
        wikipedia.set_lang("es")
    except:
        # En caso de error, devolver una cadena vacía
        return ""
    return rec

def run():
    """Ejecutar el asistente virtual."""
    rec = listen()
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)
    elif 'cuántos suscriptores tiene' in rec:
        name_subs = rec.replace('cuántos suscriptores tiene', '')
        data = urllib.request.urlopen(
            'https://www.googleapis.com/youtube/v3/chanels?part=statistics&forUsername=' + name_subs.strip() + '&key=' + KEY).read()
        subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
        talk(name_subs + " tiene {:,d}".format(int(subs)) + " suscriptores!")
    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)
    elif 'busca' in rec:
        order = rec.replace('busca', '')
        info = wikipedia.summary(order, 1)
        talk(info)
    else:
        talk("Vuelve a intentarlo")

while True:
    run()

