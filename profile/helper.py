import os
import time
import json
import pickle
from pymongo import MongoClient
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


timeout = 2
# Login & Scroll


def login(driver):

    load_dotenv()
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    username = get_object(driver, By.ID, "username")
    print(username)
    username.send_keys(email)

    # time.sleep(100)
    password_element = get_object(
        driver,
        By.XPATH,
        "//input[@id='password' and @name='session_password' and @type='password']",
    )
    password_element.send_keys(password)

    login_button = get_object(driver, By.CLASS_NAME, "btn__primary--large")
    login_button.click()


def scroll_and_load(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Pause to allow loading

        # Try to click the "Show more results" button if it exists
        try:
            show_more_button = driver.find_element(
                By.XPATH,
                "//button[contains(@class, 'scaffold-finite-scroll__load-button')]",
            )
            if show_more_button:
                show_more_button.click()
                time.sleep(2)  # Give some time for new results to load
        except NoSuchElementException:
            pass  # Continue if no button is found

        # Check if the page height has stopped increasing
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Getter setter


def wait_element(driver, by, element, timeout=timeout) -> None:
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, element)))


def get_element(driver, by, element, timeout=timeout):
    return driver.find_element(by, element)


def get_elements(driver, by, element, timeout=timeout):
    return driver.find_elements(by, element)


def get_object(driver, by, element, timeout=timeout):
    wait_element(driver, by, element, timeout)
    return get_element(driver, by, element)


def get_objects(driver, by, element, timeout=timeout):
    wait_element(driver, by, element, timeout)
    return get_elements(driver, by, element)


# Extractor


def extract_element_text(driver, by, element, timeout=timeout):
    try:
        return get_object(driver, by, element, timeout=timeout).text.strip()
    except NoSuchElementException:
        return "Not available"


def extract_many_element_text(driver, by, element, timeout=timeout):
    try:
        items = get_objects(driver, by, element, timeout=timeout)
        temp = []
        for i in items:
            temp.append(i.text.strip())

        return temp
    except NoSuchElementException:
        return "Not available"


def extract_element_attribute(driver, by, element, attribute):
    try:
        return get_object(driver, by, element, timeout=timeout).get_attribute(attribute)
    except NoSuchElementException:
        return "Not available"


def extract_many_element_attribute(driver, by, element, attribute):
    try:
        items = get_objects(driver, by, element, timeout=timeout)
        temp = []
        for i in items:
            temp.append(i.get_attribute(attribute))
        return temp
    except NoSuchElementException:
        return "Not available"


def save_to_json(data, filename="scraped_profiles.json"):
    """Saves the extracted profile data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_mongo(data):
    """Saves the extracted profile data to a MongoDB collection."""
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    collection_name = os.getenv("MONGO_COLLECTION")

    # Establish MongoDB connection
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Insert data into the MongoDB collection
    if isinstance(data, list):
        collection.insert_many(data)  # Insert a list of profiles
    else:
        collection.insert_one(data)  # Insert a single profile

    print(f"Data successfully saved to MongoDB collection: {collection_name}")


def import_json_to_mongo(
    json_file_path, db_name, collection_name, mongo_uri="mongodb://localhost:27017/"
):
    """
    Import a JSON file into a MongoDB collection.

    :param json_file_path: Path to the JSON file to import.
    :param db_name: Name of the MongoDB database.
    :param collection_name: Name of the collection within the MongoDB database.
    :param mongo_uri: URI of the MongoDB server. Defaults to localhost.
    """
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Load the JSON data
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Insert data into the collection
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

    print(f"Data successfully imported into {db_name}.{collection_name}")


def save_cookies(driver, filepath):
    with open(filepath, "wb") as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookies(driver, filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
    else:
        print("Cookies file not found, logging in again...")


def start_chrome_with_debug():
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "debuggerAddress", "127.0.0.1:9222"
    )  # Connect to the remote-debugging Chrome
    driver = webdriver.Chrome(options=chrome_options)
    return driver
