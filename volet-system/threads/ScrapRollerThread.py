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
    def __init__(self, link):
        Thread.__init__(self)
        self.df_roller = pd.DataFrame()
        self.link = link
 
    def run(self):
        driver = webdriver.Chrome()
        driver.get(self.link)
        driver.maximize_window()
        
        inputs = driver.find_element(By.CSS_SELECTOR, 'div[class=" step_options "]')
        height_input = inputs.find_elements(By.CSS_SELECTOR, 'input[class="form-control grey"]')[0]
        width_input = inputs.find_elements(By.CSS_SELECTOR, 'input[class="form-control grey"]')[1]

        height_min = int(height_input.get_attribute('data-min'))
        height_max = int(height_input.get_attribute('data-max'))

        width_min = int(width_input.get_attribute('data-min'))
        width_max = int(width_input.get_attribute('data-max'))

        index_list = [i for i in range(height_min, height_max + 100, 100)]
        column_list = [i for i in range(width_min, width_max + 100, 100)]
        column_list[-1] = width_max

        options = driver.find_elements(By.CSS_SELECTOR, 'div[class*="step_group form-group"]')[1:-1]
        for option in options:
            if option.is_displayed():
                try:
                    option.find_element(By.CSS_SELECTOR, 'div[id^="step_option_"]').click()
                    time.sleep(1)
                except:
                    continue

        for index in index_list:
            height_input.send_keys(Keys.CONTROL, 'a')
            height_input.send_keys(index)

            WebDriverWait(driver, 10).until_not(ec.element_attribute_to_include((By.CSS_SELECTOR, 'input[class="form-control grey"]'), 'disabled'))

            if driver.find_elements(By.CSS_SELECTOR, 'div[class="error-step"]')[0].is_displayed():
                width_input.send_keys(Keys.CONTROL, 'a')
                width_input.send_keys(width_min)

                WebDriverWait(driver, 10).until_not(ec.element_attribute_to_include((By.CSS_SELECTOR, 'input[class="form-control grey"]'), 'disabled'))

                height_input.send_keys(Keys.CONTROL, 'a')
                height_input.send_keys(index)

                WebDriverWait(driver, 10).until_not(ec.element_attribute_to_include((By.CSS_SELECTOR, 'input[class="form-control grey"]'), 'disabled'))

            for column in column_list:
                width_input.send_keys(Keys.CONTROL, 'a')
                width_input.send_keys(column)
                WebDriverWait(driver, 10).until_not(ec.element_attribute_to_include((By.CSS_SELECTOR, 'input[class="form-control grey"]'), 'disabled'))
                
                if driver.find_elements(By.CSS_SELECTOR, 'div[class="error-step"]')[0].is_displayed():
                    width_input.send_keys(Keys.CONTROL, 'a')
                    width_input.send_keys(width_min)
                    WebDriverWait(driver, 10).until_not(ec.element_attribute_to_include((By.CSS_SELECTOR, 'input[class="form-control grey"]'), 'disabled'))
                    break

                time.sleep(0.5)

                price = driver.find_element(By.CSS_SELECTOR, 'p[class="current-price"]').text.strip()[:-6].replace(' ', '')
               
                self.df_roller.loc[math.floor(index/100)*100, math.floor(column/100)*100] = price

        driver.quit()