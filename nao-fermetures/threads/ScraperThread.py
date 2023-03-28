import time
import pandas as pd
import re
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

class ScraperThread(Thread):
    def __init__(self, type=39, product='roller'):
        Thread.__init__(self)
        self.df = pd.DataFrame()
        self.type = type
        self.product = product

    def get_link(self):
        link = ''

        if self.product == 'roller':
            link = 'https://www.nao-fermetures.fr/volet-roulant-aluminium-traditionnel-c2x37403978'
        elif self.product == 'gate':
            if self.type == 55:
                link = 'https://www.nao-fermetures.fr/porte-de-garage-enroulable-55-mm-c2x18660336'
            elif self.type == 77:
               link = 'https://www.nao-fermetures.fr/porte-de-garage-enroulable-77-mm-c2x28672503' 
            
        return link


    def run(self):        
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get(self.get_link())
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="c-app-cookies__btn c-app-cookies__btn--success"]'))
        ).click()

        driver.maximize_window()

        if self.product == 'roller':
            Select(driver.find_element(By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID2"]')).select_by_visible_text(f'{self.type} mm')
        
        height_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID0"]'))
        width_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID1"]'))

        height_options = driver.find_element(By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID0"]').find_elements(By.CSS_SELECTOR, 'option')
        width_options = driver.find_element(By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID1"]').find_elements(By.CSS_SELECTOR, 'option')
        
        index_list = [i.text for i in height_options]
        column_list = [i.text for i in width_options]
        for index in index_list:
            width_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID1"]'))
            width_select.select_by_index(0)

            WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID0"]'))
            )

            height_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID0"]'))
            height_select.select_by_visible_text(index)
            time.sleep(0.5)
            
            WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID1"]'))
            )

            for column in column_list:
                width_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="PDTOPTVALUEID1"]'))
                
                try:
                    width_select.select_by_visible_text(column)
                except:
                    width_select.select_by_index(0)
                    break

                time.sleep(0.5)

                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'span[class="PBSalesPrice"]'))
                )

                price = driver.find_element(By.CSS_SELECTOR, 'span[class="PBSalesPrice"]')
                self.df.loc[index, column] = re.findall(r'\d+\s?\.?\d+,\d+', price.text.strip())[0].replace('.', '')
        
        driver.quit()