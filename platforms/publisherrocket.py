from pynput.mouse import Button, Controller
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController
from time import sleep
import os

import json

config = json.load(open("config.json"))

class PublisherRocket:

    def __init__(self, actions):
        self.mouse = Controller()
        self.keyboard = KeyboardController()
        self.actions = actions
        self.compileActions(self.actions["init"])

    def search(init, keywords):
        self.compileActions(self.actions["search"], chars={"keywords": keywords})
        # gestione del file scaricato
        pass

    def compileActions(self, actions : list, chars = {}):
        for action in actions:
            if action["mouse"]:
                self.mouse.position = action["pos"]
                self.mouse.press(Button.left)
                self.mouse.release(Button.left)
            else:
                text = chars[action["chars"]]
                for char in text:
                    self.keyboard.press(char)
                    self.keyboard.release(char)
            sleep(action["delay"])
