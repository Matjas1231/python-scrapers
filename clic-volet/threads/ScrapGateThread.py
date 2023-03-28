import time
import pandas as pd
import re
import math
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By

class ScrapGatehread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.df_gate = pd.DataFrame()

    def run(self):        
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://clic-volet.fr/configurateurs/9839-porte-de-garage-enroulable-sur-mesure.html')
        time.sleep(1)
        driver.maximize_window()
        time.sleep(1)

        width_input = driver.find_element(By.CSS_SELECTOR, 'input#porte_garage_castellane--dimensions_tableau--largeur_tableau')
        height_input = driver.find_element(By.CSS_SELECTOR, 'input#porte_garage_castellane--dimensions_tableau--hauteur_tableau')

        width_min = int(width_input.get_attribute('min'))
        width_max = int(width_input.get_attribute('max'))

        height_min = int(height_input.get_attribute('min'))
        height_max = int(height_input.get_attribute('max'))

        index_list = [math.floor(i/100)*100 for i in range(height_min, height_max + 100, 100)]
        column_list = [math.floor(i/100)*100 for i in range(width_min, width_max + 100, 100)]
        index_list[0] = height_min
        column_list[0] = width_min

        price_place = driver.find_element(By.CSS_SELECTOR, 'span#prix_final')

        old_price = ''
        for index in index_list:
            height_input.clear()
            height_input.send_keys(index)
            for column in column_list:
                width_input.clear()
                width_input.send_keys(column)
                height_input.click()
                time.sleep(1)
                
                if not price_place.text:
                    break

                price = re.findall(r'\d+,?\d+.\d+', price_place.text)[0]
                i = 0
                while old_price == price:
                    height_input.clear()
                    height_input.send_keys(index)
                    time.sleep(1)

                    width_input.clear()
                    width_input.send_keys(column)
                    height_input.click()
                    time.sleep(1)

                    price = re.findall(r'\d+,?\d+.\d+', price_place.text)[0]
                    print(f'Pętla - cena {price}')

                    if price != old_price or i > 1:
                        break
                    i += 1

                old_price = price

                print(f'Szerokość: {column} x Wysokość: {index} - cena: {price}')
                self.df_gate.loc[index, column] = price.replace(',', '').replace('.', ',')
      

