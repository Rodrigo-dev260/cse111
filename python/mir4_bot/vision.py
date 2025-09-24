import os, sys

def caminho_absoluto(relativo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativo)
    return os.path.join(os.path.abspath("."), relativo)

import cv2, numpy as np, pyautogui, os, sys

def caminho_absoluto(relativo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativo)
    return os.path.join(os.path.abspath("."), relativo)

def detectar_mob():
    template_path = caminho_absoluto('assets/mob_template.png')
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path, 0)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    if max_val > 0.8:
        pyautogui.press('1')

def detectar_morte():
    template_path = caminho_absoluto('assets/revive_button.png')
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path, 0)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val > 0.8
