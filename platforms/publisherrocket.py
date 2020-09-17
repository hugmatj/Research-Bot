from pynput.mouse import Button, Controller
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController
from time import sleep
import subprocess
import os

class PublisherRocket:

    def __init__(self, config, actions):
        self.config = config
        self.mouse = Controller()
        self.keyboard = KeyboardController()
        self.actions = actions

    def search(self, keywords):
        subprocess.call(self.config["pr_path"], shell=True)
        sleep(15)
        self.compileActions(self.actions["search_pr"], chars={"keyword": keywords, "directory": self.config["output"], "filename_1": "{} publisher rocket (book).csv".format(keywords), "filename_2": "{} publisher rocket (ebook).csv".format(keywords)})

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
