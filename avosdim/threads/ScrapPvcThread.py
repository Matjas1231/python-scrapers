import time
import pandas as pd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class ScrapPvcThread(Thread):
    def __init__(self, is_armor):
        Thread.__init__(self)
        self.df = pd.DataFrame()
        self.is_armor = is_armor
 
    def run(self):
        time.sleep(1)
        driver = webdriver.Firefox()
        if self.is_armor:
            driver.get('https://avosdim.com/de/rollladenpanzer-einzelteil-nach-mass-aluminium-pvc.html')
        else:
            driver.get('https://avosdim.com/volet-roulant-sur-mesure-renovation.html')
        driver.maximize_window()
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable(('id', 'axeptio_btn_acceptAll'))
        ).click()

        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input[class="number"]'))
        ).click()

        height_box = driver.find_element(By.ID, 'hauteur')
        height_input = height_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')
        height_min = height_input.get_attribute('min')
        height_max = height_input.get_attribute('max')

        width_box = driver.find_element(By.ID, 'largeur')
        width_input = width_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')
        width_min = width_input.get_attribute('min')

        index_list = [i for i in range(int(height_min), int(height_max) + 100, 100)]
        column_dict = {}
        if self.is_armor:
            for i in range(int(width_min), 1800 + 100, 100):
                if i == 560:
                    column_dict[i] = i-60
                else:
                    column_dict[i-60] = i-60
        else:
            for i in range(int(width_min), 1800 + 100, 100):
                if i == 626:
                    column_dict[i] = i-26
                else:
                    column_dict[i-26] = i-26

        price = driver.find_element(By.CSS_SELECTOR, 'span[id^=product-price-]')
        for index in index_list:
            height_box = driver.find_element(By.ID, 'hauteur')
            height_input = height_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')
            width_box = driver.find_element(By.ID, 'largeur')
            width_input = width_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')

            height_input.clear()
            height_input.send_keys(index)
            price.click()

            WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="loader"]')))
            time.sleep(0.5)
            height_box = driver.find_element(By.ID, 'hauteur')
            height_input = height_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')
            width_box = driver.find_element(By.ID, 'largeur')
            width_input = width_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')

            for orginal_col, mapped_col in column_dict.items(): 
                height_box = driver.find_element(By.ID, 'hauteur')
                height_input = height_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')
                width_box = driver.find_element(By.ID, 'largeur')
                width_input = width_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')

                width_input.clear()
                width_input.send_keys(orginal_col)
                price.click()
                WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="loader"]')))
                time.sleep(0.8)
                height_box = driver.find_element(By.ID, 'hauteur')
                height_input = height_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')
                width_box = driver.find_element(By.ID, 'largeur')
                width_input = width_box.find_element(By.CSS_SELECTOR, 'input[class="number"]')

                self.df.loc[index, mapped_col] = price.text[:-2].replace('.', ',')
                
        driver.quit()
