# PickNPull Notification System

A Python-based webscraper that fetches vehicle information from the PickNPull website and notifies users via email and SMS about new vehicle postings.

## Version

2.0.0

## Author

Gurpreet Singh Bassan

## License

MIT

## Dependencies

-   python>=3.8
-   requests
-   python-dotenv

## Files

-   **webscraper.py**: The main script which fetches vehicle information and stores it in a JSON file. It also identifies new vehicles and triggers email and SMS notifications.
-   **email_smtp.py**: A helper script to send email and SMS notifications using SMTP.

## Usage

To use the PickNPull Notification System, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/GSinghh/pick-n-pull
    cd pick-n-pull
    ```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project root directory and add your email credential, phone number and carrier information:

    ```env
    EMAIL_ADDRESS=Your Gmail address
    EMAIL_PASSWORD=Google App Password
    ```

    - `EMAIL_ADDRESS` must be a gmail address since thats what SMTP utilizes
    - `EMAIL_PASSWORD` must be a gmail app password since google no longer allows signing in with your normal password for less secure apps. i.e. Python Apps

    ```env
    PHONE_NUMBER=Your Phone Number
    CARRIER=Name of Your Mobile Carrier
    ```

    - `PHONE_NUMBER` Mobile phone number with no dashes or spaces
    - `CARRIER` Name of your Carrier, must match a carrier within `email_smtp.py`

4. Instantiate a PickNPull object within `webscraper.py`:

    ```python
    PickNPull(make, model, postal_code, distance, start_year, end_year)
    ```

    - `make` Brand of the vehicle you're searching for \***Must Be in makes.json\***
    - `model` Model of the vehicle you're searching for \***Must Be in models.json\***
    - `postal_code` The Zip Code for the area you're searching
    - `distance` Radius in Miles
    - `start_year` The starting year for your search (Can be left empty)
    - `end_year` The ending year for your search (Can be left empty)

5. Run the `webscraper.py` script:
    ```sh
    python webscraper.py
    ```
