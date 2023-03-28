import time
import pandas as pd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ScrapBasicThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.df_roller_pcv37 = pd.DataFrame()
        self.df_roller_alu39 = pd.DataFrame()
 
    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://www.domondo.fr/volets-roulants/volets-roulants-renovation/volet-roulant-renovation-standard')
        driver.maximize_window()
        driver.execute_script('window.scrollTo(0, 500)')
        driver.find_element(By.ID, 'accept-cookies-checkbox').click()

        sizes_row = driver.find_element(By.CSS_SELECTOR, 'div[class="sizes row ng-star-inserted"]')
        height, width = sizes_row.find_elements(By.CSS_SELECTOR, 'div[class="help-block"]')

        width_min, width_max = width.find_elements(By.CSS_SELECTOR, 'span[class="ng-star-inserted"]')
        width_min = int(width_min.text[5:width_min.text.find('mm')].strip())
        width_max = int(width_max.text[5:width_max.text.find('mm')].strip())

        height_min, height_max = height.find_elements(By.CSS_SELECTOR, 'span[class="ng-star-inserted"]')
        height_min = int(height_min.text[5:height_min.text.find('mm')].strip())
        height_max = int(height_max.text[5:height_max.text.find('mm')].strip())

        column_list = [i for i in range(width_min, width_max + 100, 100)]
        index_list = [i for i in range(height_min, height_max + 100, 100)]

        width_input = sizes_row.find_element(By.CSS_SELECTOR, 'input[class*="cf-size-width form-control"]')
        height_input = sizes_row.find_element(By.CSS_SELECTOR, 'input[class*="cf-size-height form-control"]')
        for index in index_list:
            height_input.clear()
            height_input.send_keys(index)
            height_input.send_keys(Keys.ENTER)
            time.sleep(0.1)
            for column in column_list:
                if float(index * column) > 4300000:
                    break
                width_input.clear()
                width_input.send_keys(column)
                width_input.send_keys(Keys.ENTER)
                time.sleep(0.1)

                profiles = driver.find_element(By.XPATH, '//*[@id="cf-step-10157"]/div/div[2]/div')
                profiles = profiles.find_elements(By.CSS_SELECTOR, 'div[class*="col-xs-3 col-xxs-6 item item-grid4"]')                
                for ind, profile in enumerate(profiles):
                    try:
                        profiles[ind].click()
                    except:
                        continue

                    time.sleep(0.1)
                    
                    kastens = driver.find_element(By.ID, 'cf-step-10161')
                    kastens.location_once_scrolled_into_view
                    kastens = kastens.find_elements(By.CSS_SELECTOR, 'div[class*="col-xs-3 col-xxs-6"]')
                    driver.execute_script('scrollBy(0,-400)')
                    kastens[0].click()
                    driver.execute_script('window.scrollTo(0,500)')
                    profile_name = profile.find_element(By.CSS_SELECTOR, 'img').get_attribute('title').strip()
                    product_price = driver.find_element(By.CSS_SELECTOR, 'div[class="summary-price text-right"]').find_element(By.CSS_SELECTOR, 'span[class="price-value"]').text.strip()[:-2].replace('.', ',')

                    match profile_name:
                        case 'PVC 37 mm':
                            self.df_roller_pcv37.loc[index, column] = product_price
                        case 'Aluminium 39 mm':
                            self.df_roller_alu39.loc[index, column] = product_price
        driver.quit()