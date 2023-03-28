import time
import math
import pandas as pd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ScrapArmorThread(Thread):
    def __init__(self, type='39'):
        Thread.__init__(self)
        self.df_armor = pd.DataFrame()
        self.type = type

    def link_to_product(self):
        link = ''
        match self.type:
            case '39':
                link = 'https://www.rollorieper.de/artikel_details.php?artikel=rolladenpanzer39'
            case '52':
                link = 'https://www.rollorieper.de/artikel_details.php?artikel=rolladenpanzer52'
            case '77':
                link = 'https://www.rollorieper.de/artikel_details.php?artikel=rolladenpanzer77'
            
        return link
        
    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": ["https://uct.service.usercentrics.eu/", 'https://privacy-proxy.usercentrics.eu', 'https://app.usercentrics.eu/']})
        driver.execute_cdp_cmd('Network.enable', {})
        driver.get(self.link_to_product())

        index_list, column_list = self.generate_index_and_columns()
        height_input = driver.find_element(By.ID, 'hoehe')
        width_input = driver.find_element(By.ID, 'breite')
        
        for index in index_list:
            height_input = driver.find_element(By.ID, 'hoehe')
            height_input.send_keys(Keys.CONTROL, 'a')
            height_input.send_keys(index)

            width_input = driver.find_element(By.ID, 'breite')
            width_input.send_keys(Keys.TAB)
            time.sleep(1)
            for column in column_list:
                width_input = driver.find_element(By.ID, 'breite')
                match self.type:
                    case '39':
                        max_square = 60000
                    case '52':
                        max_square =  95000
                    case '77':
                        max_square = 150000

                if (column * index) > max_square:
                    break

                width_input.send_keys(Keys.CONTROL, 'a')
                width_input.send_keys(column)
                height_input = driver.find_element(By.ID, 'hoehe')
                height_input.send_keys(Keys.TAB)

                time.sleep(1)

                if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="arretierung"] :nth-child(2)').get_attribute('selected')):
                    driver.find_element(By.CSS_SELECTOR, 'select[id="arretierung"] :nth-child(2)').click()
                    time.sleep(1)

                if not driver.find_element(By.ID , '_weiss').is_selected():
                    driver.find_element(By.ID , '_weiss').click()
                
                driver.find_element(By.NAME, 'berechnePreis').click()

                price = driver.find_elements(By.TAG_NAME, ('strong'))[1].text.strip()[:-1].replace('.', ',')
                self.df_armor.loc[index*10, column*10] = price
                driver.find_element(By.CSS_SELECTOR, 'a[title="Eingaben ändern"]').click()


    def generate_index_and_columns(self):
        height_min = 10
        height_max = 800

        if self.type == '39':
            width_min = 35
            width_max = 280            
        elif self.type == '52':
            width_min = 35
            width_max = 400
        elif self.type == '77':
            width_min = 35
            width_max = 450

        index_list = [i for i in range(height_min, height_max + 10, 10)]
        column_list = [math.floor(i/10)*10 for i in range(width_min, width_max + 10, 10)]        
        column_list[0] = 35

        return index_list, column_list