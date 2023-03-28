import time
import pandas as pd
import math
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class ScrapRollerThread(Thread):
    def __init__(self, with_motor=False):
        Thread.__init__(self)
        self.df_roller_pvc40 = pd.DataFrame()
        self.df_roller_alu39 = pd.DataFrame()
        self.df_roller_alu40 = pd.DataFrame()
        self.df_roller_alu55 = pd.DataFrame()
        self.df_roller_alu_thermoreflex_39 = pd.DataFrame()
        self.with_motor = with_motor

    def change_drive(self, driver):
        if not self.with_motor:
            manual = driver.find_element(By.CSS_SELECTOR, 'span[for="volet_visio--type_de_motorisation--manoeuvre_manuelle"]')
            manual.location_once_scrolled_into_view
            driver.execute_script('scrollBy(0,-200)')
            time.sleep(2)
            manual.click()
        else:
            pass

    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://clic-volet.fr/configurateurs/2338-configurateur-volet-visio-3701376143625.html')
        driver.maximize_window()
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="axeptio_btn_acceptAll"]'))
        )
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'button[id="axeptio_btn_acceptAll"]').click()

        self.change_drive(driver)

        height_input = driver.find_element(By.CSS_SELECTOR, 'input[id="volet_visio--dimensions_tableau--hauteur_tableau"]')
        width_input = driver.find_element(By.CSS_SELECTOR, 'input[id="volet_visio--dimensions_tableau--largeur_tableau"]')

        height_min = int(height_input.get_attribute('min'))
        height_max = int(height_input.get_attribute('max'))

        width_min = int(width_input.get_attribute('min'))
        width_max = int(width_input.get_attribute('max'))

        index_list = [math.floor(i/100)*100 for i in range(height_min, height_max + 100, 100)]
        column_list = [math.floor(i/100)*100 for i in range(width_min, width_max + 100, 100)]

        index_list[0] = 454
        index_list[-1] = 3103
        column_list[0] = 414
        column_list[-1] = 4004

        for index in index_list:
            height_input.clear()
            height_input.send_keys(index)
            time.sleep(1)
            for column in column_list:
                width_input.clear()
                width_input.send_keys(column)
                height_input.click()
                time.sleep(1)

                price = driver.find_elements(By.CSS_SELECTOR, 'span[id="prix_final"]')[0].get_attribute('textContent').strip()[:-1]
                price = price.replace(',', '')

                if float(price) < 0:
                    break

                profiles = driver.find_elements(By.CSS_SELECTOR, 'div[class="choix_standard--options row container_options mx-n2 text-center"]')
                profiles[2].location_once_scrolled_into_view
                driver.execute_script('scrollBy(0, -100)')
                profiles = profiles[2].find_elements(By.CSS_SELECTOR, '[class="type_de_lames--one_option choix_standard--one_option col col-auto px-2 col-6 col-sm-4 col-md-4 col-xl-3 mb-3"]')

                if len(profiles) > 0:
                    for profile in profiles:
                        try:
                            profile.click()
                        except:
                            continue
                        time.sleep(0.2)
                        price = driver.find_elements(By.CSS_SELECTOR, 'span[id="prix_final"]')[0].get_attribute('textContent').strip()[:-1]
                        
                        if index % 100 != 0:
                            index = math.floor(index/100)*100
                        
                        if column % 100 != 0:
                            column = math.floor(column/100)*100
                        
                        if 'pvc 40' in profile.text.lower():
                            self.df_roller_pvc40.loc[index, column] = price.replace('.', ',')
                        elif 'alu px-39' in profile.text.lower():
                            self.df_roller_alu39.loc[index, column] = price.replace('.', ',')
                        elif 'alu px-40' in profile.text.lower():
                            self.df_roller_alu40.loc[index, column] = price.replace('.', ',')
                        elif 'alu px-55' in profile.text.lower():
                            self.df_roller_alu55.loc[index, column] = price.replace('.', ',')
                        elif 'thermoreflex' in profile.text.lower():
                            self.df_roller_alu_thermoreflex_39.loc[index, column] = price.replace('.', ',')
                else:
                    break
