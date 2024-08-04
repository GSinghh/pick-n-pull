#!/usr/local/bin/python3

import os
import json
import email_smtp
import requests
from datetime import datetime


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
            results = self.get_vehicle_information()
            self.store_data_in_file(results, file_name)
        else:
            prev_results = self.load_data_from_file(file_name)
            new_results = self.get_vehicle_information()
            if new_results != prev_results:
                new_vehicles = self.identify_change(new_results, prev_results)
                email_smtp.send_email(new_vehicles)
                self.store_data_in_file(new_results, file_name)

    def URL_builder(self):
        makes = self.load_data_from_file("makes.json")
        models = self.load_data_from_file("models.json")

        if self.make not in makes:
            return "Vehicle Not Found"
        if self.model not in models:
            return "Brand Not Found"

        return f"https://www.picknpull.com/api/vehicle/search?&makeId={makes[self.make]}&modelId={models[self.model]}&year={self.validate_years()}&distance={self.distance}&zip={self.postal_code}&language=english"

    def store_data_in_file(self, data, filename):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_data_from_file(self, filename):
        with open(filename) as file:
            return json.load(file)

    def validate_years(self):
        if self.start_year == "" and self.end_year == "":
            return ""
        elif self.start_year != "" and self.end_year == "":
            return self.start_year
        elif self.start_year == "" and self.end_year != "":
            return self.end_year
        else:
            return f"{self.start_year}-{self.end_year}"

    def get_vehicle_information(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
        }
        response = requests.get(self.URL_builder(), headers).json()
        return self.parse_json_data(response)

    def parse_json_data(self, locations):
        vals = {}
        for data in locations:
            location = data["location"].get("name", "Name Not Found")
            vehicles = data["vehicles"]
            vehicle_info = []
            for vehicle in vehicles:
                vin = vehicle.get("vin", "Unknown VIN")
                link_to_post = (
                    f"https://www.picknpull.com/check-inventory/vehicle-details/{vin}"
                )
                year = vehicle.get("year", "Unknown Year")
                model = vehicle.get("model", "Unknown Model")
                make = vehicle.get("make", "Unknown Make")
                row = vehicle.get("row", "Unknown Row")
                image_url = vehicle.get("largeImage", "Image URL Unavailable")
                date_added = vehicle.get("dateAdded", "Date Not Found")
                if date_added:
                    date_added = self.format_date(date_added)
                car = f"{year} {make} {model}"
                vehicle_info.append(
                    {
                        "Car": car,
                        "VIN": vin,
                        "Row": row,
                        "Link": link_to_post,
                        "Image URL": image_url,
                        "Date Added": date_added,
                    }
                )
            vehicle_info.sort(
                key=lambda vehicle: vehicle.get("Date Added"), reverse=True
            )
            vals[location] = vehicle_info
        return vals

    def format_date(self, date):
        date_vals = datetime.fromisoformat(date)
        return f"{date_vals.month}-{date_vals.day}-{date_vals.year}"

    def identify_change(self, new_results, prev_results):
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
