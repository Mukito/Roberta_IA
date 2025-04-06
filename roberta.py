import os
import random
import subprocess
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import pygame
from pydub.generators import Sine
from pydub import AudioSegment
from datetime import datetime
import locale
import difflib
#from acoes import obter_hora, obter_dia, abrir_youtube  # importa ações separadas
from acoes import obter_hora, obter_dia, abrir_youtube, abrir_chrome, abrir_spotify
import time  # lá no topo, se ainda não tiver


# Inicializações
reconhecedor = sr.Recognizer()
motor_voz = pyttsx3.init()

# Voz em português
for voz in motor_voz.getProperty('voices'):
    if "pt" in voz.languages or "brazil" in voz.name.lower():
        motor_voz.setProperty('voice', voz.id)
        break

ativadores = ["roberta", "ei roberta", "roberta querida", "roberta me escuta"]

# Gera bip se não existir
def gerar_bip():
    if not os.path.exists("bip.wav"):
        print("Gerando bip.wav...")
        bip = Sine(1000).to_audio_segment(duration=300) # 1000 Hz por 300 ms
        bip = bip - 6  # reduz volume em 6 decibéis (~metade)
        bip.export("bip.wav", format="wav")
        time.sleep(0.5)

# Toca som de ativação
def tocar_bip():
    pygame.mixer.init()
    pygame.mixer.music.load("bip.wav")
    pygame.mixer.music.play()

# Fala com voz
def falar(texto):
    motor_voz.say(texto)
    motor_voz.runAndWait()
    #time.sleep(1.5)

# Ouve do microfone
def ouvir():
    with sr.Microphone() as source:
        print("Aguardando comando...")
        audio = reconhecedor.listen(source)
        try:
            texto = reconhecedor.recognize_google(audio, language="pt-BR")
            print("Você disse:", texto)
            return texto.lower()
        except sr.UnknownValueError:
            falar("Desculpe, não entendi.")
            return ""
        except sr.RequestError:
            print("Erro na conexão com o serviço de reconhecimento.")
            falar("Estou com problemas para me conectar.")
            return ""

#def ouvir():
#    return input("Digite o comando simulado: ")



# Lê comandos do arquivo
def carregar_comandos():
    comandos = {}
    try:
        with open("comandos.txt", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if ":" in linha:
                    pergunta, resposta = linha.strip().split(":", 1)
                    comandos[pergunta.lower()] = resposta
    except FileNotFoundError:
        pass
    return comandos

# Conta piada aleatória
def contar_piada():
    try:
        with open("piadas.txt", "r", encoding="utf-8") as arquivo:
            piadas = [linha.strip() for linha in arquivo if linha.strip()]
        if piadas:
            return random.choice(piadas)
    except FileNotFoundError:
        return "Não encontrei o arquivo de piadas."
    return "Não tenho piadas no momento."

# Processa comandos
def processar_comando(comando):
    from acoes import obter_hora, obter_dia, abrir_youtube
    comandos = carregar_comandos()

    if "piada" in comando:
        falar(contar_piada())
        return

    if "abrir chrome" in comando:
        subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        falar("Abrindo o Chrome.")
        return

    if "abrir spotify" in comando:
        subprocess.Popen("C:\\Users\\Master\\AppData\\Roaming\\Spotify\\Spotify.exe")
        falar("Abrindo o Spotify.")
        return

    if "youtube" in comando:
        partes = comando.split("youtube")
        if len(partes) > 1:
            pesquisa = partes[1].strip()
            falar(abrir_youtube(pesquisa))
        else:
            falar("O que você quer que eu procure no YouTube?")
        return

    for pergunta in comandos:
        if pergunta.lower() in comando.lower():
            resposta = comandos[pergunta]
            if "{hora}" in resposta:
                resposta = resposta.replace("{hora}", obter_hora())
            if "{dia}" in resposta:
                resposta = resposta.replace("{dia}", obter_dia())
            falar(resposta)
            return
    
    # Tenta encontrar algo parecido se não encontrou exatamente
    possiveis_chaves = list(comandos.keys())
    parecidas = difflib.get_close_matches(comando, possiveis_chaves, n=1, cutoff=0.6)

    if parecidas:
        resposta = comandos[parecidas[0]]
        if "{hora}" in resposta:
            resposta = resposta.replace("{hora}", obter_hora())
        if "{dia}" in resposta:
            resposta = resposta.replace("{dia}", obter_dia())
        falar(resposta)
        return

    falar("Desculpe, ainda não sei fazer isso.")
