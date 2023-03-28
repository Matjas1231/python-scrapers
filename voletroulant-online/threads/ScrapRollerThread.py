import time
import pandas as pd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class ScrapRollerThread(Thread):
    def __init__(self, type='pvc', with_motor=False):
        Thread.__init__(self)
        self.df_roller = pd.DataFrame()
        self.type = type
        self.with_motor = with_motor

    def generate_index_and_columns(self):
        if self.type == 'pvc':
            width_min = 700
            width_max = 2100
            height_min = 700
            height_max = 2200
            if self.with_motor:
                height_max = 2250

        if self.type == 'alu':
            width_min = 700
            width_max = 3000
            height_min = 700
            height_max = 2200
            if self.with_motor:
                height_max = 3000

        index_list = [i for i in range(height_min, height_max + 100, 100)]
        column_list = [i for i in range(width_min, width_max + 100, 100)]

        return index_list, column_list

    def run(self):        
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://www.voletroulant-online.fr/voletroulant/volet-roulant-sur-mesure.php?volet=3')
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, 'button[id="axeptio_btn_acceptAll"]').click()
        driver.maximize_window()

        index_list, column_list = self.generate_index_and_columns()
        if self.type == 'alu' and self.with_motor:
            max_square = 6600000
        else:
            max_square = 4000000

        for index in index_list:
            for column in column_list:
                if (index * column) > max_square:
                    break
                time.sleep(2)

                first_step = driver.find_element(By.CSS_SELECTOR, 'div[id="etape1"]')
                first_step.find_element(By.CSS_SELECTOR, 'div[class="suivant"]').click()
                time.sleep(1.5)

                second_step = driver.find_element(By.CSS_SELECTOR, 'div[id="etape2"]')

                if not self.with_motor:
                    driver.find_element(By.CSS_SELECTOR, 'img[id="manoeuvre1"]').click()
                    second_step.find_element(By.CSS_SELECTOR, 'div[class="suivant"]').click()
                else:
                    driver.find_element(By.CSS_SELECTOR, 'img[id="manoeuvre8"]').click()
                    time.sleep(0.5)
                    driver.find_element(By.CSS_SELECTOR, 'div[id="valid_acc"]').click()
                
                time.sleep(0.5)
            
                WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'div[id="etape9"] > div[class="suivant"]')))
                
                third_step = driver.find_element(By.CSS_SELECTOR, 'div[id="etape9"]')
                third_step.find_element(By.CSS_SELECTOR, 'div[class="suivant"]').click()

                time.sleep(1)
                
                fourth_step = driver.find_element(By.CSS_SELECTOR, 'div[id="etape3"]')

                if self.type == 'pvc':
                    driver.find_element(By.CSS_SELECTOR, 'div[id="blockPVC"]').find_element(By.CSS_SELECTOR, 'img').click()
                else:
                    driver.find_element(By.CSS_SELECTOR, 'div[id="blockALU"]').find_element(By.CSS_SELECTOR, 'img').click()

                fourth_step.find_element(By.CSS_SELECTOR, 'div[class="suivant"]').click()
                time.sleep(3)

                width_input = driver.find_element(By.CSS_SELECTOR, 'input[id="lmax"]')

                width_input.send_keys(Keys.CONTROL, 'a')
                width_input.send_keys(column)

                height_input = driver.find_element(By.CSS_SELECTOR, 'input[id="hmax"]')
                height_input.send_keys(Keys.CONTROL, 'a')
                height_input.send_keys(index)

                WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'div[id="etape4"] > div[class="suivant"]')))
                
                fifth_step = driver.find_element(By.CSS_SELECTOR, 'div[id="etape4"]')
                fifth_step.find_element(By.CSS_SELECTOR, 'div[class="suivant"]').click()

                WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'div[id="etape5"]')))

                sixth_step = driver.find_element(By.CSS_SELECTOR, 'div[id="etape5"]')
                sixth_step.find_element(By.CSS_SELECTOR, 'div[class="suivant"]').click()
                time.sleep(2)

                seventh_step = driver.find_element(By.CSS_SELECTOR, 'div[id="etape6"]')
                seventh_step.find_element(By.CSS_SELECTOR, 'div[id="save_volet"]').click()

                WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'div[id="acces_panier"]')))

                price = driver.find_element(By.CSS_SELECTOR, 'span[id="prixvolet"]').text.strip()

                print(price)
                self.df_roller.loc[index, column] = price

                driver.find_element(By.CSS_SELECTOR, 'div[id="acces_panier"]').click()

                time.sleep(1)
                remove_from_cart = driver.find_elements(By.CSS_SELECTOR, 'a[title="Enlever"]')
                for link in remove_from_cart:
                    link.click()
                    time.sleep(1)
                time.sleep(1)

                driver.get('https://www.voletroulant-online.fr/voletroulant/volet-roulant-sur-mesure.php?volet=3')

        driver.quit()