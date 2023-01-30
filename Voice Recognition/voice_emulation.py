import pyttsx3

def falar_frase(frase):
    engine = pyttsx3.init() # Inicializador PyTTSx3 para Transformar Texto em Audio

    engine.say(frase)
    engine.runAndWait()