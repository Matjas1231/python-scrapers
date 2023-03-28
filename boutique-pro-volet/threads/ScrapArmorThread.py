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
    def __init__(self, type='alu40'):
        Thread.__init__(self)
        self.df_armor = pd.DataFrame()
        self.type = type

    def get_link(self):
        link = ''

        if 'alu' in self.type or 'sp' in self.type:
            link = 'https://boutique.pro-volet.fr/tablier-de-volet-roulant/3729-tablier-aluminium-sur-mesure-pour-volet-roulant.html'
        else:
            link = 'https://boutique.pro-volet.fr/tablier-de-volet-roulant/3742-tablier-pvc-sur-mesure-pour-volet-roulant.html'
            
        return link

    def generate_index_and_columns(self, driver):
        dimensions_div = driver.find_element(By.CSS_SELECTOR, 'div.confi_dimension_step.groupDimensionsTab')
        width_div = dimensions_div.find_elements(By.CSS_SELECTOR, 'div[id^=step]')[0]
        height_div = dimensions_div.find_elements(By.CSS_SELECTOR, 'div[id^=step]')[1]
        
        width_input = width_div.find_element(By.CSS_SELECTOR, 'input')
        width_min = int(width_input.get_attribute('data-min'))
        width_max = int(width_input.get_attribute('data-max'))
        
        height_input = height_div.find_element(By.CSS_SELECTOR, 'input')
        height_min = int(height_input.get_attribute('data-min'))
        height_max = int(height_input.get_attribute('data-max'))

        index_list = [math.floor(i/100)*100 for i in range(height_min, height_max + 100, 100)]
        index_list[0] = height_min
        index_list.append(height_max)

        column_list = [i for i in range(width_min, width_max + 100, 100)]

        return index_list, column_list


    def run(self):
        time.sleep(1)
        driver = webdriver.Firefox()
        driver.get(self.get_link())
        
        driver.maximize_window()
        time.sleep(3)

        driver.find_element(By.CSS_SELECTOR, 'a[class="cookie-close-button btn js-cookieCloseButton"]').click()
        driver.execute_script('scrollTo(0, 0)')

        index_list, column_list = self.generate_index_and_columns(driver)

        width_input = driver.find_elements(By.CSS_SELECTOR, 'div.confi_dimension_step.groupDimensionsTab > div > div[class="col-xs-12"] > div > div > div > div > input')[0]
        height_input = driver.find_elements(By.CSS_SELECTOR, 'div.confi_dimension_step.groupDimensionsTab > div > div[class="col-xs-12"] > div > div > div > div > input')[1]
        price_place = driver.find_element(By.CSS_SELECTOR, 'span[id="confi_prix_ttc"]')        

        confirmer_button = driver.find_element(By.XPATH, '//div[text()="Confirmer"]')
        confirmer = driver.find_element(By.XPATH, '//div[text()="Confirmer"]/..')
        
        old_price = ''
        for index in index_list:
            driver.execute_script('scrollTo(0, 0)')
            while True:
                try:
                    height_input.click()
                    height_input.clear()
                    height_input.send_keys(index)
                    height_input.send_keys(Keys.ENTER)
                    break
                except:
                    continue
            for column in column_list:
                driver.execute_script('scrollTo(0, 0)')
                while True:
                    try:
                        width_input.click()
                        width_input.clear()
                        width_input.send_keys(column)
                        width_input.send_keys(Keys.ENTER)
                        break
                    except:
                        continue

                if 'selected' not in confirmer.get_attribute('class'):
                    try:
                        time.sleep(1)
                        confirmer_button.click()
                    except:
                        time.sleep(0.5)
                        confirmer_button.click()
                
                driver.execute_script('scrollTo(0, 1000)')
                time.sleep(1)
                match self.type:
                    case 'alu40':
                        try:
                            profile_alu40 = driver.find_element(By.CSS_SELECTOR, 'div[data-original-title="adp40" i][data-display="true"]')

                            if 'selected' not in profile_alu40.get_attribute('class'):
                                print('Wybrano profil 40')
                                profile_alu40.click()
                                time.sleep(2)
                        except:
                            break
                    case 'alu45':
                        try:
                            profile_alu45 = driver.find_element(By.CSS_SELECTOR, 'div[data-original-title="adp45" i][data-display="true"]')

                            if 'selected' not in profile_alu45.get_attribute('class'):
                                print('Wybrano profil 45')
                                profile_alu45.click()
                                time.sleep(2)
                        except:
                            break
                    case 'alu55':
                        try:
                            profile_alu55 = driver.find_element(By.CSS_SELECTOR, 'div[data-original-title="adp55" i][data-display="true"]')

                            if 'selected' not in profile_alu55.get_attribute('class'):
                                print('Wybrano profil 55')
                                profile_alu55.click()
                                time.sleep(2)
                        except:
                            break
                    case 'sp36':
                        try:
                            profile_sp36 = driver.find_element(By.CSS_SELECTOR, 'div[data-original-title^="sp" i][data-display="true"]')

                            if 'selected' not in profile_sp36.get_attribute('class'):
                                print('Wybrano profil SP 36')
                                profile_sp36.click()
                                time.sleep(2)
                        except:
                            break
                    case 'pvc37':
                        try:
                            profile_pvc37 = driver.find_element(By.CSS_SELECTOR, 'div[data-content*="pvc 37" i][data-display="true"]')

                            if 'selected' not in profile_pvc37.get_attribute('class'):
                                print('Wybrano profil 37')
                                profile_pvc37.click()
                                time.sleep(2)
                        except:
                            break
                    case 'pvc42':
                        try:
                            profile_pvc42 = driver.find_element(By.CSS_SELECTOR, 'div[data-content*="pvc 42" i][data-display="true"]')

                            if 'selected' not in profile_pvc42.get_attribute('class'):
                                print('Wybrano profil 42')
                                profile_pvc42.click()
                                time.sleep(2)
                        except:
                            break

                driver.execute_script('scrollTo(0, 1000)')
                time.sleep(1)

                WebDriverWait(driver, 10).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'span[id="confi_prix_ttc"]'))
                )

                price_place.click()
                price = re.findall('\d+\s?\d+,\d+', price_place.text.strip())[0]

                i = 0
                while old_price == price:
                    print('Pętla - powtórzenie ceny')
                    time.sleep(1)

                    price = driver.find_element(By.CSS_SELECTOR, 'span[id="confi_prix_ttc"]')
                    price.click()
                    price = price.text.strip()
                    price = re.findall('\d+\s?\d+,\d+', price)[0]

                    if old_price != price or i > 0:
                        break

                    i += 1

                print(f'Profil: {self.type} cena - {price}')

                self.df_armor.loc[index, column] = price
                old_price = price

        driver.quit()