import interception
import keyboard
import time


interception.auto_capture_devices()

def clique_esquerdo():
    interception.click(button="left")
    print("[INFO] Clique esquerdo enviado")

def mover_para(x, y):
    print(f"[INFO] Movendo o mouse para ({x}, {y})")
    interception.move_to(x, y)

def escutar():
    # print("[INFO] Pressione R (F1), T (clique), E (mover), ESC (sair)")
    while True:
        if keyboard.is_pressed("r"):
            interception.press("r")
            time.sleep(0.2)
        elif keyboard.is_pressed("2"):
            interception.press("2")
            time.sleep(0.0009)
            clique_esquerdo()
            time.sleep(0.2)
        # elif keyboard.is_pressed("e"):
        #     mover_para(835, 774)
        #     time.sleep(0.2)

if __name__ == "__main__":

    escutar()