from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import time
import os
import json

class PickNPull:
    def __init__(self, make, model, postal_code, distance, start_year = '', end_year = '') -> None:
        self.start_year = start_year
        self.end_year = end_year
        self.postal_code = postal_code
        self.distance = distance
        self.make = make
        self.model = model
        self.models = {}
        self.makes = {}
        self.allCars = {}
        
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
        if os.path.isfile('makes.json') and os.path.isfile('models.json'):
            self.models = self.load_data_from_file('models.json')
            self.makes = self.load_data_from_file('makes.json')
        else:
            self.get_makes_and_models()

        self.get_car_information()
    
    """
        This function grabs all makes and models from the dropdown menus
        Values are stored in the dictionary
        Dictionary is saved into json document so dropdowns will only 
        Need to be parsed once
    """
    
    
    def get_makes_and_models(self):
        # Initializing webdriver
        driver = self.driver
        driver.get("https://picknpull.com/check-inventory/")
        
        ignored_exception = (StaleElementReferenceException, NoSuchElementException)
        wait = WebDriverWait(driver, 50, ignored_exceptions=ignored_exception)
        
        brands_location = '//*[@id="main-content"]/div[1]/app-vehicle-search-controls/div/div/div/div[1]/div[1]/select'
        models_location = '//*[@id="main-content"]/div[1]/app-vehicle-search-controls/div/div/div/div[1]/div[2]/select'
        
        brands = self.locate_element(brands_location, wait)
        
        for i in range(1, len(brands.options)):
            # Iterating through each index in brand dropdown
            # Allows models to be stored for each brand
            brands.select_by_index(i)
            self.store_brands(brands.options[i])
            time.sleep(.25)
            
            # Grabbing all models for that brand
            models_select = self.locate_element(models_location, wait)
            self.store_models(models_select)

            self.store_data_in_file(self.makes, 'makes.json')
            self.store_data_in_file(self.models, 'models.json')
        driver.quit()
        
    def URL_builder(self):
        # This function will generate a URL that the driver will use to find the vehicle its looking for
        
        if self.make not in self.makes:
            return "Vehicle Not Found"
        if self.model not in self.models:
            return "Brand Not Found"
        
        return f"https://picknpull.com/check-inventory?make={self.makes[self.make]}&model={self.models[self.model]}&distance={self.distance}&zip={self.postal_code}&year={self.check_years()}"
            
    def locate_element(self, element_location, wait, attempts = 3):
        for attempt in range(attempts):
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH, element_location)))       
                element_select = Select(element)
                return element_select
            except StaleElementReferenceException:
                if attempt == 3:
                    print(f"Element not found after {attempts} attemmpts")
            
    def store_models(self, models_select):
        for j in range(1, len(models_select.options)):
            model = models_select.options[j]
            try:
                self.models[model.text] = model.get_attribute('value')
            except StaleElementReferenceException:
                print("Error When Storing Model")
                
    def store_brands(self, brand):
        try:
            self.makes[brand.text] = brand.get_attribute('value')
        except StaleElementReferenceException:
            print("Error When Storing Brand")
        
    def store_data_in_file(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)
            
    def load_data_from_file(self, filename):
        with open(filename) as file:
            return json.load(file)
        
        
    def check_years(self):
        if self.start_year == '' and self.end_year == '':
            return ''
        elif self.start_year != '' and self.end_year == '':
            return self.start_year
        else:
            return self.start_year + '-' + self.end_year
        
    def get_car_information(self):
        driver = self.driver
        driver.get(self.URL_builder())
        self.remove_modal(driver)
        
        
        search_button_location = '/html/body/app-root/div/div/div/app-check-inventory/app-home/div/div/div[1]/app-vehicle-search-controls/div/div/div/div[3]/div[2]/input'
        search_button = driver.find_element(By.XPATH, search_button_location)
        search_button.click()
        
        results_location = '//span[@id="resultsList"]'
        car_results = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, results_location)))
        
        for result in car_results:
            anchor_tag_location = './/a'
            location = result.find_element(By.XPATH, anchor_tag_location).text
            tbody_location = './/tbody'
            tbody = result.find_element(By.XPATH, tbody_location)
            rows = tbody.find_elements(By.XPATH, './/tr')
            tr_number = 1
            vehicles = []
            for row in rows:
                year = row.find_element(By.XPATH, f'//*[@id="resultsList"]/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[{tr_number}]/td[2]').text
                make = row.find_element(By.XPATH, f'//*[@id="resultsList"]/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[{tr_number}]/td[3]').text
                model = row.find_element(By.XPATH, f'//*[@id="resultsList"]/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[{tr_number}]/td[4]').text
                row_number = row.find_element(By.XPATH, f'//*[@id="resultsList"]/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[{tr_number}]/td[5]').text
                image_url = row.find_element(By.XPATH, f'//*[@id="resultsList"]/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[{tr_number}]/td[1]/img').get_attribute('src')
                tr_number += 1
                vehicle = year + ' ' + make + ' ' + model
                vehicles.append({'Car': vehicle,
                                 'Row Number': row_number, 
                                 'Image URL': image_url})
                
            self.allCars[location] = vehicles
        driver.quit()
        
    def remove_modal(self, driver):
        try:
            modal_button_location = '/html/body/app-root/div/div/div/app-check-inventory/app-home/div/div/div[1]/div[2]/div/div/div[1]/div/div'
            modal_button = driver.find_element(By.XPATH, modal_button_location)
            modal_button.click()
        except NoSuchElementException:
            print("Modal not found, Skipping step")
        
test = PickNPull("Acura", "Integra", 94560, 25, "94", "01")