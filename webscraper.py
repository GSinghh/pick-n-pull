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

class PickNPull:
    def __init__(self, make, model, start_year, end_year, postal_code, distance) -> None:
        self.start_year = start_year
        self.end_year = end_year
        self.postal_code = postal_code
        self.distance = distance
        self.models = {}
        self.makes = {}
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    
    # This function grabs all makes and models from the dropdown menus
    # Values are stored to be used later to generate URL 
    
    def get_makes_and_models(self):
        # Initializing webdriver
        driver = self.driver
        driver.get("https://picknpull.com/check-inventory/")
        
        ignored_exception = (StaleElementReferenceException, NoSuchElementException)
        wait = WebDriverWait(driver, 50, ignored_exceptions=ignored_exception)
        
        brands_location = '//*[@id="main-content"]/div[1]/app-vehicle-search-controls/div/div/div/div[1]/div[1]/select'
        models_location = '//*[@id="main-content"]/div[1]/app-vehicle-search-controls/div/div/div/div[1]/div[2]/select'
        
        brands = driver.find_element(By.XPATH, brands_location)
        brands = Select(brands)
        
        for i in range(1, 5):
            brands.select_by_index(i)
            time.sleep(.5)
            # Grabbing all models for that brand
            models = driver.find_element(By.XPATH, models_location)
            models_select = Select(models)
            for j in range(1, len(models_select.options)):
                model = models_select.options[j].text
                print(model)
                
                
            brand = brands.options[i]
            brand_val = brand.get_attribute('value')
            self.makes[brand.text] = brand_val
            
            
        driver.quit()
        
    def store_models(self, models):
        for i in range(1, len(models.options) + 1):
            model = models.options[i]
            model_val = model.get_attribute('value')
            self.models[model] = model_val
            
           
        
        
        
test = PickNPull("Acura", "Integra", "94", "01", 94560, 50)
test.get_makes_and_models()