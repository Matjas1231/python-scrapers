import time
import pandas as pd
import re
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By

class ScrapGatehread(Thread):
    def __init__(self, type=55):
        Thread.__init__(self)
        self.df_gate = pd.DataFrame()
        self.type = type

    def run(self):        
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.get('https://www.fermeturegarage.com/portes-de-garage-enroulables.html')
        time.sleep(1)
        driver.maximize_window()

        driver.find_element(By.CSS_SELECTOR, 'a#rgpd-ok').click()
        driver.execute_script('scrollTo(0, 300)')
        driver.find_element(By.CSS_SELECTOR, f'input[id="{self.type}"]').click()

        time.sleep(1)

        driver.execute_script('scrollTo(0, document.body.scrollHeight)')

        width_input = driver.find_element(By.CSS_SELECTOR, 'input#client_largeur')
        height_input = driver.find_element(By.CSS_SELECTOR, 'input#client_hauteur')

        width_min = 600 if self.type == 55 else 500
        width_max = int(driver.find_element(By.CSS_SELECTOR, 'em#volet_largeur_max').text.strip())
        width_max_totale = driver.find_element(By.CSS_SELECTOR, 'em#volet_largeur_ht')
        
        height_min = 500 if self.type == 55 else 400
        height_max = int(driver.find_element(By.CSS_SELECTOR, 'em#volet_hauteur_max').text.strip())
        height_max_totale = driver.find_element(By.CSS_SELECTOR, 'em#volet_hauteur_ht')

        column_list = [i for i in range(width_min, width_max + 100, 100)]
        index_list = [i for i in range(height_min, height_max + 100, 100)]
        
        price_place = driver.find_element(By.CSS_SELECTOR, 'p#prixTotal > em')
        for index in index_list:
            height_input.clear()

            for dig in str(index):
                height_input.send_keys(dig)
                time.sleep(0.2)

            for column in column_list:
                width_input.clear()
                max_square = 8000000 if self.type == 55 else 15000000

                for dig in str(column):
                    width_input.send_keys(dig)
                    time.sleep(0.2)

                if int(width_max_totale.text.strip()) > width_max or int(height_max_totale.text.strip()) > height_max or int(width_max_totale.text.strip()) * int(height_max_totale.text.strip()) > max_square:
                    print(f'Przerwano: brama {self.type}')
                    break

                height_input.click()

                time.sleep(2)
                i = 0
                while True:
                    try:
                        if i > 2:
                            break
                        
                        price_place = driver.find_element(By.CSS_SELECTOR, 'p#prixTotal > em')
                        break
                    except:
                        height_input.click()
                        width_input.click()
                        time.sleep(1)
                        i += 1
                        continue

                price = re.findall(r'\d+\s?\.?\d+,\d+', price_place.text.strip())[0]

                print(f'Profil: {self.type} - cena {price}')
                self.df_gate.loc[index, column] = price

        driver.quit()


        

        