import time
import pandas as pd
import re
import math
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class ScrapArmorThread(Thread):
    def __init__(self, type=39):
        Thread.__init__(self)
        self.df_armor = pd.DataFrame()
        self.type = type

        if self.type == 77:
            self.type = 75

    def generate_index_and_columns(self, driver):
        dimension_div = driver.find_element(By.CSS_SELECTOR, 'div.product.attribute.overview > div > strong')

        width_min, height_min, width_max, height_max = map(int, re.findall('\d+', dimension_div.text))

        index_list = [math.floor(i/10)*10 for i in range(height_min, height_max + 10, 10)]
        column_list = [math.floor(i/10)*10 for i in range(width_min, width_max + 10, 10)]
        
        index_list[0] = height_min
        index_list.append(height_max)
        
        return index_list, column_list

    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get(f'https://www.leroidelafenetre.fr/lames-alu-{self.type}-mm-livrees-assemblees-en-tablier-complet.html')
        
        driver.maximize_window()
        time.sleep(5)

        width_input = driver.find_element(By.CSS_SELECTOR, 'input#configurator-width')
        height_input = driver.find_element(By.CSS_SELECTOR, 'input#configurator-height')

        index_list, column_list = self.generate_index_and_columns(driver)

        for index in index_list:
            height_input.send_keys(Keys.CONTROL, 'a')
            height_input.send_keys(index)
            height_input.send_keys(Keys.TAB)

            WebDriverWait(driver, 10).until_not(
                ec.element_to_be_clickable((driver.find_element(By.CSS_SELECTOR, 'div[data-role="loader"]')))
            )   

            for column in column_list:
                width_input.send_keys(Keys.CONTROL, 'a')
                width_input.send_keys(column)
                width_input.send_keys(Keys.TAB)

                WebDriverWait(driver, 10).until_not(
                    ec.element_to_be_clickable((driver.find_element(By.CSS_SELECTOR, 'div[data-role="loader"]')))
                )

                time.sleep(1)

                error = driver.find_elements(By.CSS_SELECTOR, 'div.message.error')

                if len(error) > 0:
                    break
                
                price_place = driver.find_element(By.CSS_SELECTOR, 'div[class="product-info-price cs-buybox__price"] > div > span > span > span.price')
                
                if index == index_list[-1] and index % 10 == 9:
                    index = index + 1
    
                self.df_armor.loc[index*10, column*10] = re.findall(r'\d\s?\d+,\d+', price_place.text)[0].replace('\u202f', '')
        
        driver.quit()
