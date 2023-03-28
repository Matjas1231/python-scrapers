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
    def __init__(self, link, change_profil=False):
        Thread.__init__(self)
        self.df_roller = pd.DataFrame()
        self.link = link
        self.change_profil = change_profil

    def run(self):
        time.sleep(1)
        driver = webdriver.Firefox()
        driver.get(self.link)
        driver.maximize_window()
        time.sleep(2)

        WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, '//button[@id="didomi-notice-agree-button"]'))
        ).click()

        WebDriverWait(driver, 20).until_not(
            ec.visibility_of_element_located((By.XPATH, '//div[@id="option-loader"]'))
        )

        driver.execute_script('scrollTo(0, 400)')

        time.sleep(0.5)

        if self.change_profil:
            driver.find_element(By.XPATH, '//select[@data-base-attribute="vr_dimensions_lames"]/option[2]').click()
            time.sleep(2)

        inputs = driver.find_elements(By.XPATH, '//div[contains(@class, "input-field") and contains(@class, "dimension") and (not(contains(@style, "display: none")) or not(@style))]')

        for input in inputs:
            if len(input.find_elements(By.XPATH, './/input[starts-with(@data-base-attribute, "vr_largeur") and not(@disabled)]')) > 0:
                width_input = input.find_elements(By.XPATH, './/input[starts-with(@data-base-attribute, "vr_largeur") and not(@disabled)]')[0]

                dimensions = input.find_element(By.XPATH, 'span[@class="u-ml-xs u-text-xs u-color-gray mention bespoke"]').text
                dimensions = re.findall('([\d]+) (mm)', dimensions)
                
                width_min = int(dimensions[0][0])
                width_max = int(dimensions[1][0])

            if len(input.find_elements(By.XPATH, './/input[starts-with(@data-base-attribute, "vr_hauteur") and not(@disabled)]')) > 0:
                height_input = input.find_elements(By.XPATH, './/input[starts-with(@data-base-attribute, "vr_hauteur") and not(@disabled)]')[0]

                dimensions = input.find_element(By.XPATH, 'span[@class="u-ml-xs u-text-xs u-color-gray mention bespoke"]').text
                dimensions = re.findall('([\d]+) (mm)', dimensions)

                height_min = int(dimensions[0][0])
                height_max = int(dimensions[1][0])

        height_input_parent_div = height_input.find_element(By.XPATH, './/..').find_element(By.XPATH, './/..')

        index_list = [math.floor(i/100)*100 for i in range(height_min, height_max + 100, 100)]
        column_list = [math.floor(i/100)*100 for i in range(width_min, width_max + 100, 100)]
        index_list[0] = height_min
        column_list[0] = width_min

        message = ''
        old_price = ''
        for index in index_list:
            height_input.send_keys(Keys.CONTROL, 'a')
            height_input.send_keys(index)
            
            time.sleep(2)
            for column in column_list:
                width_input.send_keys(Keys.CONTROL, 'a')
                width_input.send_keys(column)

                time.sleep(0.5)
        
                if 'validation-error' in height_input_parent_div.get_attribute('class'):
                    width_input.send_keys(Keys.CONTROL, 'a')
                    width_input.send_keys(width_min)
                    break

                message = driver.find_element(By.XPATH, 'div[@class="configuration-message"]')
                if message.text:
                    print('Wykryto wiadomość: ' + message.text)
                    width_input.send_keys(Keys.CONTROL, 'a')
                    width_input.send_keys(column)

                    time.sleep(2)
                
                price = driver.find_elements(By.XPATH, 'span[@data-price-type="finalPrice"]')[0].text.strip()
                price = re.findall('[\d]+,[\d]+', price)[0]

                try:
                    WebDriverWait(driver, 30).until(
                        lambda drv: re.findall('[\d]+,[\d]+', drv.find_elements(By.XPATH, 'span[@data-price-type="finalPrice"]')[0].text.strip())[0] != old_price
                    )
                except:
                    while old_price == price:
                        print('Pętla')
                        width_input.send_keys(Keys.CONTROL, 'a')
                        time.sleep(1)
                        width_input.send_keys(Keys.BACKSPACE)
                        width_input.send_keys(column)
                        height_input.click()
                        time.sleep(2)

                        price = driver.find_elements(By.XPATH, 'span[@data-price-type="finalPrice"]')[0].text.strip()
                        price = re.findall('[\d]+,[\d]+', price)[0]

                        if old_price != price or i > 1:
                            break

                        i += 1

                time.sleep(0.2)

                old_price = price

                self.df_roller.loc[math.floor(index/100)*100, math.floor(column/100)*100] = price

        driver.quit()