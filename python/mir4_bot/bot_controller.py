import pyautogui, time, math, random
from vision import detectar_mob, detectar_morte
from utils import verificar_hp, log_evento

ativo = True

def iniciar_bot(habilidades, tempo_total):
    global ativo
    inicio = time.time()
    while ativo and time.time() - inicio < tempo_total:
        if detectar_morte():
            pyautogui.click(960, 540)  # Clica no botão de reviver
            time.sleep(5)
            log_evento("Personagem reviveu")
        mover_em_circulo(habilidades)
        detectar_mob()
        verificar_hp()
        log_evento("Loop executado")

def parar_bot():
    global ativo
    ativo = False

def mover_em_circulo(habilidades):
    centro_x, centro_y, raio, passos = 960, 540, 150, 36
    for i in range(passos):
        x = centro_x + raio * math.cos(2 * math.pi * i / passos)
        y = centro_y + raio * math.sin(2 * math.pi * i / passos)
        pyautogui.moveTo(x, y, duration=0.05)
        pyautogui.press('space')
        if random.random() < 0.3:
            pyautogui.press(random.choice(habilidades))
        time.sleep(0.2)
