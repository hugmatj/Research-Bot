from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException, InvalidArgumentException
from bs4 import BeautifulSoup
import imaplib
import email
from email.header import decode_header
import webbrowser
from time import sleep
import json
import os

# get config
config = json.load(open("config.json"))

# setting up options
options = Options()
options.add_experimental_option("prefs", {"download.default_directory" : config["output"]})
#options.add_argument("--headless")

class GoogleKeywordPlanner:
    options = Options()

    def __init__(self):
        username = "thomasegiacomoselfpublishing@gmail.com"
        password = "Proposte2019"
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

class KWFinder:

    def __init__(self, credentials):
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

class JungleScout:
    items = 0
    doneItems = 0

    def __init__(self, credentials):
        # setup email
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.login(config["GKP"]["email"], config["GKP"]["password"])
        status, messages = self.imap.select("INBOX")
        messages = int(messages[0])
        self.newMessages = []
        for i in range(messages, messages-10, -1):
            self.newMessages.append(str(i))

        # setup browser
        self.browser = webdriver.Chrome(config["chromedriver_path"], options=options)
        self.browser.set_window_size(1280, 720)
        self.browser.get("https://members.junglescout.com/login")
        while True:
            try:
                self.browser.find_element_by_xpath("//*[@id=\"root\"]/div/div[1]/div/div/div/div[2]/input[1]").send_keys(credentials["email"])
                break
            except NoSuchElementException:
                sleep(0.5)
        self.browser.find_element_by_xpath("//*[@id=\"root\"]/div/div[1]/div/div/div/div[2]/input[2]").send_keys(credentials["password"])
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

# controlla i caratteri speciali per ogni piattaforma.
# pulizia file marci alla fine di tutte le piattaforme

if __name__ == "__main__":
    # getting keywords
    keywords = open("keywords.txt").read().strip().split("\n")
    kwf = KWFinder(config["KWF"])
    js = JungleScout(config["JS"])
    for keyword in keywords:
        kwf.search(keyword)
        js.search(keyword)
