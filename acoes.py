from datetime import datetime
import locale
import webbrowser
import subprocess



def obter_hora():
    return datetime.now().strftime("%H:%M")

def obter_dia():
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
        except:
            pass
    hoje = datetime.now()
    dias_semana = hoje.strftime("%A")
    data_formatada = hoje.strftime("%d de %B de %Y")
    return f"{dias_semana}, {data_formatada}"

def abrir_youtube(pesquisa):
    if pesquisa:
        url = f"https://www.youtube.com/results?search_query={pesquisa.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Abrindo {pesquisa} no YouTube."
    else:
        return "O que você quer que eu procure no YouTube?"

def abrir_chrome():
    try:
        subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        return "Abrindo o Chrome."
    except Exception as e:
        return f"Não consegui abrir o Chrome: {e}"

def abrir_spotify():
    try:
        subprocess.Popen("C:\\Users\\Master\\AppData\\Roaming\\Spotify\\Spotify.exe")
        return "Abrindo o Spotify."
    except Exception as e:
        return f"Não consegui abrir o Spotify: {e}"
