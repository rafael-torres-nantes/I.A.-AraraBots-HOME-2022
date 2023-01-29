from audio_reproduce import  falar_frase
from speech_rec import ouvir_microfone

def main():
    frase = ouvir_microfone()
    falar_frase(frase)
    return

if __name__ == "__main__":
    main()