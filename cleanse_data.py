def parse_json_data(locations):
    vals = {}
    for data in locations:
        location = data["location"].get("name", "Name Not Found")
        vehicles = data["vehicles"]
        vehicle_info = []
        for vehicle in vehicles:
            vin = vehicle.get("vin", "Unknown VIN")
            link = f"https://www.picknpull.com/check-inventory/vehicle-details/{vin}"
            year = vehicle.get("year", "Unknown Year")
            model = vehicle.get("model", "Unknown Model")
            make = vehicle.get("make", "Unknown Make")
            row = vehicle.get("row", "Unknown Row")
            image_url = vehicle.get("largeImage", "Image URL Unavailable")
            car = f"{year} {make} {model}"
            vehicle_info.append(
                {
                    "car": car,
                    "vin": vin,
                    "row": row,
                    "link": link,
                    "Image URL": image_url,
                }
            )
        vals[location] = vehicle_info
    return vals
