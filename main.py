from roberta import ouvir, falar, processar_comando, ativadores, tocar_bip, gerar_bip
import time
import random

# Gera o bip na inicialização
gerar_bip()

respostas_padrao = [
    "Oi, estou ouvindo. Pode dizer o que deseja?",
    "Sim, diga.",
    "Estou pronta, pode falar!",
    "Diga o que você quer que eu faça.",
    "Pode falar, estou escutando!"
]


# Loop principal
while True:
    comando = ouvir()

    # Se não ouviu nada, volta pro início do loop
    if not comando:
        continue

    comando = comando.lower()  # Deixa tudo em minúsculas pra comparar melhor

    # Verifica se chamou a Roberta
    if any(ativador in comando for ativador in ativadores):
        tocar_bip()
        time.sleep(0.3)

        # Remove o ativador da frase
        for ativador in ativadores:
            comando = comando.replace(ativador, "")
        comando = comando.strip()

        # Se não falou mais nada, Roberta tenta ouvir até 2 vezes
        tentativas = 0
        while not comando and tentativas < 2:
            falar(random.choice(respostas_padrao))
            time.sleep(0.5)
            comando = ouvir()
            comando = comando.lower() if comando else ""
            tentativas += 1

        # Espera o comando verdadeiro
        if not comando:
            print("Nada foi dito. Voltando a esperar ativação...\n")
            continue
        
        # Verifica se o comando é para encerrar
        if "sair" in comando or "parar" in comando:
            falar("Até logo!")
            break

        # Processa o comando normalmente
        processar_comando(comando)
    else:
        print("Aguardando a palavra mágica...")
