import time
import math
import pandas as pd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class ScrapRollerThread(Thread):
    def __init__(self, type='rollladen39', with_motor=False, with_net=False):
        Thread.__init__(self)
        self.df_roller = pd.DataFrame()
        self.type = type
        self.with_motor = with_motor
        self.with_net = with_net

    def link_to_product(self):
        link = ''
        match self.type:
            case 'rollladen39':
                link = 'https://www.rollorieper.de/montage_auswahl.php?artikel=rolladen39'
            case 'rollladen52':
                link = 'https://www.rollorieper.de/montage_auswahl.php?artikel=rolladen52'
            case 'rollladen77':
                link = 'https://www.rollorieper.de/montage_auswahl.php?artikel=rolladen77'
            
        return link
 
    def run(self):
        time.sleep(1)
        driver = webdriver.Chrome()
        driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": ["https://uct.service.usercentrics.eu/", 'https://privacy-proxy.usercentrics.eu', 'https://app.usercentrics.eu/']})
        driver.execute_cdp_cmd('Network.enable', {})
        driver.get(self.link_to_product())

        time.sleep(2)
        if self.type != 'rollladen52':
            row = driver.find_elements(By.CSS_SELECTOR, 'div[class="row well"]')[0]
            
        else:
            row = driver.find_elements(By.CSS_SELECTOR, 'div[class="row well"]')[1]
        row.find_element(By.CSS_SELECTOR, 'a[class="btn btn-primary btn-block green"]').click()
        time.sleep(1)

        index_list, column_list = self.generate_index_and_columns()
        height_input = driver.find_element(By.ID, 'hoehe')
        width_input = driver.find_element(By.ID, 'breite')

        if (self.type == 'rollladen39' or self.type == 'rollladen52') and not self.with_motor:
            column_list[0] = 35

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
                    case 'rollladen39':
                        max_square = 60000
                    case 'rollladen52':
                        max_square = 80000
                    case 'rollladen77':
                        max_square = 150000
                    
                if (column * index) > max_square:
                    break
                
                width_input.send_keys(Keys.CONTROL, 'a')
                width_input.send_keys(column)
                height_input = driver.find_element(By.ID, 'hoehe')
                height_input.send_keys(Keys.TAB)

                time.sleep(1)
                if self.type != 'rollladen77':
                    try:
                        self.choose_selects_39_52(driver)
                    except:
                        print('Brak napędu ręcznego')
                        break
                else:
                    self.choose_selects_77(driver)

                time.sleep(0.5)
                if self.type != 'rollladen77':
                    if not driver.find_element(By.ID , '_weiss').is_selected():
                        driver.find_element(By.ID , '_weiss').click()
                else:
                    if not driver.find_element(By.ID , '_02').is_selected():
                        driver.find_element(By.ID , '_02').click()

                time.sleep(0.5)            
                 
                driver.find_element(By.NAME, 'berechnePreis').click()

                time.sleep(1)

                try:
                    driver.execute_script('scrollBy(0,200)')
        
                    driver.find_element(By.CSS_SELECTOR, 'a[title="Eingaben ändern"]')
                except:
                    print('nie znaleziono powrotu')
                    driver.back()
                    break

                if self.type != 'rollladen77':
                    price = driver.find_elements(By.TAG_NAME, ('strong'))[1].text.strip()[:-1].replace('.', ',')
                else:
                    price = driver.find_elements(By.CSS_SELECTOR, ('div[class*="text-right"]'))[-2].text.strip()[:-1].replace('.', ',')
                    driver.execute_script('scrollBy(0,400)')

                print(price)
                self.df_roller.loc[index*10, column*10] = price

                time.sleep(1)                

                driver.find_element(By.CSS_SELECTOR, 'a[title="Eingaben ändern"]').click()
                driver.execute_script('scrollTo(0,0)')

                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, 'hoehe'))
                )
                
        driver.quit()



    def choose_selects_77(self, driver):
        seconds = 1
        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="antrieb"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="antrieb"] :nth-child(2)').click()
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'jqloader')))
            WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.ID, 'jqloader')))

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="antriebsbedienung"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="antriebsbedienung"] :nth-child(2)').click()
            time.sleep(seconds)

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="bedienseite"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="bedienseite"] :nth-child(2)').click()
            time.sleep(seconds)

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="kastenfarbe"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="kastenfarbe"] :nth-child(2)').click()
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'jqloader')))
            WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.ID, 'jqloader')))

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="schienenfarbe"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="schienenfarbe"] :nth-child(2)').click()
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'jqloader')))
            WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.ID, 'jqloader')))


    def choose_selects_39_52(self, driver):
        seconds = 1
        if self.type == 'rollladen39' and self.with_net:
            print('siatka')
            try:
                if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="modell"] > option[value="Eckiger Kasten mit Insektenschutz"]').get_attribute('selected')):
                    driver.find_element(By.CSS_SELECTOR, 'select[id="modell"] > option[value="Eckiger Kasten mit Insektenschutz"]').click()
                    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'jqloader')))
                    WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.ID, 'jqloader')))
            except:
                raise Exception
        else:
            if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="modell"] > option[value="Eckiger Kasten"]').get_attribute('selected')):
                driver.find_element(By.CSS_SELECTOR, 'select[id="modell"] > option[value="Eckiger Kasten"]').click()
                WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'jqloader')))
                WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.ID, 'jqloader')))

        if not self.with_motor:
            try:
                if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="antriebkategorie"] > option[value="Manuell"]').get_attribute('selected')):
                    driver.find_element(By.CSS_SELECTOR, 'select[id="antriebkategorie"] > option[value="Manuell"]').click()
                    time.sleep(seconds)
            except:
                raise Exception
        else:
            if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="antriebkategorie"] > option[value="EcoLine - Motor"]').get_attribute('selected')):
                driver.find_element(By.CSS_SELECTOR, 'select[id="antriebkategorie"] > option[value="EcoLine - Motor"]').click()
                time.sleep(seconds)

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="antrieb"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="antrieb"] :nth-child(2)').click()
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'jqloader')))
            WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.ID, 'jqloader')))

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="antriebsbedienung"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="antriebsbedienung"] :nth-child(2)').click()
            time.sleep(seconds)

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="variante"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="variante"] :nth-child(2)').click()
            time.sleep(seconds)

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="variante"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="variante"] :nth-child(2)').click()
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'jqloader')))
            WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.ID, 'jqloader')))

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="bedienseite"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="bedienseite"] :nth-child(2)').click()
            time.sleep(seconds)

        time.sleep(seconds)
        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="arretierung"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="arretierung"] :nth-child(2)').click()
            time.sleep(seconds)

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="kastenfarbe"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="kastenfarbe"] :nth-child(2)').click()
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'jqloader')))
            WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.ID, 'jqloader')))

        if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="schienenfarbe"] :nth-child(2)').get_attribute('selected')):
            driver.find_element(By.CSS_SELECTOR, 'select[id="schienenfarbe"] :nth-child(2)').click()
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'jqloader')))
            WebDriverWait(driver, 10).until_not(ec.visibility_of_element_located((By.ID, 'jqloader')))

        if not self.with_motor:
            if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="gurtfarbe"] :nth-child(2)').get_attribute('selected')):
                driver.find_element(By.CSS_SELECTOR, 'select[id="gurtfarbe"] :nth-child(2)').click()
                time.sleep(seconds)

            if not bool(driver.find_element(By.CSS_SELECTOR, 'select[id="gurtwicklerfarbe"] :nth-child(2)').get_attribute('selected')):
                driver.find_element(By.CSS_SELECTOR, 'select[id="gurtwicklerfarbe"] :nth-child(2)').click()
                time.sleep(seconds)


    def generate_index_and_columns(self):
        height_min = 10

        if not self.with_net:
            if self.type == 'rollladen39' and not self.with_motor:
                width_min = 35
                width_max = 300
                height_max = 350
            elif self.type == 'rollladen39' and self.with_motor:
                width_min = 60
                width_max = 300
                height_max = 350
            elif self.type == 'rollladen52' and not self.with_motor:
                width_min = 35
                width_max = 360
                height_max = 340
            elif self.type == 'rollladen52' and self.with_motor:
                height_min = 10
                width_min = 60
                width_max = 360
                height_max = 340
            elif self.type == 'rollladen77':
                width_min = 60
                width_max = 450
                height_max = 450
        else:
            if self.with_motor:
                width_min = 60
                width_max = 160
                height_max = 240
            else:
                width_min = 35
                width_max = 160
                height_max = 240

        index_list = [i for i in range(height_min, height_max + 10, 10)]
        column_list = [math.floor(i/10)*10 for i in range(width_min, width_max + 10, 10)]        

        return index_list, column_list