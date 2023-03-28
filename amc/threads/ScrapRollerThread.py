import time
import pandas as pd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class ScrapRollerThread(Thread):
    def __init__(self, type='pvc'):
        Thread.__init__(self)
        self.df_sangle = pd.DataFrame()
        self.df_motor = pd.DataFrame()

        if type == 'alu39':
            self.df_net_sangle = pd.DataFrame()
            self.df_net_motor = pd.DataFrame()

        self.type = type
 
    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://www.amc-production.fr/volet-roulant/devis')
        time.sleep(2)
        driver.maximize_window()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'div[class="jsx-3181655403 eapp-cookie-consent-actions-accept eapp-cookie-consent-actions-button"]').click()
        
        self.choose_profile(driver)
        driver.find_element(By.XPATH, '//*[@id="vue"]/section[1]/div/div/div[1]/div[6]/div[2]/div[1]/div').click()

        driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn-rouge-amc css_btn_obtenir_prix_du_devis pull-right"]').click()
        time.sleep(1)

        index_list, column_list = self.generate_index_and_columns()
        width_input = driver.find_element(By.XPATH, '//*[@id="vue"]/section[2]/div/div[1]/div[2]/table[3]/tbody/tr[3]/td[7]/table/tbody/tr[1]/td[2]/input')
        height_input = driver.find_element(By.XPATH, '//*[@id="vue"]/section[2]/div/div[1]/div[2]/table[3]/tbody/tr[3]/td[7]/table/tbody/tr[2]/td[2]/input')
        
        product_price_with_delivery = driver.find_element(By.XPATH, '/html/body/div[4]/section[2]/div/div[2]/div/div[1]/div[3]/div[2]/span[2]')
        
        select = Select(driver.find_element(By.XPATH, '//*[@id="vue"]/section[2]/div/div[1]/div[2]/table[3]/tbody/tr[3]/td[5]/div/select'))        
        if self.type == 'alu52':
            select_profile_type = Select(driver.find_element(By.XPATH, '/html/body/div[4]/section[2]/div/div[1]/div[2]/table[3]/tbody/tr[3]/td[3]/div/select'))
            select_profile_type.select_by_value('AL52')

        for index in index_list:
            # Reset szerokości w celu włączenia taśmy
            width_input.send_keys((Keys.CONTROL, 'a'))
            width_input.send_keys(800)
            select.select_by_value('sangle')

            height_input.send_keys(Keys.CONTROL, 'a')
            height_input.send_keys(index)            
            for column in column_list:
                if (column <= 2000 and self.type == 'alu39') or (column <= 1500 and self.type == 'alu52') or self.type == 'pvc':
                    width_input.send_keys(Keys.CONTROL, 'a')
                    width_input.send_keys(column)

                    time.sleep(0.2)
                    product_price_with_delivery.click()

                    product_price = self.calculate_cost(driver, product_price_with_delivery)
                    self.df_sangle.loc[index, column] = str(product_price).replace('.', ',')

                    try:
                        product_price = self.take_price_with_net(driver, product_price_with_delivery)
                        self.df_net_sangle.loc[index, column] = str(product_price).replace('.', ',')
                    except:
                        pass

                    # if column >= min_motor_width:
                    select.select_by_value('electrique_aok')
                
                    product_price_with_delivery.click()

                    product_price = self.calculate_cost(driver, product_price_with_delivery)
                    self.df_motor.loc[index, column] = str(product_price).replace('.', ',')

                    try:
                        product_price = self.take_price_with_net(driver, product_price_with_delivery)
                        self.df_net_motor.loc[index, column] = str(product_price).replace('.', ',')
                    except:
                        pass

                    select.select_by_value('sangle')
                else:
                    select.select_by_value('electrique_aok')

                    width_input.send_keys((Keys.CONTROL, 'a'))
                    width_input.send_keys(column)
                    time.sleep(0.2)

                    product_price_with_delivery.click()
                    
                    product_price = self.calculate_cost(driver, product_price_with_delivery)
                    self.df_motor.loc[index, column] = str(product_price).replace('.', ',')

    def take_price_with_net(self, driver, product_price_with_delivery):
            select_net = Select(driver.find_element(By.XPATH, '/html/body/div[4]/section[2]/div/div[1]/div[2]/table[3]/tbody/tr[4]/td[3]/div/select'))
            select_net.select_by_visible_text('Avec moustiquaire')
            time.sleep(0.2)
            product_price_with_delivery.click()

            product_price = self.calculate_cost(driver, product_price_with_delivery)
            select_net.select_by_visible_text('Pas de moustiquaire')

            return product_price

    def calculate_cost(self, driver, product_price_with_delivery):
        delivery_cost = driver.find_element(By.CSS_SELECTOR, 'span[class="text-bold css_prix_livraison"]')
        try:
            product_price = float(product_price_with_delivery.text.strip()[:-2].replace(',', '.')) - float(delivery_cost.text.strip()[:-2].replace(',', '.'))
            product_price = round(product_price, 2)
        except:
            product_price = product_price_with_delivery.text.strip()[:-2].replace('.', ',')

        return product_price

    def generate_index_and_columns(self):
        width_min = 300
        height_min = 300
        height_max = 2800

        match self.type:
            case 'pvc':                
                width_max = 1800
            case 'alu39':
                width_max = 3000
            case 'alu52':
                width_min = 800
                width_max = 4000
                height_min = 800

        index_list = [i for i in range(height_min, height_max + 100, 100)]
        column_list = [i for i in range(width_min, width_max + 100, 100)]

        return index_list, column_list
    
    def choose_profile(self, driver):
        match self.type:
            case 'pvc':
                driver.find_elements(By.CSS_SELECTOR, 'div[class*="css_coloris_tablier blanc css_option_selectionnable"]')[1].click()
            case 'alu39' | 'alu52':
                pass
