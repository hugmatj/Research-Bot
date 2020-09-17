from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException, InvalidArgumentException
from bs4 import BeautifulSoup
from time import sleep
import imaplib
import email
import os

class JungleScout:
    items = 0
    doneItems = 0

    def __init__(self, config, options):
        self.config = config
        # setup email
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.login(self.config["GKP"]["email"], self.config["GKP"]["password"])
        status, messages = self.imap.select("INBOX")
        messages = int(messages[0])
        self.newMessages = []
        for i in range(messages, messages-10, -1):
            self.newMessages.append(str(i))

        # setup browser
        self.browser = webdriver.Chrome(self.config["chromedriver_path"], options=options)
        self.browser.set_window_size(1280, 720)
        self.browser.get("https://members.junglescout.com/login")
        while True:
            try:
                self.browser.find_element_by_xpath("//*[@id=\"root\"]/div/div[1]/div/div/div/div[2]/input[1]").send_keys(self.config["JS"]["email"])
                break
            except NoSuchElementException:
                sleep(0.5)
        self.browser.find_element_by_xpath("//*[@id=\"root\"]/div/div[1]/div/div/div/div[2]/input[2]").send_keys(self.config["JS"]["password"])
        url = self.browser.current_url
        self.browser.find_element_by_xpath("//*[@id=\"root\"]/div/div[1]/div/div/div/div[2]/div/button").click()
        while url == self.browser.current_url:
            try:
                self.browser.find_element_by_xpath("//*[@id=\"root\"]/div/div[1]/div/div/div/div[2]/div/button").click()
            except (ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException):
                sleep(0.25)

    def search(self, keywords):
        self.getMails(keywords.lower())
        self.checkMails()

    def getMails(self, keywords):
        while True:
            self.browser.get("https://members.junglescout.com/#/keyword")
            try:
                connectionTest = self.browser.get("//*[@id=\"app-content\"]/div[2]/div/div/div[2]/h3")
                print(type(connectionTest.text))
                print("x{}x".format(connectionTest.text))
                print(connectionTest.text == "404")
                if connectionTest.text == "404":
                    self.browser.get("https://members.junglescout.com/")
                    continue
            except (NoSuchElementException, InvalidArgumentException):
                sleep(0.1)
            break

        while True:
            try:
                self.browser.find_element_by_xpath("//*[@id=\"app-content\"]/div[2]/div/div[2]/div[2]/div/div/span/input").send_keys(Keys.CONTROL, "a")
                self.browser.find_element_by_xpath("//*[@id=\"app-content\"]/div[2]/div/div[2]/div[2]/div/div/span/input").send_keys(keywords)
                break
            except NoSuchElementException:
                try:
                    elem = self.browser.find_element_by_xpath("//*[@id=\"app-content\"]/div[2]/div/div/div[2]/h3")
                    self.browser.get("https://members.junglescout.com/#/keyword")
                except NoSuchElementException:
                    sleep(0.5)

        self.browser.find_element_by_xpath("//*[@id=\"app-content\"]/div[2]/div/div[2]/div[2]/button").click()

        downloadConfirmed = True
        # download button
        while True:
            try:
                if downloadConfirmed:
                    # "Download CSV" button
                    self.browser.find_element_by_xpath("//*[@id=\"app-content\"]/div[2]/div/div[3]/div[3]/div/button").click()
                else:
                    break
                for _ in range(20):
                    sleep(0.5)
                    try:
                        confirm = self.browser.find_element_by_xpath("//*[@id=\"root\"]/div/div[2]/div/div/div")
                    except NoSuchElementException:
                        confirm = "error"
                    if confirm.text.startswith("When the CSV file is ready"):
                        downloadConfirmed = False
                        break
            except Exception as e:
                if isinstance(e, ElementClickInterceptedException):
                    try:
                        self.browser.find_element_by_xpath("//*[@id=\"_pendo_g_fkRG-UFEgcEBLPnYNRw7hpzcFgo\"]/div/div/div/a[2]").click()
                    except NoSuchElementException:
                        sleep(0.5)
                sleep(0.5)
        self.items += 1

    def checkMails(self):
        while self.doneItems != self.items:
            status, messages = self.imap.select("INBOX")
            messages = int(messages[0])

            for i in range(messages, messages-10, -1):
                res, msg = self.imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        if msg["From"].endswith("<hello@junglescout.com>") and msg["Subject"] == "Download link is ready for Keyword Scout" and not str(i) in self.newMessages:
                            self.newMessages.append(str(i))
                            body = msg.get_payload(decode=True).decode()
                            soup = BeautifulSoup(body, 'html.parser')
                            download_link = soup.find("a", attrs={"target": "_blank" ,"style": "color: #f57706;"}).text
                            self.browser.get(download_link)
                            self.doneItems += 1
                            if self.doneItems > self.items:
                                self.doneItems = self.items
            sleep(5)
        for file in os.listdir("output"):
            if file.startswith("Keyword_Scout"):
                keyword = open("output/{}".format(file)).read().strip().split("\n")[2][17:-1]
                os.rename("output/{}".format(file), "output/{} junglescout.csv".format(keyword))
                print("\"{}\" (junglescout) exported.".format(keyword))
