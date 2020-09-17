from pynput.mouse import Button, Controller
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController
from time import sleep
import os

class GoogleKeywordPlanner:

    def __init__(self, config, actions):
        self.config = config
        self.mouse = Controller()
        self.keyboard = KeyboardController()
        self.actions = actions

    def search(self, keywords):
        keywords_text = ""
        for keyword in keywords:
            keywords_text += ", {}".format(keyword)
        self.compileActions(self.actions["search_gkp"], chars={"keywords": keywords_text, "url": self.config["gkp_url"]})
        sleep(10)
        for file in os.listdir(self.config["output"]):
            if file.startswith("Keyword Stats"):
                os.rename("{}/{}".format(config["output"], file), "{} gkp.csv".format(keywords_text[2:]))
                break
        print("(GKP) keywords extracted.")

    def compileActions(self, actions : list, chars = {}):
        for action in actions:
            print("doing something")
            if action["mouse"]:
                self.mouse.position = action["pos"]
                self.mouse.press(Button.left)
                self.mouse.release(Button.left)
            else:
                text = chars[action["chars"]]
                for char in text:
                    self.keyboard.press(char)
                    self.keyboard.release(char)
                if "url" in chars:
                    self.keyboard.press(Key.enter)
                    sleep(20)
            sleep(action["delay"])
