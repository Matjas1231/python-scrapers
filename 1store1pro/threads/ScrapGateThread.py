import time
import re
import pandas as pd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class ScrapGateThread(Thread):
    def __init__(self,):
        Thread.__init__(self)
        self.df_gate = pd.DataFrame()

    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://www.1store1pro.com/porte-de-garage/235-volet-roulant-renovation-electrique.html')
        time.sleep(2)
        driver.maximize_window()

        width_input = driver.find_element(By.CSS_SELECTOR, 'div[data-display="true"] > div > input[data-dimension="1"]')
        height_input = driver.find_element(By.CSS_SELECTOR, 'div[data-display="true"] > div > input[data-dimension="2"]')

        width_min = int(width_input.get_attribute('data-min'))
        width_max = int(width_input.get_attribute('data-max'))

        height_min = int(height_input.get_attribute('data-min'))
        height_max = int(height_input.get_attribute('data-max'))

        column_list = [i for i in range(width_min, width_max + 100, 100)]
        index_list = [i for i in range(height_min, height_max + 100, 100)]

        dimensions_supp_inputs = driver.find_element(By.XPATH, '//span[contains(text(), "Dimensions suplémentaires")]/../../div[@class="row"]')
        dimensions_supp_inputs = dimensions_supp_inputs.find_elements(By.CSS_SELECTOR, 'input')

        for input in dimensions_supp_inputs:
            time.sleep(0.5)
            input.send_keys(500)
            input.send_keys(Keys.TAB)

        color_white = driver.find_element(By.CSS_SELECTOR, 'img[alt="Blanc 9010"]')
        color_white.location_once_scrolled_into_view
        time.sleep(2)
        color_white.click()

        for index in index_list:
            driver.execute_script('scrollTo(0, 200)')
            time.sleep(1)
            height_input.clear()
            height_input.send_keys(index)
            height_input.send_keys(Keys.TAB)
            time.sleep(0.5)
            for column in column_list:
                width_input.clear()
                width_input.send_keys(column)
                width_input.send_keys(Keys.TAB)
                time.sleep(0.5)

                driver.execute_script('scrollTo(0, 1500)')

                time.sleep(1)

                price_place = driver.find_element(By.CSS_SELECTOR, 'dd#final_price')                
                price = re.findall(r'\d+\s\d+,\d+', price_place.text)[0]
                print(f'{column} x {index} = {price}')
                
                self.df_gate.loc[index, column] = price
