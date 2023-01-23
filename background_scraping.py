from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

movie_list = ['Fight Club']

option = Options()
option.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

for movie in movie_list:
    driver.get("https://www.google.com/")
    print(driver.find_element('xpath', '/html/body/div[1]/div[1]/div/div/div/div[1]/div/div[1]/a').text)