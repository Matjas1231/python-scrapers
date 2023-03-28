import time
import pandas as pd
import re
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class ScrapGatehread(Thread):
    def __init__(self, type=55):
        Thread.__init__(self)
        self.df_gate = pd.DataFrame()
        self.type = type

    def run(self):        
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://priximbattable.net/porte-de-garage-enroulable-motorisee/3298-porte-de-garage-enroulable-motorisee-sur-mesure.html')
        time.sleep(1)
        driver.maximize_window()
        driver.find_element(By.CSS_SELECTOR, 'p.ConsentLGPDyes').click()

        options_div = driver.find_element(By.CSS_SELECTOR, 'div[class*="groupFieldBlock packlistGroup"]')
        options = options_div.find_elements(By.CSS_SELECTOR, 'div[class*="ndkackFieldItem"]')

        driver.execute_script('scrollTo(0,550)')      
        for option in options:            
            option_title = option.find_element(By.CSS_SELECTOR, 'label').text.strip().lower()
            try:
                option.click()
                time.sleep(1)
            except:
                continue
            
            if 'type de pose' in option_title:
                option.find_elements(By.CSS_SELECTOR, 'div[class="col-md-3 col-xs-4 filterTag img-item-row"]')[0].click()
                time.sleep(1)
            elif 'lames' in option_title:
                if self.type == 55:
                    option.find_element(By.CSS_SELECTOR, 'img[data-value^="55"]').click()
                elif self.type == 77:
                    option.find_element(By.CSS_SELECTOR, 'img[data-value^="77"]').click()
                    option.click() 
            elif 'couleur' in option_title:
                option.find_element(By.CSS_SELECTOR, 'li[data-value^="blanc" i]').click()
            elif 'dimensions' in option_title:
                dimensions_div = option

                width_input = driver.find_elements(By.CSS_SELECTOR, 'input[id^="dimension_text_width"]')
                for w in width_input:
                    if w.is_displayed():
                        width_input = w

                width_min = int(width_input.get_attribute('min'))
                width_max = int(width_input.get_attribute('max'))
                width_input.click()
                width_input.send_keys(width_min)

                height_input = driver.find_elements(By.CSS_SELECTOR, 'input[id^="dimension_text_height"]')
                for h in height_input:
                    if h.is_displayed():
                        height_input = h

                height_min = int(height_input.get_attribute('min'))
                height_max = int(height_input.get_attribute('max'))
                height_input.send_keys(height_min)

                column_list = [i for i in range(width_min, width_max + 100, 100)]
                index_list = [i for i in range(height_min, height_max + 100, 100)]

            time.sleep(2)
            
        driver.execute_script('scrollBy(0,100)')

        dimensions_div.click()
        
        price_place = driver.find_element(By.CSS_SELECTOR, 'div[class="price productPriceUp product-price alu-align-center alu-dir-column"]')

        for index in index_list:
            height_input.clear()
            height_input.send_keys(index)
            time.sleep(2)
            for column in column_list:
                width_input.clear()
                width_input.send_keys(column)
                time.sleep(1)

                price = re.findall(r'\d\s?\.?\d+,\d+', price_place.text.strip())[0].replace(' ', '')
                print(f'Brama: {self.type} - cena {price}')
                self.df_gate.loc[index, column] = price
                time.sleep(0.5)

        driver.quit()