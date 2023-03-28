import time
import pandas as pd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ScrapArmorThread(Thread):
    def __init__(self, type='pvc'):
        Thread.__init__(self)
        self.df_armor = pd.DataFrame()
        self.type = type
    
    def generate_index_and_columns(self):
        width_min = 500
        height_min = 500

        match self.type:
            case 'pvc':                
                width_max = 2200                
                height_max = 2200
            case 'alu':
                width_max = 3000                
                height_max = 3000
        
        index_list = [i for i in range(height_min, height_max + 100, 100)]
        column_list = [i for i in range(width_min, width_max + 100, 100)]

        return index_list, column_list

    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://www.voletroulant-online.fr/voletroulant/tablier-volet-roulant.php')
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, 'button[id="axeptio_btn_acceptAll"]').click()
        driver.maximize_window()
        
        if self.type == 'alu':
            driver.find_element(By.CSS_SELECTOR, 'input[id="alu"]').click()

        index_list, column_list = self.generate_index_and_columns()

        if self.type == 'pvc':
            max_square = 4400000
        else:
            max_square = 6600000

        width_input = driver.find_element(By.CSS_SELECTOR, 'input[id="largeur"]')
        height_input = driver.find_element(By.CSS_SELECTOR, 'input[id="hauteur"]')
        for index in index_list:
            height_input.send_keys(Keys.CONTROL, 'a')
            height_input.send_keys(index)
            for column in column_list:
                if (index * column) > max_square:
                    break
                
                width_input.send_keys(Keys.CONTROL, 'a')

                for digit in str(column):
                    width_input.send_keys(digit)
                    time.sleep(0.1)

                time.sleep(0.5)
                price = driver.find_element(By.CSS_SELECTOR, 'span[id="prix"]').text.strip()
                self.df_armor.loc[index, column] = price
        
        driver.quit()