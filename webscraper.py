from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
    
    

    def get_makes_and_models(self):
        self.driver.get("https://picknpull.com/check-inventory/")