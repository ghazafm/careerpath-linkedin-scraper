from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from helper import scroll_to_bottom
from helper import get_object
from helper import get_objects
from helper import extract_element_text
from helper import extract_many_element_text
from helper import extract_element_attribute

from selenium.webdriver.common.by import By
from helper import get_object, extract_element_text, extract_element_attribute, extract_many_element_text
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from helper import get_object, extract_element_text
from selenium.common.exceptions import NoSuchElementException

def extract_company_people_links(driver, company_url):
    # Go to the company URL
    driver.get(company_url)
    
    # Get all the profile cards with their links
    profile_links_xpath = "//ul[@class='display-flex list-style-none flex-wrap']/li//a[contains(@class, 'app-aware-link')]"
    profile_links = get_objects(driver, By.XPATH, profile_links_xpath)
    
    # Extract the href (profile link) from each card
    links = []
    for profile in profile_links:
        link = extract_element_attribute(profile, By.XPATH, '.', 'href')
        links.append(link)
    
    return links

def extract_intro(driver):
    try:
        intro_data = {}
        
        # XPath for the intro section
        intro_xpath = "//div[contains(@class, 'mt2 relative')]"
        intro = get_object(driver, By.XPATH, intro_xpath)
        if intro:
            # Extract name using XPath
            name_xpath = ".//h1[contains(@class, 'text-heading-xlarge')]"
            name = extract_element_text(intro, By.XPATH, name_xpath)
            intro_data['name'] = name
            
            # Extract pronouns (if available) using XPath
            pronouns_xpath = ".//span[contains(@class, 'text-body-small v-align-middle')]"
            try:
                pronouns = extract_element_text(intro, By.XPATH, pronouns_xpath)
                intro_data['pronouns'] = pronouns
            except:
                intro_data['pronouns'] = 'Not available'

            # Extract company/workplace (works_at) using XPath
            works_at_xpath = ".//div[contains(@class, 'text-body-medium break-words')]"
            works_at = extract_element_text(intro, By.XPATH, works_at_xpath)
            intro_data['works_at'] = works_at
            # Extract location using XPath
            location_xpath = ".//span[contains(@class, 'text-body-small inline t-black--light break-words')]"
            location = extract_element_text(intro, By.XPATH, location_xpath)
            intro_data['location'] = location

            # Extract followers count using XPath
            followers_xpath = "//p[contains(@class, 'pvs-header__optional-link')]//span[contains(text(), 'followers')]"
            try:
                followers = extract_element_text(driver, By.XPATH, followers_xpath).split()[0]
                intro_data['followers'] = followers
            except:
                print('ini salah')
                intro_data['followers'] = 'Hide'
                
            # Extract connections count using XPath
            connections_xpath = "//li[@class='text-body-small']//span[@class='t-black--light']//span[@class='t-bold']"
            try:
                connections = extract_element_text(driver, By.XPATH, connections_xpath)
                intro_data['connections'] = connections
            except:
                intro_data['connections'] = 'Not available'

        else:
            print("Intro section not found")
            intro_data = None

    except NoSuchElementException as e:
        print(f"Error extracting intro: Element not found - {e}")
        intro_data = None
    except Exception as e:
        print(f"Error extracting intro: {e}")
        intro_data = None

    print(intro_data)
    return intro_data



def extract_about(driver):
    try:
        xpath_about = "//section[contains(@class, 'artdeco-card pv-profile-card')]//h2[span[text()='About']]/ancestor::section//div[contains(@class, 'full-width')]//span[@aria-hidden='true']"
        
        about_description = extract_element_text(driver, By.XPATH, xpath_about)

        if about_description:
            return {'about_description': about_description}
        else:
            return {'about_description': None}

    except Exception as e:
        print(f"Error extracting 'About' section: {e}")
        return {'about_description': None}

        
    
def extract_experience(driver, profile_url):
    experiences = []
    driver.get(profile_url + '/details/experience/')
    scroll_to_bottom(driver)

    # Find the experience list container
    experience_list = get_objects(driver, By.CLASS_NAME, "pvs-list__paged-list-item")
    
    # Iterate over each experience item
    for experience in experience_list:
        try:
            # Extract job title
            job_title = extract_element_text(experience, By.XPATH, ".//div[contains(@class,'t-bold')]")

            # Extract company name
            company_name = extract_element_text(experience, By.XPATH,  ".//span[contains(@class, 'hoverable-link-text')]")

            # Extract duration
            duration = extract_element_text(experience, By.XPATH,  ".//span[contains(@class, 't-black--light')][1]")

            # Extract location
            location = extract_element_text(experience, By.XPATH, ".//span[contains(@class, 't-black--light')][2]")

            # Create a dictionary to store this experience's details
            experience_data = {
                'job_title': job_title,
                'company_name': company_name,
                'duration': duration,
                'location': location
            }

            # Append this experience to the list
            experiences.append(experience_data)
            
        except Exception as e:
            print(f"Error extracting data for one experience: {e}")

    return experiences  # Return the full list of experiences

            
def extract_education(driver, profile_url):
    educations = []
    driver.get(profile_url)
    scroll_to_bottom(driver)
    
    # Locate all education entries (multiple li elements within the ul)
    education_entries = get_objects(driver, By.XPATH, "//section[contains(@class, 'artdeco-card') and contains(., 'Education')]//ul/li[contains(@class, 'artdeco-list__item')]")
    
    # Loop through each education entry
    for entry in education_entries:
        try:
            # Extract organization name
            university_name = extract_element_text(entry, By.XPATH, ".//a[contains(@href, 'company')]//div[contains(@class,'hoverable-link-text')]")
            
            # Extract degree and field of study
            degree_field = extract_element_text(entry, By.XPATH, ".//span[contains(@class, 't-14 t-normal')]")
            
            # Extract graduation year or duration
            graduation_year = extract_element_text(entry, By.XPATH, ".//span[@class='pvs-entity__caption-wrapper']")
            
            # Extract additional information (if available, such as skills)
            skills = extract_element_text(entry, By.XPATH, ".//strong")
            
            education_data = {
                'university_name': university_name,
                'degree_field': degree_field,
                'graduation_year': graduation_year,
                'skills': skills
            }
            educations.append(education_data)

        except Exception as e:
            print(f"Error extracting data from one education entry: {e}")
    
    return educations

def extract_certificate(driver, profile_url):
    certificates = []
    driver.get(profile_url + '/details/certifications/')
    scroll_to_bottom(driver)
    
    # Locate certification items
    certifications = get_objects(driver, By.XPATH, "//ul[contains(@class, 'GwDizhdSHYPkIbgBuMBRdRJgYmpMKyoUqjqU')]/li")

    # Loop through each certification and extract details
    for cert in certifications:
        cert_data = {}
        
        # Extract certification name
        cert_name = extract_element_text(cert, By.XPATH, ".//span[@aria-hidden='true']")
        cert_data['certification_name'] = cert_name

        # Extract issuer (if available)
        try:
            issuer = extract_element_text(cert, By.XPATH, ".//span[@aria-hidden='true'][2]")
            cert_data['issuer'] = issuer
        except:
            cert_data['issuer'] = "Not available"
        
        # Extract the date issued (if available)
        try:
            date_issued = extract_element_text(cert, By.XPATH, ".//span[contains(@class, 'pvs-entity__caption-wrapper')]")
            cert_data['date_issued'] = date_issued
        except:
            cert_data['date_issued'] = "Not available"
        
        # Extract credential link (if available)
        try:
            credential_link = extract_element_attribute(cert, By.XPATH, ".//a[contains(@aria-label, 'Show credential')]", "href")
            cert_data['credential_link'] = credential_link
        except:
            cert_data['credential_link'] = "Not available"

        # Append this certificate's data to the list
        certificates.append(cert_data)

    # Return the list of all certificates
    return certificates



def extract_volunteering(driver, profile_url):
    volunteers = []
    driver.get(profile_url)
    scroll_to_bottom(driver)
    # Locate all volunteering entries (multiple li elements within the ul)
    volunteering_entries = get_objects(driver, By.XPATH, "//section[contains(@class, 'artdeco-card') and contains(., 'Volunteer experience')]//ul/li[contains(@class, 'artdeco-list__item')]")
    
    # Loop through each volunteering entry
    for entry in volunteering_entries:
        try:
            # Extract the role or title
            role = extract_element_text(entry, By.XPATH, ".//div[contains(@class,'t-bold')]")
            
            # Extract the organization name
            organization = extract_element_text(entry, By.XPATH, ".//span[contains(@class, 't-14 t-normal')]")
            
            # Extract the duration
            duration = extract_element_text(entry, By.XPATH, ".//span[@class='pvs-entity__caption-wrapper']")
            
            # Extract the cause (if available)
            cause = extract_element_text(entry, By.XPATH, ".//span[@class='t-14 t-normal t-black--light']")
            
            # Extract the description (if available)
            description = extract_element_text(entry, By.XPATH, ".//div[contains(@class, 'inline-show-more-text')]")
            
            volunteer_data = {
                'role': role,
                'organization': organization,
                'duration': duration,
                'cause': cause,
                'description': description,
            }
            
            volunteers.append(volunteer_data)
        except Exception as e:
            print(f"Error extracting data from one volunteering entry: {e}")
        
    return volunteers



def extract_project(driver, profile_url):
    projects = []
    driver.get(profile_url + '/details/projects/')
    scroll_to_bottom(driver)
    
    projects_element = get_objects(driver, By.XPATH, "//ul[@class='GwDizhdSHYPkIbgBuMBRdRJgYmpMKyoUqjqU ']/li")

    # Loop through each project and extract details
    for project in projects_element:
        project_data = {}
        
        # Extract project title
        project_title = get_object(project, By.XPATH, ".//div[contains(@class, 'mr1 t-bold')]/span[@aria-hidden='true']")
        print("Project Title:", project_title)
        
        # Extract associated dates (if available)
        try:
            dates = extract_element_text(project, By.XPATH, ".//span[@class='t-14 t-normal']")
            project_data['dates'] = dates
        except:
            project_data['dates'] = "Not Available"
        
        # Extract associated organization (if available)
        try:
            organization = extract_element_text(project, By.XPATH, ".//span[contains(text(), 'Associated with')]/following-sibling::span")
            project_data['organization'] = organization
        except:
            project_data['organization'] = "Not Available"
        
        # Extract description (if available)
        try:
            description = extract_element_text(project, By.XPATH, ".//div[@class='t-14 t-normal t-black']/span[@aria-hidden='true']")
            project_data['description'] = description
        except:
            project_data['description'] = "Not Available"
        
        # Extract related link (if available)
        try:
            link = extract_element_attribute(project, By.XPATH, ".//a[@class='optional-action-target-wrapper']", "href")
            project_data['link'] = link
        except:
            project_data['link'] = "Not Available"
        
        projects.append(project_data)
        
    return projects



def extract_skill(driver, profile_url):
    skills = []
    driver.get(profile_url + '/details/skills/')
    scroll_to_bottom(driver)
    skills_element = get_objects(driver, By.XPATH, "//li[contains(@class, 'pvs-list__paged-list-item')]")

    # Loop through each skill and extract details
    for skill in skills_element:
        skill_data = {}
        # Extract skill title
        skill_title = extract_element_text(skill, By.XPATH, ".//div[contains(@class, 'hoverable-link-text')]/span[@aria-hidden='true']")
        skill_data['tittle'] = skill_title
        
        # Extract endorsements, if available
        try:
            endorsements = extract_element_text(skill, By.XPATH, ".//span[contains(@aria-hidden, 'true') and contains(text(), 'endorsements')]")
            skill_data['endorsements'] = endorsements
        except:
            skill_data['endorsements'] = "Not available"
        
        skills.append(skill_data)
        
    return skills



def extract_honor(driver, profile_url):
    honors = []
    driver.get(profile_url + '/details/honors/')
    scroll_to_bottom(driver)
    honors_xpath = "//ul[contains(@class, 'QFIEFfDZEAkjXzJYqEIBeKsbogPQVPlQgbg')]/li"

    # Find all honors and awards elements
    honors_elements = get_objects(driver, By.XPATH, honors_xpath)

    # Iterate through each honor/award item and extract details
    for honor in honors_elements:
        # Extract the title of the honor
        title = extract_element_text(By.XPATH, ".//div[contains(@class, 't-bold')]/span")
        
        # Extract the issuer and date
        issuer_date = extract_element_text(honor, By.XPATH, ".//span[contains(@class, 't-14 t-normal')]")
        
        # Extract the associated institution if available
        try:
            associated_institution = extract_element_text(honor, By.XPATH, ".//span[contains(text(), 'Associated with')]")
        except:
            associated_institution = "Not available"
        
        # Extract image or media link if present
        try:
            media_url = extract_element_attribute(honor, By.XPATH, ".//a[contains(@class, 'optional-action-target-wrapper')]", "href")
        except:
            media_url = "No media"

        education_data = {
                'title': title,
                'issuer_date': issuer_date,
                'associated_institution': associated_institution,
                'media_url': media_url
            }
        honors.append(education_data)
    return honors



def extract_organizations(driver, profile_url):
    organizations = []
    driver.get(profile_url)
    # Locate all organization entries (multiple li elements within the ul)
    organization_entries = get_objects(driver, By.XPATH, "//section[contains(@class, 'artdeco-card') and contains(., 'Organizations')]//ul/li[contains(@class, 'artdeco-list__item')]")
    
    # Loop through each organization entry
    for entry in organization_entries:
        try:
            # Extract the organization name
            organization_name = extract_element_text(entry, By.XPATH, ".//div[contains(@class,'t-bold')]")
            
            # Extract the role or title
            role = extract_element_text(entry, By.XPATH, ".//span[contains(@class, 't-14 t-normal')]")
            
            # Extract the duration
            duration = extract_element_text(entry, By.XPATH, ".//span[@class='pvs-entity__caption-wrapper']")
            
            # Extract description or other additional information (if available)
            description = extract_element_text(entry, By.XPATH, ".//div[contains(@class, 't-14 t-normal t-black')]")
            
            organization_data = {
                'organization_name': organization_name,
                'role': role,
                'duration': duration,
                'description': description
            }
            organizations.append(organization_data)
        except Exception as e:
            print(f"Error extracting data from one organization entry: {e}")
        
    return organizations


def scrape_profile(driver, profile_url, visited_profiles):
    if profile_url in visited_profiles:
        print(f"Already visited: {profile_url}")
        return
    
    driver.get(profile_url)
    scroll_to_bottom(driver)

    profile_data = {}

    profile_data['intro'] = extract_intro(driver)
    # profile_data['about'] = extract_about(driver)
    # profile_data['experience'] = extract_experience(driver, profile_url)
    # profile_data['education'] = extract_education(driver, profile_url)
    # profile_data['certificate'] = extract_certificate(driver, profile_url)
    # profile_data['volunteering'] = extract_volunteering(driver, profile_url)
    # profile_data['projects'] = extract_project(driver, profile_url)
    # profile_data['skills'] = extract_skill(driver, profile_url)
    # profile_data['honor'] = extract_honor(driver, profile_url)
    # profile_data['organizations'] = extract_organizations(driver, profile_url)

    return profile_data


def extract_more_profiles(driver):
    """Extract 'More profiles for you' section URLs."""
    try:
        # Locate the section with profiles similar to the current one
        profile_urls = get_object(driver, By.XPATH, "//a[@data-field='browsemap_card_click']")
        
        # If URLs are found, extract them
        if profile_urls:
            urls = profile_urls.get_attribute("href")
            return urls
        else:
            raise NoSuchElementException("No 'More profiles for you' section found.")
            
    except NoSuchElementException as e:
        print(f"Error: {e}. No profiles were found.")
        return []
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

