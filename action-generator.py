from pynput.mouse import Button, Controller
from pynput import keyboard
import json

mouse = Controller()
actions = []

def on_press(key):
    pass

def on_release(key):
    if str(key) in ("Key.ctrl_l", "Key.ctrl"):
        actions.append({"mouse": True, "pos": [mouse.position[0], mouse.position[1]], "delay": 1})
        print("Action added! ({}, {})".format(mouse.position[0], mouse.position[1]))
    elif str(key) in ("Key.alt_l", "Key.alt"):
        with open("generated_action.json", "w") as file:
            json.dump({"result":actions}, file, indent=1)
        print("Program finished. Actions added: ", len(actions))
        return False
    elif str(key) == "Key.ctrl_r":
        actions.append({"mouse": False, "chars": "", "delay": 1})
        print("Keyboard command added!")

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
