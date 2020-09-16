from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException, InvalidArgumentException
from time import sleep
import os

import json

config = json.load(open("config.json"))

class KWFinder:

    def __init__(self, credentials, options):
        self.browser = webdriver.Chrome(config["chromedriver_path"], options=options)
        self.browser.set_window_size(1280, 720)
        self.browser.get("https://kwfinder.com")
        while True:
            try:
                self.browser.find_element_by_xpath("//*[@id=\"mg-main-nav\"]/ul/li[4]/a").click()
                break
            except (NoSuchElementException, ElementClickInterceptedException):
                sleep(0.5)
        while True:
            try:
                self.browser.find_element_by_xpath("//*[@id=\"user_email\"]").send_keys(credentials["email"])
                break
            except NoSuchElementException:
                sleep(0.5)
        self.browser.find_element_by_xpath("//*[@id=\"user_password\"]").send_keys(credentials["password"])
        self.browser.find_element_by_xpath("//*[@id=\"new_user\"]/div[4]/button").click()
        while self.browser.current_url != "https://app.kwfinder.com/":
            pass

    def search(self, keywords):
        keywords = keywords.lower()
        if self.browser.current_url != "https://app.kwfinder.com/":
            self.browser.get("https://app.kwfinder.com/")

        # keywords
        while True:
            try:
                self.browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div/div[2]/form/div/input").send_keys(keywords)
                break
            except NoSuchElementException:
                sleep(0.5)

        # region
        self.browser.find_element_by_xpath("//*[@id=\"rw_1_input\"]/div/div").click()
        while True:
            try:
                self.browser.find_element_by_xpath("//*[@id=\"rw_1_listbox\"]/li[2]/span/span[1]/span[2]").click()
                break
            except (NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException):
                sleep(0.5)

        # language
        self.browser.find_element_by_xpath("//*[@id=\"rw_2_input\"]/div/div").click()
        while True:
            try:
                sleep(1)
                self.browser.find_element_by_xpath("//*[contains(text(), 'English')]").click()
                sleep(1)
                break
            except (NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException):
                sleep(0.5)

        # submit
        self.browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div/div[2]/form/div/div/button").click()

        while True:
            try:
                self.browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div[1]/div[4]/div[2]/div/div[1]/div[1]/div/input").click()
                break
            except NoSuchElementException:
                sleep(0.5)
        self.browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div[1]/div[5]/div[3]/div/button").click()
        self.browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div[1]/div[5]/div[3]/div/aside/ul/li[2]/button").click()
        outputFile = "output/kwfinder_{}_export.csv".format(self.underscore(keywords))
        while not os.path.isfile(outputFile):
            pass
        os.rename(outputFile, "output/{} kwfinder.csv".format(keywords))
        print("\"{}\" (KWFinder) exported.".format(keywords))

    def underscore(self, text):
        newText = ""
        for char in text:
            if char == " ":
                newText += "_"
            else:
                newText += char
        return newText
