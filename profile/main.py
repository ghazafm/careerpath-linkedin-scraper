import os
from dotenv import load_dotenv
from helper import login, start_chrome_with_debug
from helper import load_cookies
from helper import save_to_json
from selenium import webdriver
from scrape import scrape_profile, extract_more_profiles


def main():
    load_dotenv()
    # driver = webdriver.Chrome()
    driver = start_chrome_with_debug()

    # driver.get('https://www.linkedin.com')

    profile_url = "https://www.linkedin.com/in/fauzanghaza"
    number_of_profiles = int(os.getenv('NUMBER_PROFILE_DISCOVERIES'))

    profile_data = []
    profile_discovered = []

    for i in range(number_of_profiles):
        print(f"Profil number: {i+1}")
        if profile_url not in profile_discovered:
            profile_info = scrape_profile(
                driver, profile_url, visited_profiles=profile_discovered
            )
            profile_data.append(profile_info)  # Append the profile data to the list
            profile_discovered.append(profile_url)
            profile_url = extract_more_profiles(driver)

    # Save the collected data
    save_to_json(profile_data)

    driver.quit()


if __name__ == "__main__":
    main()
