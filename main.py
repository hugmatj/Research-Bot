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
#options.add_argument("--headless")

# controlla i caratteri speciali per ogni piattaforma.
# pulizia file marci alla fine di tutte le piattaforme
# gestisci come passi config.json tra i vari moduli
# fixa il fatto che a volte non prende il tasto "search" (analogo al tasto Download CSV) su JungleScout

if __name__ == "__main__":
    # getting keywords
    #test = GoogleKeywordPlanner(options)
    keywords = open("keywords.txt").read().strip().split("\n")
    #kwf = KWFinder(config["KWF"], options)
    js = JungleScout(config["JS"], options)
    for keyword in keywords:
        #kwf.search(keyword)
        js.search(keyword)
