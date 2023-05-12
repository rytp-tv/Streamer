from selenium import webdriver
import os
import chromedriver_autoinstall
import time

PATH = "./chromedriver"
URL = "https://github.com/RoastSea8/chromedriver-autoinstaller"

def main():
    chromedriver_autoinstall.install()
    # os.chmod('./chromedriver', 0o755) # MacOS only
    driver = webdriver.Chrome(PATH)
    driver.get(URL)
    time.sleep(1000)
