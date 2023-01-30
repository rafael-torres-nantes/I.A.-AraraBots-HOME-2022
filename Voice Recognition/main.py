from voice_recognition import ouvir_microfone
from voice_emulation import  falar_frase

def main():
    frase = ouvir_microfone()
    falar_frase(frase)
    return

if __name__ == "__main__":
    main()