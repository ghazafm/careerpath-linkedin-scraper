from urllib.parse import urlparse, urlunparse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from helper import scroll_and_load
from helper import get_object
from helper import get_objects
from helper import extract_element_text
from helper import extract_many_element_text
from helper import extract_element_attribute
from helper import save_to_json

from selenium.webdriver.common.by import By
from helper import (
    get_object,
    extract_element_text,
    extract_element_attribute,
    extract_many_element_text,
)
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
        link = extract_element_attribute(profile, By.XPATH, ".", "href")
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
            intro_data["name"] = name

            # Extract pronouns (if available) using XPath
            pronouns_xpath = (
                ".//span[contains(@class, 'text-body-small v-align-middle')]"
            )
            try:
                pronouns = extract_element_text(intro, By.XPATH, pronouns_xpath)
                intro_data["pronouns"] = pronouns
            except:
                intro_data["pronouns"] = None

            # Extract company/workplace (works_at) using XPath
            works_at_xpath = ".//div[contains(@class, 'text-body-medium break-words')]"
            works_at = extract_element_text(intro, By.XPATH, works_at_xpath)
            intro_data["works_at"] = works_at
            # Extract location using XPath
            location_xpath = ".//span[contains(@class, 'text-body-small inline t-black--light break-words')]"
            location = extract_element_text(intro, By.XPATH, location_xpath)
            intro_data["location"] = location

            # Extract followers count using XPath
            followers_xpath = "//p[contains(@class, 'pvs-header__optional-link')]//span[contains(text(), 'followers')]"
            try:
                followers = extract_element_text(
                    driver, By.XPATH, followers_xpath
                ).split()[0]
                intro_data["followers"] = followers
            except:
                intro_data["followers"] = None

            # Extract connections count using XPath
            connections_xpath = "//li[@class='text-body-small']//span[@class='t-black--light']//span[@class='t-bold']"
            try:
                connections = extract_element_text(driver, By.XPATH, connections_xpath)
                intro_data["connections"] = connections
            except:
                intro_data["connections"] = None

        else:
            print("Intro section not found")
            intro_data = None

    except NoSuchElementException as e:
        print(f"Error extracting intro: Element not found - Not Available")
        intro_data = None
    except Exception as e:
        print(f"Error extracting intro: Not Available")
        intro_data = None

    return intro_data


def extract_about(driver):
    try:
        xpath_about = "//section[contains(@class, 'artdeco-card pv-profile-card')]//h2[span[text()='About']]/ancestor::section//div[contains(@class, 'full-width')]//span[@aria-hidden='true']"

        about_description = extract_element_text(
            driver, By.XPATH, xpath_about, timeout=2
        )

        if about_description:
            return {"about_description": about_description}
        else:
            return {"about_description": ""}

    except Exception as e:
        print(f"'About' section doesn't exist")
        return {"about_description": ""}



def extract_experience(driver):
    experience_data = []
    try:
        # Define the list to store all experience data
        scroll_and_load(driver)
        # Define XPath for extracting job experience information
        experience_elements = get_objects(
            driver,
            By.XPATH,
            "//div[@id='experience']/ancestor::section//ul/li[contains(@class, 'artdeco-list__item')]",
            timeout=5
        )

        # Loop through the experiences and extract information
        for experience in experience_elements:
            # Initialize a dictionary to store the data for each experience
            experience_dict = {}

            try:
                # Check if the experience has multiple roles (nested list)
                try:            
                    nested_experiences = get_objects(
                        experience,
                        By.XPATH,
                        ".//div[contains(@class, 'pvs-entity__sub-components')]/ul/li/div[contains(@data-view-name, 'profile-component-entity')]",
                    )
                except Exception as e:
                    nested_experiences = None
                    
                if nested_experiences:
                    try:
                        company_name = extract_element_text(
                            experience,
                            By.XPATH,
                            ".//div[contains(@class, 'flex-wrap')]",
                        ).split("\n")[0]
                    except Exception as e:
                        print(f"Error extracting company name: Not available")
                        company_name = None

                    # try:
                    #     total_time = extract_element_text(
                    #         experience,
                    #         By.XPATH,
                    #         ".//span[@class='t-14 t-normal']"
                    #     ).split("\n")[0]
                    #     experience_dict['total_time'] = total_time
                    # except Exception as e:
                    #     print(f"Error extracting total time: Not available")
                    #     experience_dict['total_time'] = None

                    try:
                        location = extract_element_text(
                            experience,
                            By.XPATH,
                            ".//a[@data-field='experience_company_logo']//span[contains(@class, 't-black--light')]"
                        ).split("\n")[0]
                    except Exception as e:
                        print(f"Error extracting location: Not available")
                        location = None

                    for nested_exp in nested_experiences:
                        # Try to extract the job title
                        try:
                            job_title = extract_element_text(
                                nested_exp,
                                By.XPATH,
                                ".//div[@class='display-flex flex-wrap align-items-center full-height']"
                            ).split('\n')[0]
                        except Exception as e:
                            print(f"Error extracting job title: Not available")
                            job_title = None

                        # Try to extract the type
                        try:
                            type = extract_element_text(
                                nested_exp,
                                By.XPATH,
                                ".//span[@class='t-14 t-normal']"
                            ).split()[0]
                        except Exception as e:
                            print(f"Error extracting type: Not available")
                            type = None

                        # Try to extract the dates
                        try:
                            dates = extract_element_text(
                                nested_exp, 
                                By.XPATH,
                                './/span[contains(@class, "t-black--light")]/span'
                            )
                        except Exception as e:
                            print(f"Error extracting dates: Not available")
                            dates = None
                            
                        try:
                            description = extract_element_text(
                                nested_exp, 
                                By.XPATH,
                                ".//li[contains(@class, 'pvs-list__item--with-top-padding')]//div[contains(@class, 'inline-show-more-text--is-collapsed')]",
                            )
                        except Exception as e:
                            print(f"Error extracting description: Not available")
                            description = None

                        experience_dict = {
                            'company_name': company_name,
                            'job_title': job_title,
                            'location': location,
                            'type': type,
                            'dates': dates,
                            'description': description
                            }
                        experience_data.append(experience_dict)
                else:
                    # Try to extract the job title
                    try:
                        company_type = extract_element_text(
                                experience, 
                                By.XPATH, 
                                ".//span[@class='t-14 t-normal']"
                        )
                        company_type = company_type.split('\n')[0]
                        company_type = company_type.split('·')
                        company_name = company_type[0]
                        type = company_type[1]
                    except Exception as e:
                        print(f"Error extracting job title: Not available")
                        company_name = None
                        type = None
                        
                    try:
                        job_title = extract_element_text(
                            experience,
                            By.XPATH,
                            ".//div[contains(@class, 'flex-wrap')]",
                        )
                    except Exception as e:
                        print(f"Error extracting company name: Not available")
                        job_title = None

                    # Try to extract the dates
                    try:
                        dates = extract_element_text(
                            experience, 
                            By.XPATH, 
                            './/span[contains(@class, "t-black--light")]/span'
                        )
                    except Exception as e:
                        print(f"Error extracting dates: Not available")
                        dates = None

                    # Try to extract the location
                    try:
                        location = extract_element_text(
                            experience, 
                            By.XPATH,
                            ".//span[contains(@class, 't-black--light')]//span[not(contains(@class, 'pvs-entity__caption-wrapper')) and @aria-hidden='true']",
                        )
                    except Exception as e:
                        print(f"Error extracting location: Not available")
                        location = None
                        
                    try:
                        description = extract_element_text(
                            experience, 
                            By.XPATH,
                            ".//li[contains(@class, 'pvs-list__item--with-top-padding')]//div[contains(@class, 'inline-show-more-text--is-collapsed')]",
                        )
                    except Exception as e:
                        print(f"Error extracting description: Not available")
                        description = None
                        
                    experience_dict = {
                            'company_name': company_name,
                            'job_title': job_title,
                            'location': location,
                            'type': type,
                            'dates': dates,
                            'description': description
                            }
                    experience_data.append(experience_dict)
            except Exception as e:
                print(f"Error extracting experience information: {e}")
    except Exception as e:
        print(f"Error extracting experience information: Not Available")
        
        
    return experience_data



def extract_education(driver):
    educations = []
    try:

        # Locate all education entries
        education_entries = get_objects(
            driver,
            By.XPATH,
            "//div[@id='education']/ancestor::section//ul/li[contains(@class, 'artdeco-list__item')]",
        )

        # Loop through each education entry
        for entry in education_entries:
            try:
                education_data = {}

                # Extract organization name
                try:
                    instance_name = extract_element_text(
                        entry,
                        By.XPATH,
                        ".//a[contains(@target, '_self')]//span[contains(@aria-hidden, 'true')]",
                    )
                    education_data["instance_name"] = instance_name
                except Exception as e:
                    print(f"Error extracting instance name: Not Available")
                    education_data["instance_name"] = None

                # Extract degree and field of study
                try:
                    degree_field = extract_element_text(
                        entry,
                        By.XPATH,
                        ".//span[contains(@class, 't-14 t-normal') and not(contains(@aria-hidden, 'true'))]",
                    )
                    degree_field = degree_field.split("\n")[0].strip()
                    education_data["degree_field"] = degree_field
                except Exception as e:
                    print(f"Error extracting degree and field of study: Not Available")
                    education_data["degree_field"] = None

                # Extract graduation year
                try:
                    graduation_year = extract_element_text(
                        entry, By.XPATH, ".//span[@class='pvs-entity__caption-wrapper']"
                    )
                    education_data["graduation_year"] = graduation_year
                except Exception as e:
                    print(f"Error extracting graduation year: Not Available")
                    education_data["graduation_year"] = None

                # # Extract skills
                # try:
                #     skills = extract_element_text(
                #         entry,
                #         By.XPATH,
                #         ".//strong[contains(text(), 'skill')]"
                #     )
                #     if not skills:
                #         skills = None
                #     education_data["skills"] = skills or ""
                # except Exception as e:
                #     print(f"Error extracting skills: not available")
                #     education_data["skills"] = None

                educations.append(education_data)

            except Exception as e:
                print(f"Error extracting one education entry: Not Available")
    except Exception as e:
        print(f"Error extracting education information: Not Available")
    return educations


def extract_certificates(driver):
    certificates = []

    try:
        # Locate all certificate entries
        certificate_entries = get_objects(
            driver,
            By.XPATH,
            "//div[@id='licenses_and_certifications']/ancestor::section//ul/li[contains(@class, 'artdeco-list__item')]",
        )

        # Loop through each certificate entry
        for entry in certificate_entries:
            try:
                certificate_data = {}

                # Extract certificate name
                try:
                    cert_name = extract_element_text(
                        entry,
                        By.XPATH,
                        ".//div[contains(@class, 'display-flex')]//span[contains(@aria-hidden, 'true')]",
                    )
                    certificate_data["cert_name"] = cert_name.strip()
                except Exception as e:
                    print(f"Error extracting certificate name: Not Available")
                    certificate_data["cert_name"] = None

                # Extract issuing organization
                try:
                    issuer = extract_element_text(
                        entry,
                        By.XPATH,
                        ".//span[@class='t-14 t-normal']//span[contains(@aria-hidden, 'true')]",
                    )
                    certificate_data["issuer"] = issuer.strip()
                except Exception as e:
                    print(f"Error extracting issuing organization: Not Available")
                    certificate_data["issuer"] = None

                # Extract issue date
                try:
                    issue_date = extract_element_text(
                        entry,
                        By.XPATH,
                        ".//span[@class='pvs-entity__caption-wrapper' and contains(@aria-hidden, 'true')]",
                    )
                    certificate_data["issue_date"] = issue_date.strip()
                except Exception as e:
                    print(f"Error extracting issue date: Not Available")
                    certificate_data["issue_date"] = None

                # Extract credential URL (if available)
                try:
                    credential_url = extract_element_attribute(
                        entry,
                        By.XPATH,
                        "//div[contains(@class, 'display-flex flex-column')]//div[contains(@class, 'pvs-entity__sub-components')]//a[contains(@class, 'artdeco-button')]",
                        "href",
                    )
                    certificate_data["credential_url"] = credential_url
                except Exception as e:
                    print(f"Error extracting credential URL: Not Available")
                    certificate_data["credential_url"] = None

                certificates.append(certificate_data)

            except Exception as e:
                print(f"Error extracting one certificate entry: Not Available")
    except Exception as e:
        print(f"Error: certificates not available")
    return certificates


def extract_project(driver):
    projects = []

    try:
        projects_element = get_objects(
            driver,
            By.XPATH,
            "//div[@id='projects']/ancestor::section//ul/li[contains(@class, 'artdeco-list__item')]",
        )

        # Loop through each project and extract details
        for project in projects_element:
            project_data = {}

            # Extract project title
            try:
                project_title = extract_element_text(
                    project,
                    By.XPATH,
                    ".//div[contains(@class, 'mr1 t-bold')]/span[@aria-hidden='true']",
                )
                project_data["project_title"] = project_title
            except:
                project_data["dates"] = None

            # Extract associated dates (if available)
            try:
                dates = extract_element_text(
                    project, By.XPATH, ".//span[@class='t-14 t-normal']"
                ).split("\n")[0]
                project_data["dates"] = dates
            except:
                project_data["dates"] = None

            # Extract associated organization (if available)
            try:
                organization = extract_element_text(
                    project,
                    By.XPATH,
                    ".//span[contains(text(), 'Associated with')]/following-sibling::span",
                )
                project_data["organization"] = organization
            except:
                project_data["organization"] = None

            # Extract description (if available)
            try:
                description = extract_element_text(
                    project,
                    By.XPATH,
                    ".//li[contains(@class, 'pvs-list__item--with-top-padding')]//div[contains(@class, 'full-width t-14')]//div[contains(@class, 'full-width')]//span[@aria-hidden='true']",
                )
                project_data["description"] = description
            except:
                project_data["description"] = None

            # Extract related link (if available)
            try:
                link = extract_element_attribute(
                    project,
                    By.XPATH,
                    ".//a[@class='optional-action-target-wrapper']",
                    "href",
                )
                project_data["link"] = link
            except:
                project_data["link"] = None

            projects.append(project_data)
    except:
        print(f"Error: projects not available")
    return projects


def extract_volunteering(driver):
    volunteers = []

    try:
        # Locate all volunteering entries (multiple li elements within the ul)
        volunteering_entries = get_objects(
            driver,
            By.XPATH,
            "//div[@id='volunteering_experience']/ancestor::section//ul/li[contains(@class, 'artdeco-list__item')]",
        )

        # Loop through each volunteering entry
        for entry in volunteering_entries:
            volunteer_data = {}

            # Try to extract the role or title
            try:
                role = extract_element_text(
                    entry, By.XPATH, ".//div[contains(@class,'t-bold')]"
                )
                volunteer_data["role"] = role
            except Exception as e:
                print(f"Error extracting role: Not Available")
                volunteer_data["role"] = None

            # Try to extract the organization name
            try:
                organization = extract_element_text(
                    entry, By.XPATH, ".//span[contains(@class, 't-14 t-normal')]"
                ).split("\n")[0]
                volunteer_data["organization"] = organization
            except Exception as e:
                print(f"Error extracting organization: Not Available")
                volunteer_data["organization"] = None

            # Try to extract the duration
            try:
                duration = extract_element_text(
                    entry, By.XPATH, ".//span[@class='pvs-entity__caption-wrapper']"
                )
                volunteer_data["duration"] = duration
            except Exception as e:
                print(f"Error extracting duration: Not Available")
                volunteer_data["duration"] = None

            # Try to extract the cause (if available)
            try:
                cause = extract_many_element_text(
                    entry, By.XPATH, ".//span[contains(@class, 't-black--light')]"
                )
                volunteer_data["cause"] = cause[1].split("\n")[0]
            except Exception as e:
                print(f"Error extracting cause: Not available")
                volunteer_data["cause"] = None

            # Try to extract the description (if available)
            try:
                description = extract_element_text(
                    entry, By.XPATH, ".//div[contains(@class, 'inline-show-more-text')]"
                )
                volunteer_data["description"] = description
            except Exception as e:
                print(f"Error extracting volunteer description: Not Available")
                volunteer_data["description"] = None

            # Add the collected data for the current entry
            volunteers.append(volunteer_data)
    except Exception as e:
        print(f"Error: volunteering not available")

    return volunteers


def extract_skill(driver):
    skills = []
    try: 
        skills_element = get_objects(
            driver,
            By.XPATH,
            "//div[@id='skills']/ancestor::section//ul/li[contains(@class, 'artdeco-list__item')]",
        )

        # Loop through each skill and extract details
        for skill in skills_element:
            skill_data = {}
            # Extract skill title
            skill_title = extract_element_text(
                skill,
                By.XPATH,
                ".//div[contains(@class, 'hoverable-link-text')]/span[@aria-hidden='true']",
            )
            skill_data["tittle"] = skill_title

            # Extract endorsements_by, if available
            try:
                endorsements_by = extract_many_element_text(
                    skill,
                    By.XPATH,
                    ".//div[contains(@class, 'mv1')]//div[@class='display-flex ']//div[contains(@class, 'inline-show-more-text--is-collapsed')]",
                )
                skill_data["endorsements_by"] = endorsements_by
            except:
                skill_data["endorsements_by"] = None

            # Extract endorsements, if available
            try:
                endorsements = extract_element_text(
                    skill,
                    By.XPATH,
                    ".//span[contains(@aria-hidden, 'true') and contains(text(), 'endorsements')]",
                )
                skill_data["endorsements"] = endorsements.split()[0]
            except:
                skill_data["endorsements"] = None

            skills.append(skill_data)
            
    except Exception as e:
        print(f"Error extracting skills information: Not Available")
    return skills


def extract_honor(driver):
    honors = []
    try:
        honors_xpath = "//div[@id='honors_and_awards']/ancestor::section//ul/li[contains(@class, 'artdeco-list__item')]"

        # Find all honors and awards elements
        honors_elements = get_objects(driver, By.XPATH, honors_xpath)

        # Iterate through each honor/award item and extract details
        for honor in honors_elements:
            # Extract the title of the honor
            title = extract_element_text(
                honor, By.XPATH, ".//div[contains(@class, 't-bold')]/span"
            )

            # Extract the issuer and date
            issuer_date = (
                extract_element_text(
                    honor, By.XPATH, ".//span[contains(@class, 't-14 t-normal')]"
                )
                .split("\n")[0]
                .split("·")
            )

            # Extract image or media link if present
            try:
                media_url = extract_element_attribute(
                    honor,
                    By.XPATH,
                    ".//a[contains(@class, 'optional-action-target-wrapper')]",
                    "href",
                )
            except:
                media_url = None

            education_data = {
                "title": title,
                "issuing_institution": issuer_date[0].strip(),
                "issued_date": issuer_date[1].strip(),
                "media_url": media_url,
            }
            honors.append(education_data)
            
    except Exception as e:
        print(f"Error extracting honors information: Not Available")
    return honors


def extract_organizations(driver):
    organizations = []
    try:
        organization_entries = get_objects(
            driver,
            By.XPATH,
            "//div[@id='organizations']/ancestor::section//ul/li[contains(@class, 'artdeco-list__item')]",
        )

        # Loop through each organization entry
        for entry in organization_entries:
            organization_data = {}

            # Try to extract the organization name
            try:
                organization_name = extract_element_text(
                    entry, By.XPATH, ".//div[contains(@class,'t-bold')]"
                )
                organization_data["organization_name"] = organization_name
            except Exception as e:
                print(f"Error extracting organization name: Not Available")
                organization_data["organization_name"] = None

            # Try to extract the role or title and duration
            try:
                role_duration = extract_element_text(
                    entry, By.XPATH, ".//span[contains(@class, 't-14 t-normal')]"
                ).split("·")

                # Separate role and duration
                role = role_duration[0].strip() if len(role_duration) > 0 else None
                duration = role_duration[1].strip() if len(role_duration) > 1 else None
                organization_data["role"] = role
                organization_data["duration"] = duration
            except Exception as e:
                print(f"Error extracting role or duration: Not Available")
                organization_data["role"] = None
                organization_data["duration"] = None

            # Try to extract the description or other additional information
            try:
                description = extract_element_text(
                    entry,
                    By.XPATH,
                    ".//li[contains(@class, 'pvs-list__item--with-top-padding')]//div[contains(@class, 't-14 t-normal t-black')]",
                )
                organization_data["description"] = description
            except Exception as e:
                print(f"Error extracting description: Not Available")
                organization_data["description"] = None

            # Append the collected data to the organizations list
            organizations.append(organization_data)
            
    except Exception as e:
        print(f"Error extracting organizations information: Not Available")
    return organizations


def scrape_profile(driver, profile_url, visited_profiles):
    if profile_url in visited_profiles:
        print(f"Already visited: {profile_url}")
        return

    driver.get(profile_url)
    scroll_and_load(driver)

    profile_data = {}
    profile_data["intro"] = extract_intro(driver)
    profile_data["about"] = extract_about(driver)
    profile_data['experience'] = extract_experience(driver)
    profile_data['education'] = extract_education(driver)
    profile_data['certificate'] = extract_certificates(driver)
    profile_data['projects'] = extract_project(driver)
    profile_data["volunteering"] = extract_volunteering(driver)
    profile_data['skills'] = extract_skill(driver)
    profile_data['honor'] = extract_honor(driver)
    profile_data['organizations'] = extract_organizations(driver)

    return profile_data


def extract_more_profiles(driver):
    """Extract 'More profiles for you' section URLs."""
    try:
        # Locate the section with profiles similar to the current one
        profile_urls = get_object(
            driver, By.XPATH, "//a[@data-field='browsemap_card_click']"
        )

        # If URLs are found, extract them
        if profile_urls:
            url = profile_urls.get_attribute("href")
            parsed_url = urlparse(url)
            url = urlunparse(parsed_url._replace(query=""))  # Remove the query part
            return url
        else:
            raise NoSuchElementException("No 'More profiles for you' section found.")

    except NoSuchElementException as e:
        print(f"Error: Not Available. No profiles were found.")
        return []

    except Exception as e:
        print(f"An unexpected error occurred: Not Available")
        return []
