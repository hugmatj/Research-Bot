from platforms.googlekeywordplanner import GoogleKeywordPlanner
from platforms.kwfinder import KWFinder
from platforms.junglescout import JungleScout
from platforms.publisherrocket import PublisherRocket

from selenium.webdriver.chrome.options import Options
import json
import os

# get config
config = json.load(open("config.json"))

# setting up options
options = Options()
options.add_experimental_option("prefs", {"download.default_directory" : config["output"]})
options.add_argument("user-data-dir=/home/andrei/.config/google-chrome")
#options.add_argument("--headless")

# controlla i caratteri speciali per ogni piattaforma.
# gestisci come passi config.json tra i vari moduli
# fixa il fatto che a volte non prende il tasto "search" (analogo al tasto Download CSV) su JungleScout
# sposta l'opzione del profilo di chrome soltanto alla classe di google keyword planner

platforms = ("kwfinder", "junglescout", "gkp", "publisher rocket (book)", "publisher rocket (ebook)")

def cleanFiles():
    for file in os.listdir(config["output"]):
        if not file.endswith(platforms):
            os.unlink("{}/{}".format(config["output"], file))
            print("\"{}\" cleaned.".format(file))
    print("File cleanup completed.")

def main():
    actions = json.load(open("actions.json"))
    keywords = open("keywords.txt").read().strip().split("\n")
    kwf = KWFinder(config, options)
    gkp = GoogleKeywordPlanner(config, options)
    js = JungleScout(config, options)
    pr = PublisherRocket(actions)
    for keyword in keywords:
        kwf.search(keyword)
        gkp.search(keyword)
        js.search(keyword)
        pr.search(keyword)
    cleanFiles()

if __name__ == "__main__":
    #main()
    # getting keywords
    #test = GoogleKeywordPlanner(options)
    actions = json.load(open("actions.json"))
    test = PublisherRocket(actions)
    #keywords = open("keywords.txt").read().strip().split("\n")
    #kwf = KWFinder(config["KWF"], options)
    #js = JungleScout(config["JS"], options)
    #for keyword in keywords:
    #    #kwf.search(keyword)
    #    js.search(keyword)
