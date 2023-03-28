import time
import pandas as pd
import re
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By

class ScrapGateThread(Thread):
    def __init__(self, type=55):
        Thread.__init__(self)
        self.df_gate = pd.DataFrame()
        self.type = type

    def get_link(self):
        link = ''
        if self.type == 55:
            link = 'https://www.discount-menuiserie.com/porte-de-garage/porte-de-garage-enroulable-potarol-55.htm'
        elif self.type == 77:
            link = 'https://www.discount-menuiserie.com/porte-de-garage/porte-de-garage-enroulable-potarol-77.htm'

        return link

    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get(self.get_link())
 
        driver.maximize_window()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, 'div#cookies > p > a').click()

        driver.find_element(By.CSS_SELECTOR, 'div#type-pose-1').click()

        diemension_div = driver.find_element(By.CSS_SELECTOR, 'div#panel-dimensions')

        width_input = diemension_div.find_element(By.CSS_SELECTOR, 'div.col-md-6 > div.form-group > input#largeur')
        width_diemension = diemension_div.find_element(By.CSS_SELECTOR, 'div.col-md-6 > div.form-group > input#largeur + small')
        width_min, width_max = map(int, re.findall(r'\d+', width_diemension.text))

        height_input = diemension_div.find_element(By.CSS_SELECTOR, 'div.col-md-6 > div.form-group > input#hauteur')
        height_diemension = diemension_div.find_element(By.CSS_SELECTOR, 'div.col-md-6 > div.form-group > input#hauteur + small')
        height_min, height_max = map(int, re.findall(r'\d+', height_diemension.text))

        column_list = [i for i in range(width_min, width_max + 100, 100)]
        index_list = [i for i in range(height_max, height_max + 100, 100)]

        index_list[-1] = height_max

        width_input.send_keys(width_min)
        height_input.send_keys(height_min)
        width_input.click()

        driver.find_element(By.CSS_SELECTOR, 'img[src*="blanc"]').click()

        driver.find_elements(By.CSS_SELECTOR, 'div#config-couleur > div.card-body > div.row > div')[0].click()

        if self.type == 55:
            driver.find_elements(By.CSS_SELECTOR, 'div#config-motorisation > div.card-body > div.row.center > div')[0].click()
        elif self.type == 77:
            driver.find_element(By.CSS_SELECTOR, 'div#option-lame-0').click()
            driver.find_element(By.CSS_SELECTOR, 'div#type-motorisation-1').click()

        for index in index_list:
            height_input.clear()
            height_input.send_keys(index)
            for column in column_list:
                width_input.clear()
                width_input.send_keys(column)
                height_input.click()
                time.sleep(0.5)
                price_place = driver.find_element(By.XPATH, '//div[@id="description"]/div/p[contains(text(), "total")]')
                print(f'Szerokość: {column} x wysokość: {index} - cena: {price_place.text}')

                price = re.findall(r'\d+,?\d+\.\d+', price_place.text)[0].replace(',', '').replace('.', ',')
                self.df_gate.loc[index, column] = price
