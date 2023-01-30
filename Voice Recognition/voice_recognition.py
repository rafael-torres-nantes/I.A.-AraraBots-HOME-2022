import speech_recognition as sr

def ouvir_microfone(): # Funcao para ouvir e reconhecer a fala
    module_rec = sr.Recognizer() # Instancia o Modulo Reconhecedor

    with sr.Microphone() as mic: # Invoca o Mic de Gravacao 
        audio = module_rec.listen(mic) # O metodo listen vai ouvir o que a gente falar e gravar na variavel frase

    frase = module_rec.recognize_google(audio, language='pt')

    print(frase)

    #if " " in frase.lower():
        #print(" ")

    return frase