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
        sleep(3)
        for file in os.listdir(self.config["output"]):
            if file.startswith("Keyword Stats"):
                os.rename("{}/{}".format(self.config["output"], file), "{}/{} gkp.csv".format(self.config["output"], keywords_text[2:]))
                break
        print("(GKP) keywords extracted.")

    def click(self):
        self.mouse.press(Button.left)
        sleep(0.25)
        self.mouse.release(Button.left)

    def compileActions(self, actions : list, chars = {}):
        for action in actions:
            if action["mouse"]:
                self.mouse.position = action["pos"]
                self.click()
            else:
                text = chars[action["chars"]]
                for char in text:
                    self.keyboard.press(char)
                    self.keyboard.release(char)
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
            sleep(action["delay"])
