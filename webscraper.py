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
        #Initializing driver variable and grabbing URL 
        driver = self.driver
        driver.get("https://picknpull.com/check-inventory/")
        
        ignored_exceptions = (StaleElementReferenceException, NoSuchElementException)
        wait = WebDriverWait(driver, 10, ignored_exceptions)
        # brands = Select(wait.until(EC.visibility_of_element_located(By.XPATH, '//*[@id="main-content"]/div[1]/app-vehicle-search-controls/div/div/div/div[1]/div[1]/select'))
        brands = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content"]/div[1]/app-vehicle-search-controls/div/div/div/div[1]/div[1]/select')))
        brands = Select(brands)
        for brand in brands.options:
            # Since there is a placeholder value within the first option of the list
            # We ignore that with this condition
            brand_val = brand.get_attribute('value')
            if brand_val != "0":
                self.makes[brand.text] = brand_val
                # Select the brand from dropdown
                brands.select_by_value(brand_val)
                
                # Re-locate models dropdown after selecting the brand
                models = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/div/div/div/app-check-inventory/app-home/div/div/div[1]/app-vehicle-search-controls/div/div/div/div[1]/div[2]/select')))
                models = Select(models)
                
                # for model in models.options:
                #     model_val = model.get_attribute('value')
                #     if model_val != "0":
                #         print(f"This is the model_val: {model_val}")
                        
                #         print(f"This is the model name: {model.text}")
            
            
            
            
           
        
        
        
test = PickNPull("Acura", "Integra", "94", "01", 94560, 50)
test.get_makes_and_models()