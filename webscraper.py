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
    
    
    # This function will grab each brand and value from the drop down
    # Stores them in the makes dictionary
    def get_makes_and_models(self):
        # Initializing driver variable and grabbing URL 
        driver = self.driver
        driver.get("https://picknpull.com/check-inventory/")
        
        ignored_exceptions = (StaleElementReferenceException, NoSuchElementException)
        wait = WebDriverWait(driver, 30, ignored_exceptions=ignored_exceptions)
        
        brands = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/app-vehicle-search-controls/div/div/div/div[1]/div[1]/select')
        brands = Select(brands)
        
        for i in range(1, len(brands.options)):
            brand = brands.options[i]
            brand_val = brand.get_attribute('value')
            self.makes[brand.text] = brand_val
            brands.select_by_value(brand_val)
            # Initial value should not be changed as we are looping over these values
            # Wait for the models dropdown to be refreshed
            
            models = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                         '#main-content > div.check_inventory > app-vehicle-search-controls > div > div > div > div:nth-child(1) > div:nth-child(2) > select')))
            models = Select(models)
            # for i in range(1, len(models.options)):
            #     model = models.options[i]
            #     model_val = model.get_attribute('value')
            #     models.select_by_value(model_val)
        # print(self.models)
        
        
            
           
        
        
        
test = PickNPull("Acura", "Integra", "94", "01", 94560, 50)
test.get_makes_and_models()