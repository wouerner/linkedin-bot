import os
import random
import ssl
import time
from datetime import datetime, timedelta
from typing import Optional

import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from selenium_stealth import stealth
# from seleniumwire import webdriver

from selenium import webdriver

import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import logging

logging.basicConfig(level=logging.INFO)  # Main app runs at DEBUG level
logger = logging.getLogger('seleniumwire')
logger.setLevel(logging.ERROR)  # Run selenium wire at ERROR level

nltk.download("punkt")
nltk.download("stopwords")

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def get_chromedriver(use_proxy=False, user_agent=None):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    chrome_options.add_argument("--user-data-dir=/home/seluser/selenium") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data


    driver = webdriver.Remote(
            command_executor='http://localhost:4444',
            options=chrome_options
        )

    driver.maximize_window()
    return driver

def login(driver):

    url = f"https://www.linkedin.com/login"
    print('url: ', url)

    driver = get_chromedriver(use_proxy=False)

    driver.get(url)
    time.sleep(3)

    user = driver.find_element(By.ID, "username")

    print('user: ', user)
    user.send_keys("")

    time.sleep(2)

    password = driver.find_element(By.ID, "password")
    print('pass: ', password)

    password.send_keys("")
    time.sleep(2)

    btn = driver.find_element(By.CLASS_NAME, "login__form_action_container")
    print('btn: ', btn)

    time.sleep(5)
    btn.click()
    time.sleep(35)

    return driver

def getScraper() -> Optional[str]:

    # search = driver.find_element(By.ID, "global-nav-typeahead")
    # search = search.find_element(By.TAG_NAME, "input")

    # search.click()

    # search.send_keys("#soujunior")

    # search.send_keys(Keys.ENTER)

    # print('search: ', search)

    # time.sleep(5)


    driver = get_chromedriver(use_proxy=False)

    SEARCH_URL = 'https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=%23soujunior&origin=FACETED_SEARCH&sid=!wW&sortBy=%22date_posted%22'
    driver.get(SEARCH_URL)

    time.sleep(30)

    # html
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    container = soup.find_all("div", class_="feed-shared-social-action-bar feed-shared-social-action-bar--full-width feed-shared-social-action-bar--has-identity-toggle feed-shared-social-action-bar--has-social-counts")

    list_buttons = [] 

    for l in container:
        print('user: ', l.find("button", class_="content-admin-identity-toggle-button").get('id'))
        print('like: ', l.find("button", class_="react-button__trigger").get('id'))

        list_buttons.append({ 
                             'like': l.find("button", class_="react-button__trigger").get('id'),
                             'user': l.find("button", class_="content-admin-identity-toggle-button").get('id'),
                             })

    print('list: ', list_buttons)

    time.sleep(2)

    for id in list_buttons:

        profile = driver.find_element(By.ID, id['user'])
        profile.click()

        time.sleep(2)

        profile = profile.find_element(By.XPATH, "//img[@alt='Logo da empresa SouJunior']")

        time.sleep(1)
        profile.click()

        save = driver.find_element(By.CLASS_NAME, "artdeco-modal__actionbar")
        save = save.find_element(By.TAG_NAME, "button")

        save.click()

        # search = driver.find_element(By.ID, id['user'])
        # search.click()

        time.sleep(2)
        search = driver.find_element(By.ID, id['like'])
        search.click()

    time.sleep(5)

    driver.quit()
    return

getScraper()
