from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException, InvalidArgumentException
from time import sleep
import pickle

import json

config = json.load(open("config.json"))

class GoogleKeywordPlanner:

    def __init__(self, options):
        self.browser = webdriver.Chrome(config["chromedriver_path"], options=options)
        #self.browser.get("https://stackoverflow.com/")
        self.browser.get("https://ads.google.com/intl/it_it/home/tools/keyword-planner/")
        #cookies = pickle.load(open("cookies.pkl", "rb"))
        #for cookie in cookies:
        #    self.browser.add_cookie(cookie)
        #print("cookies added.")
        #self.browser.refresh()
        #self.browser.get("https://www.youtube.com")
        #while True:
            #print("dumping cookies...")
            #with open("cookiestext.txt", "w") as file:
                #file.write(str(self.browser.get_cookies()))
            #pickle.dump(self.browser.get_cookies() , open("cookies.pkl","wb"))
            #sleep(5)

    def initialise(self):
        #self.browser = webdriver.Chrome("/home/andrei/Documenti/Lavori/keywords-bot/chromedriver", options=self.options)
        #self.browser.get("https://ads.google.com/aw/keywordplanner/ideas/new?ocid=537997864&euid=427576287&__u=8073802663&uscid=537997864&__c=8676706536&authuser=4&subid=it-it-ha-aw-bk-c-bau%21o3~CjwKCAjwnef6BRAgEiwAgv8mQfSEBgWYMw7_xcFhCa8EFKf8UdjckIT83dQGZ7Y9eS_j6t1C-oJSPhoC1VAQAvD_BwE~60200838689~")
        #loginButton = self.browser.find_element_by_xpath("//*[@id=\"gb_70\"]")
        #loginButton.click()

        #emailField = self.browser.find_element_by_xpath("//*[@id=\"identifierId\"]")
        #emailField.send_keys()

        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
        sleep(3)
        self.driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
        self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(3)
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
        sleep(2)
        self.driver.get('https://youtube.com')
        sleep(5)
