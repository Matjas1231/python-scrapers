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

class ScrapRollerThread(Thread):
    def __init__(self, type='alu40', with_motor=False):
        Thread.__init__(self)
        self.df_roller = pd.DataFrame()
        self.type = type
        self.with_motor = with_motor

    def get_link(self):
        link = ''
        if self.with_motor:
            link = 'https://boutique.pro-volet.fr/volets-roulants-renovations/3759-volet-roulant-renovation-electrique-filaire.html'
        else:
            link = 'https://boutique.pro-volet.fr/volets-roulants-renovations/3760-volet-roulant-renovation-manuel-a-manivelle.html'
            
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
        profile_div = driver.find_element(By.XPATH, '//span[contains(text(), "Personnalisation du volet")]/../../..')
        profile_option = profile_div.find_elements(By.CSS_SELECTOR, 'div[id^="step_option"]')[0]

        profile_type_div = profile_div.find_element(By.XPATH, 'following-sibling::div[starts-with(@id, "step_")]')
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

                WebDriverWait(driver, 10).until(lambda d: 'notAvailable' not in confirmer.get_attribute('class'))
                if 'selected' not in confirmer.get_attribute('class'):
                    try:
                        time.sleep(1)
                        confirmer_button.click()
                    except:
                        time.sleep(0.5)
                        confirmer_button.click()

                WebDriverWait(driver, 10).until(lambda d: 'notAvailable' not in profile_option.get_attribute('class'))
       
                driver.execute_script('scrollTo(0, 1000)')
                WebDriverWait(driver, 10).until(
                    ec.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Personnalisation du volet")]/../../..'))
                )
                time.sleep(1)

                if 'selected' not in profile_option.get_attribute('class'):
                    try:
                        time.sleep(1)
                        profile_option.click()
                    except:
                        time.sleep(0.5)
                        profile_option.click()

                WebDriverWait(driver, 10).until(lambda d: 'notAvailable' not in profile_type_div.get_attribute('class'))
                
                match self.type:
                    case 'alu40':
                        try:
                            profile_alu40 = driver.find_element(By.CSS_SELECTOR, 'div[data-original-title="adp40" i][data-display="true"]')

                            if 'selected' not in profile_alu40.get_attribute('class'):
                                print('Wybrano profil 40')
                                profile_alu40.click()
                        except:
                            break
                    case 'alu50':
                        try:
                            profile_alu50 = driver.find_element(By.CSS_SELECTOR, 'div[data-original-title="adp50" i][data-display="true"]')

                            if 'selected' not in profile_alu50.get_attribute('class'):
                                print('Wybrano profil 50')
                                profile_alu50.click()
                        except:
                            break
                    case 'alu55':
                        try:
                            profile_alu55 = driver.find_element(By.CSS_SELECTOR, 'div[data-original-title="adp55" i][data-display="true"]')

                            if 'selected' not in profile_alu55.get_attribute('class'):
                                print('Wybrano profil 55')
                                profile_alu55.click()
                        except:
                            break

                driver.execute_script('scrollTo(0, 1000)')
                time.sleep(1.5)

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

                self.df_roller.loc[index, column] = price
                old_price = price

        driver.quit()
                
