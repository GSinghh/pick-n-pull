import os
import json
from datetime import datetime
import email_smtp
import requests


class PickNPull:
    def __init__(
        self, make, model, postal_code, distance, start_year="", end_year=""
    ) -> None:
        self.start_year = start_year
        self.end_year = end_year
        self.postal_code = postal_code
        self.distance = distance
        self.make = make
        self.model = model

        file_name = f"{self.make}_{self.model}.json"
        if not os.path.isfile(file_name):
            results = self.get_car_information()
            self.store_data_in_file(results, file_name)
        else:
            prev_results = self.load_data_from_file(file_name)
            new_results = self.get_car_information()
            if new_results != prev_results:
                new_vehicles = self.identify_change(new_results, prev_results)
                email_smtp.send_email(new_vehicles)
                self.store_data_in_file(new_results, file_name)

    """
        This function grabs all makes and models from the dropdown menus
        Values are stored in the dictionary
        Dictionary is saved into json document so dropdowns will only 
        Need to be parsed once
    """

    def URL_builder(self):

        makes = self.load_data_from_file("makes.json")
        models = self.load_data_from_file("models.json")

        if self.make not in makes:
            return "Vehicle Not Found"
        if self.model not in models:
            return "Brand Not Found"

        return f"https://www.picknpull.com/api/vehicle/search?&makeId={self.makes[self.make]}&modelId={self.models[self.model]}&year={self.check_years()}&distance={self.distance}&zip={self.postal_code}&language=english"

    def store_data_in_file(self, data, filename):
        with open(filename, "w") as file:
            json.dump(data, file)

    def load_data_from_file(self, filename):
        with open(filename) as file:
            return json.load(file)

    def check_years(self):
        if self.start_year == "" and self.end_year == "":
            return ""
        elif self.start_year != "" and self.end_year == "":
            return self.start_year
        else:
            return self.start_year + "-" + self.end_year

    def get_car_information(self):
        raw_data = requests.get(self.URL_builder())
        print(raw_data)

    def identify_change(self, new_results, prev_results):
        # This function will identify change between the previous results and the current results after scraping
        # It will return a dictionary with the new vehicles and their locations
        changes = {}

        for key in new_results:
            if key not in prev_results:
                changes[key] = new_results[key]
            elif len(new_results[key]) > len(prev_results[key]):
                new_cars = [
                    car for car in new_results[key] if car not in prev_results[key]
                ]
                if new_cars:
                    changes[key] = new_cars

        return changes


test = PickNPull("Acura", "Integra", 94560, 50, "94", "01")
