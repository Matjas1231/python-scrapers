import time
import pandas as pd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ScrapArmorThread(Thread):
    def __init__(self, type='alu39'):
        Thread.__init__(self)
        self.df_armor = pd.DataFrame()
        self.df_motor = pd.DataFrame()
        self.type = type

    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://www.amc-production.fr/tablier/devis')
        time.sleep(2)
        driver.maximize_window()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'div[class="jsx-3181655403 eapp-cookie-consent-actions-accept eapp-cookie-consent-actions-button"]').click()

        self.choose_profile(driver)
        
        driver.find_element(By.CSS_SELECTOR, 'button[name="obtenor_prix_devis"]').click()
        time.sleep(3)
        driver.execute_script('scrollBy(0,-200)')
        driver.find_element(By.CSS_SELECTOR, 'button[class="css_bouton_modifier_details_article btn btn-rouge-amc"]').click()

        index_list, column_list = self.generate_index_and_columns()

        width_input = driver.find_element(By.XPATH, '//*[@id="vue"]/section[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[6]/table/tbody/tr[1]/td[2]/input')
        height_input = driver.find_element(By.XPATH, '//*[@id="vue"]/section[2]/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[6]/table/tbody/tr[2]/td[2]/input')
        product_price_with_delivery = driver.find_element(By.XPATH, '//*[@id="vue"]/section[2]/div/div[2]/div/div[1]/div[3]/div[2]/span[2]')        
        for index in index_list:            
            height_input.send_keys(Keys.CONTROL, 'a')
            height_input.send_keys(index)   
            for column in column_list:
                    width_input.send_keys(Keys.CONTROL, 'a')
                    width_input.send_keys(column)

                    time.sleep(0.2)
                    product_price_with_delivery.click()
                    product_price = self.calculate_cost(driver, product_price_with_delivery)
                    self.df_armor.loc[index, column] = str(product_price).replace('.', ',')

    def choose_profile(self, driver):
        match self.type:
            case 'alu52':
                driver.find_element(By.XPATH, '//*[@id="vue"]/section[1]/div/div/div[1]/div[4]/div[1]/div/div[1]/div[2]/div').click()
            case 'alu39':
                pass

    def calculate_cost(self, driver, product_price_with_delivery):
        delivery_cost = driver.find_element(By.XPATH, '//*[@id="vue"]/section[2]/div/div[2]/div/div[1]/div[3]/div[1]/span[4]')
        try:
            product_price = float(product_price_with_delivery.text.strip()[:-2].replace(',', '.')) - float(delivery_cost.text.strip()[:-2].replace(',', '.'))
            product_price = round(product_price, 2)
        except:
            product_price = product_price_with_delivery.text.strip()[:-2].replace('.', ',')

        return product_price

    def generate_index_and_columns(self):
        width_min = 200
        height_min = 200

        match self.type:
            case 'alu39':
                width_max = 3000
                height_max = 3000
            case 'alu52':
                width_max = 4000
                height_max = 3000

        index_list = [i for i in range(height_min, height_max + 100, 100)]
        column_list = [i for i in range(width_min, width_max + 100, 100)]

        return index_list, column_list

