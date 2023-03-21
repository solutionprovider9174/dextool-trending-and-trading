# Implementation of Selenium WebDriver with Python using PyTest

import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.proxy import Proxy, ProxyType
import threading

PAIR = "0xa8dfebeb90f8e148b6a3c611758ea63703ab02c1"


URL = "https://www.dextools.io/app/en/ether"
DRIVER = "D:\chromedriver.exe"
EXTENSION_PATH1 = R"C:\Users\SevenStar\AppData\Local\Google\Chrome\User Data\Default\Extensions\nkbihfbeogaeaoehlefnkodbefgpgknn\10.25.0_0.crx"
global chrome_driver
global action

class ScrapeThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        def start():
            while True:
                prox = Proxy()
                prox.proxy_type = ProxyType.MANUAL
                prox.http_proxy = "http://solution333:success333_streaming-1@geo.iproyal.com:12321"
                prox.ssl_proxy = "http://solution333:success333_streaming-1@geo.iproyal.com:12321"
                capabilities = webdriver.DesiredCapabilities.CHROME
                prox.add_to_capabilities(capabilities)
                service = DRIVER
                chrome_options = Options()
                chrome_options.add_argument("start-maximized")
                chrome_options.add_extension(EXTENSION_PATH1)
                chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')

                global chrome_driver
                chrome_driver = webdriver.Chrome(
                    executable_path=service, chrome_options=chrome_options, desired_capabilities=capabilities)

                
                global action
                action = ActionChains(chrome_driver)

                try:
                    new_session()
                except Exception as e:
                    print(e)


        def new_session():
            chrome_driver.get(URL)
            sleep(3)
            chrome_driver.switch_to.window(chrome_driver.window_handles[0])
            close_button = WebDriverWait(chrome_driver, timeout=100).until(
                lambda d: d.find_element(By.CLASS_NAME, "close"))
            print("click close button")
            action.move_to_element_with_offset(close_button, 0, 0)
            action.click()
            action.perform()
            trending_dextools()

            chrome_driver.quit()   


        def trending_dextools():

            # search-contrainer
            search_contrainer = WebDriverWait(chrome_driver, timeout=100).until(
                lambda d: d.find_element(By.CLASS_NAME, "search-container"))
            print("click search container")
            action.move_to_element_with_offset(search_contrainer, 0, 0)
            action.click()
            action.perform()
            sleep(3)

            # pair input
            pair_input = WebDriverWait(chrome_driver, timeout=100).until(
                lambda d: d.find_element(By.CLASS_NAME, "search-pairs"))
            print("input pair")
            pair_input.send_keys(PAIR)
            sleep(1)

            # found pair click
            found_pair = WebDriverWait(chrome_driver, timeout=100).until(
                lambda d: d.find_element(By.CLASS_NAME, "search-result-item"))
            print("found pair")
            action.move_to_element_with_offset(found_pair, 0, 0)
            action.click()
            action.perform()
            sleep(5)

            try:
                # favorite button
                favorite_button = WebDriverWait(chrome_driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "favorite-button")))
                print("favorite button click")
                action.move_to_element_with_offset(favorite_button, 0, 0)
                action.click()
                action.perform()
                sleep(1)

                # search token button
                search_token_button = WebDriverWait(chrome_driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-token-button")))
                print("search token button click")
                action.move_to_element_with_offset(search_token_button, 0, 0)
                action.click()
                action.perform()
                sleep(2)

                # close search token panel
                pairs_search_container = WebDriverWait(chrome_driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pairs-search-container")))
                close_button = pairs_search_container.find_element(
                    By.CLASS_NAME, "close")
                print("close search token panel")
                action.move_to_element_with_offset(close_button, 0, 0)
                action.click()
                action.perform()
                sleep(2)
            except Exception as e:
                print(e)

            try:
                # social container
                social_container = WebDriverWait(chrome_driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "social-container")))
                print("found social container")
                socials = social_container.find_elements(By.TAG_NAME, "a")
                print(len(socials))
                sleep(1)
                try:
                    # share button click
                    action.move_to_element_with_offset(socials[0], 0, 0)
                    action.click()
                    action.perform()
                    sleep(1)

                    # share info block
                    share_info_block = WebDriverWait(chrome_driver, 100).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "share-btn")))
                    print("found share info block")
                    share_infos = share_info_block.find_elements(By.TAG_NAME, "a")
                    # share buttons click
                    for share_info in share_infos:
                        action.move_to_element_with_offset(share_info, 0, 0)
                        action.click()
                        action.perform()
                        sleep(1)

                    # close button click
                    share_info_panel = WebDriverWait(chrome_driver, 100).until(
                        EC.presence_of_element_located((By.TAG_NAME, "app-social-media-modal")))
                    close_button = share_info_panel.find_element(
                        By.CLASS_NAME, "close")
                    print("close share modal")
                    action.move_to_element_with_offset(close_button, 0, 0)
                    action.click()
                    action.perform()
                    sleep(1)
                except Exception as e:
                    print(e)

                SOCIALS = ["share", "etherscan", "web", "telegram",
                        "twitter", "coingecko", "???", "????", "???", "???", "????"]
                for i in range(1, len(socials)-1):
                    print("{} click".format(SOCIALS[i]))
                    action.move_to_element_with_offset(socials[i], 0, 0)
                    action.click()
                    action.perform()
                    sleep(1)
                    chrome_driver.switch_to.window(chrome_driver.window_handles[0])

            except Exception as e:
                print(e)


            sleep(2)


        start()

threads = []
for num in range(2):
    t = ScrapeThread(URL)
    t.start()
    threads.append(t)

for t in threads:
    t.join()