import pyautogui, time

def verificar_hp():
    hp_pixel = pyautogui.pixel(100, 100)  # Ajuste conforme sua tela
    if hp_pixel[0] < 100:
        pyautogui.press('f1')  # Usa poção

def log_evento(msg):
    with open("log_bot.txt", "a") as log:
        log.write(f"{time.ctime()}: {msg}\n")
