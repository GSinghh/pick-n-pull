from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager


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
    
    
    # This function will grab each brand from the drop down
    # Stores them in the makes hashmap
    # Remove {'Choose Model: 0}
    def get_makes(self):
        driver = self.driver
        driver.get("https://picknpull.com/check-inventory/")
        brands = Select(driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/app-vehicle-search-controls/div/div/div/div[1]/div[1]/select'))
        for brand in brands.options:
            self.makes[brand.text] = brand.get_attribute('value')
        print(self.makes)
        
        
    # This function will grab each model from the drop down
    # Stores them in the models hashmap
    def get_models(self):
        driver = self.driver
        driver.get("https://picknpull.com/check-inventory/")
        
        
 