from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

# Scrapping usando o selenium para buscar imagens no google
# Source: https://levelup.gitconnected.com/how-to-download-google-images-using-python-2021-82e69c637d59

#Opens up web driver and goes to Google Images
path = os.path.dirname(__file__)
driver = webdriver.Chrome(f'{path}\\..\\resources\\chromedriver_win32\\chromedriver.exe')
driver.get('https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl')

box = driver.find_element_by_xpath('//*[@id="APjFqb"]') # XPATH da barra de busca

champ = "lux"
query = "league of legends " + champ
box.send_keys(query)
box.send_keys(Keys.ENTER)

for i in range(1, 50):
    try:
        elemento = driver.find_element_by_xpath(f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img')
        dir = f'{path}\\images\\{champ}'
        if not os.path.exists(dir):
            os.makedirs(dir)
        elemento.screenshot(f'{dir}\\{i}.png')
    except:
        pass

