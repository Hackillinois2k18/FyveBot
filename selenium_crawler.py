import unittest
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



class SeleniumScrape:

    def run(self, vidId):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)

        driver.get("https://www.youtube.com/watch?v={}".format(vidId))
        #mute video
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='ytp-mute-button ytp-button']"))).click()

        # clicks more options dropdown on video
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch[1]/div[2]/div[2]/div[1]/div[6]/div[2]/ytd-video-primary-info-renderer[1]/div[1]/div[1]/div[3]/div[1]/ytd-menu-renderer[1]/button[1]/yt-icon[1]"))).click()

        #clicks opentranscripts and clears timestamps
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//yt-formatted-string[@class='style-scope ytd-menu-service-item-renderer'][contains(text(),'Open transcript')]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch[1]/div[2]/div[2]/div[1]/ytd-transcript-loader[1]/div[1]/ytd-transcript-renderer[1]/div[1]/ytd-transcript-header-renderer[1]/div[1]/ytd-menu-renderer[1]/button[1]/yt-icon[1]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/ytd-app[1]/ytd-popup-container[1]/iron-dropdown[1]/div[1]/ytd-menu-popup-renderer[1]/paper-menu[1]/div[1]/ytd-menu-service-item-renderer[1]/yt-formatted-string[1]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch[1]/div[2]/div[2]/div[1]/ytd-transcript-loader[1]/div[1]/ytd-transcript-renderer[1]/div[2]/ytd-transcript-body-renderer[1]"))).click()

        #grabs transcript from the video
        text = driver.find_element_by_xpath("/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch[1]/div[2]/div[2]/div[1]/ytd-transcript-loader[1]/div[1]/ytd-transcript-renderer[1]/div[2]/ytd-transcript-body-renderer[1]").text

        transcriptRaw = open('raw_transcript.txt', 'w')
        transcriptRaw.write(text)
        transcriptRaw.close()
        driver.close()
