import os
from dotenv import load_dotenv
from helper import login, save_cookies, load_cookies
from selenium import webdriver
from profile.scrape1 import scrape_profile, extract_more_profiles

def main():
    load_dotenv()
    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com/login')
    cookies_path = "linkedin_cookies.pkl"
    
    # Check if we are logged in by visiting the LinkedIn home page
    driver.get('https://www.linkedin.com/feed/')
    
    # If login page is still shown, login manually and save cookies
    if "login" in driver.current_url:
        login(driver)  # Perform login manually
        save_cookies(driver, cookies_path)  # Save cookies after login
    
    input("Press Enter after login...")
    driver.quit()

if __name__ == "__main__":
    main()
