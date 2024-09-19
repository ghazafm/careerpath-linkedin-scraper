from helper import login
from helper import get_object
from helper import get_element
from helper import wait_element
from helper import find_job_profile
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


# Setup WebDriver
driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')

# Login to LinkedIn
login(driver)

input("Press Enter if already login and answering captcha.....")

wait_element(driver, By.CLASS_NAME, "ivm-view-attr__img-wrapper")
# Navigate to the profile page
profile_url = "https://www.linkedin.com/in/fauzanghaza/"
driver.get(profile_url)

# Scroll down to load dynamic content
start = time.time()

# Initial scroll values
initialScroll = 0
finalScroll = 1000

# Scroll the page dynamically for 20 seconds to load content
while True:
    driver.execute_script(f'window.scrollTo({initialScroll},{finalScroll})')
    initialScroll = finalScroll
    finalScroll += 1000
    time.sleep(2)  # Adjust based on internet speed

    end = time.time()
    if round(end - start) > 20:  # Scroll for 20 seconds
        break

# Extract the updated page source after scrolling
src = driver.page_source


# time.sleep(1000)
# Intro
try:
    # Wait for the intro section to load
    intro = driver.find_element(By.CLASS_NAME, 'mt2.relative')

    if intro:
        # Extract name
        name = intro.find_element(By.TAG_NAME, 'h1').text.strip()

        # Extract company/workplace
        works_at = intro.find_element(By.CLASS_NAME, 'text-body-medium').text.strip()

        # Extract location
        location = intro.find_elements(By.CLASS_NAME, 'text-body-small.inline.t-black--light.break-words')[0].text.strip()

        print(f"Name: {name}")
        print(f"Works At: {works_at}")
        print(f"Location: {location}")
    else:
        print("Intro section not found")

except NoSuchElementException as e:
    print(f"Error extracting intro: Element not found - {e}")
except Exception as e:
    print(f"Error extracting intro: {e}")
    
# About
try:
    xpath_about = "//section[contains(@class, 'artdeco-card pv-profile-card')]//h2[span[text()='About']]/ancestor::section//div[contains(@class, 'full-width')]//span[@aria-hidden='true']"
    
    about_description = driver.find_element(By.XPATH, xpath_about).text.strip()
    
    print(f"About: {about_description}")
except Exception as e:
    print(f"Error extracting 'About' section: {e}")
    
    
# Experience
driver.get(profile_url + '/details/experience/')

# Find the experience list container
experience_list = driver.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item")

# Iterate over each experience item
for experience in experience_list.find_all('li', {"class": "pvs-list__paged-list-item"}):
    try:
        # Extract job title
        job_title_element = experience.find_element(By.XPATH, ".//div[contains(@class,'t-bold')]")
        job_title = job_title_element.text

        # Extract company name
        company_name_element = experience.find_element(By.XPATH, ".//span[contains(@class, 'hoverable-link-text')]")
        company_name = company_name_element.text

        # Extract duration
        duration_element = experience.find_element(By.XPATH, ".//span[contains(@class, 't-black--light')][1]")
        duration = duration_element.text

        # Extract location
        location_element = experience.find_element(By.XPATH, ".//span[contains(@class, 't-black--light')][2]")
        location = location_element.text

        # Print the extracted data
        print(f"Job Title: {job_title}")
        print(f"Company: {company_name}")
        print(f"Duration: {duration}")
        print(f"Location: {location}")
        print("=" * 50)

    except Exception as e:
        print(f"Error extracting data for one experience: {e}")



# Education
driver.get(profile_url)
education_section = driver.find_element(By.CLASS_NAME, "MhGRIvJrtQxHgIhvUXjiSWWUlBvalavdjEnRipQ")

# Extract university name
university_element = education_section.find_element(By.XPATH, ".//a[contains(@href, 'company')]//div[contains(@class,'hoverable-link-text')]")
university_name = university_element.text

# Extract degree and field of study
degree_element = education_section.find_element(By.XPATH, ".//span[contains(text(), \"Bachelor's degree\")]")
degree = degree_element.text

# Extract graduation year
year_element = education_section.find_element(By.XPATH, ".//span[@class='t-black--light'][1]")
graduation_year = year_element.text

# Extract skills if available
skills_element = education_section.find_element(By.XPATH, ".//strong")
skills = skills_element.text

# Print the extracted data
print(f"University: {university_name}")
print(f"Degree: {degree}")
print(f"Graduation Year: {graduation_year}")
print(f"Skills: {skills}")


# Certificate
driver.get(profile_url + '/details/certifications/')

certifications = driver.find_elements(By.XPATH, "//ul[contains(@class, 'GwDizhdSHYPkIbgBuMBRdRJgYmpMKyoUqjqU')]/li")

# Loop through each certification and extract details
for cert in certifications:
    # Extract certification name
    cert_name = cert.find_element(By.XPATH, ".//span[@aria-hidden='true']").text
    print("Certification Name:", cert_name)
    
    # Extract issuer (if available)
    try:
        issuer = cert.find_element(By.XPATH, ".//span[@aria-hidden='true'][2]").text
        print("Issuer:", issuer)
    except:
        print("Issuer: Not available")
    
    # Extract the date issued (if available)
    try:
        date_issued = cert.find_element(By.XPATH, ".//span[contains(@class, 'pvs-entity__caption-wrapper')]").text
        print("Date Issued:", date_issued)
    except:
        print("Date Issued: Not available")
    
    # Extract credential link (if available)
    try:
        credential_link = cert.find_element(By.XPATH, ".//a[contains(@aria-label, 'Show credential')]").get_attribute("href")
        print("Credential Link:", credential_link)
    except:
        print("Credential Link: Not available")

    print("\n")

# projects
driver.get(profile_url + '/details/projects/')

projects = driver.find_elements(By.XPATH, "//ul[@class='GwDizhdSHYPkIbgBuMBRdRJgYmpMKyoUqjqU ']/li")

# Loop through each project and extract details
for project in projects:
    # Extract project title
    project_title = project.find_element(By.XPATH, ".//div[contains(@class, 'mr1 t-bold')]/span[@aria-hidden='true']").text
    print("Project Title:", project_title)
    
    # Extract associated dates (if available)
    try:
        dates = project.find_element(By.XPATH, ".//span[@class='t-14 t-normal']").text
        print("Dates:", dates)
    except:
        print("Dates: Not available")
    
    # Extract associated organization (if available)
    try:
        organization = project.find_element(By.XPATH, ".//span[contains(text(), 'Associated with')]/following-sibling::span").text
        print("Organization:", organization)
    except:
        print("Organization: Not available")
    
    # Extract description (if available)
    try:
        description = project.find_element(By.XPATH, ".//div[@class='t-14 t-normal t-black']/span[@aria-hidden='true']").text
        print("Description:", description)
    except:
        print("Description: Not available")
    
    # Extract related link (if available)
    try:
        link = project.find_element(By.XPATH, ".//a[@class='optional-action-target-wrapper']").get_attribute("href")
        print("Project Link:", link)
    except:
        print("Project Link: Not available")

    print("\n")
    
    
# Skill
driver.get(profile_url + '/details/skills/')
skills = driver.find_elements(By.XPATH, "//li[contains(@class, 'pvs-list__paged-list-item')]")

# Loop through each skill and extract details
for skill in skills:
    # Extract skill title
    skill_title = skill.find_element(By.XPATH, ".//div[contains(@class, 'hoverable-link-text')]/span[@aria-hidden='true']").text
    print("Skill Title:", skill_title)
    
    # Extract endorsements, if available
    try:
        endorsements = skill.find_element(By.XPATH, ".//span[contains(@aria-hidden, 'true') and contains(text(), 'endorsements')]").text
        print("Endorsements:", endorsements)
    except:
        print("Endorsements: Not available")
    
    # # Extract other information if available (like associated projects)
    # try:
    #     associated_project = skill.find_element(By.XPATH, ".//span[@aria-hidden='true' and contains(text(), 'Development')]").text
    #     print("Associated Project:", associated_project)
    # except:
    #     print("Associated Project: Not available")

    print("\n")
    
# Honor & Awards
driver.get(profile_url + '/details/honors/')
honors_xpath = "//ul[contains(@class, 'QFIEFfDZEAkjXzJYqEIBeKsbogPQVPlQgbg')]/li"

# Find all honors and awards elements
honors_elements = driver.find_elements(By.XPATH, honors_xpath)

# Iterate through each honor/award item and extract details
for honor in honors_elements:
    # Extract the title of the honor
    title = honor.find_element(By.XPATH, ".//div[contains(@class, 't-bold')]/span").text
    
    # Extract the issuer and date
    issuer_date = honor.find_element(By.XPATH, ".//span[contains(@class, 't-14 t-normal')]").text
    
    # Extract the associated institution if available
    try:
        associated_institution = honor.find_element(By.XPATH, ".//span[contains(text(), 'Associated with')]").text
    except:
        associated_institution = "Not available"
    
    # Extract image or media link if present
    try:
        media_url = honor.find_element(By.XPATH, ".//a[contains(@class, 'optional-action-target-wrapper')]").get_attribute("href")
    except:
        media_url = "No media"

    # Print the scraped data
    print(f"Title: {title}")
    print(f"Issuer and Date: {issuer_date}")
    print(f"Associated Institution: {associated_institution}")
    print(f"Media URL: {media_url}")
    print("="*50)
    

driver.quit()