# test_scrape.py

import unittest
from unittest.mock import patch, MagicMock
from mock_profile_data import (mock_intro_data, mock_about_data, mock_experience_data, 
                               mock_education_data, mock_certificates_data, mock_volunteering_data)
from scrape import scrape_profile

class TestScrapeProfile(unittest.TestCase):

    @patch('scrape.extract_intro')
    @patch('scrape.extract_about')
    @patch('scrape.extract_experience')
    @patch('scrape.extract_education')
    @patch('scrape.extract_certificate')
    @patch('scrape.extract_volunteering')
    @patch('selenium.webdriver.Chrome')
    def test_scrape_profile(self, mock_driver, mock_extract_intro, mock_extract_about, 
                            mock_extract_experience, mock_extract_education, 
                            mock_extract_certificate, mock_extract_volunteering):
        
        # Set the mock return values
        mock_extract_intro.return_value = mock_intro_data
        mock_extract_about.return_value = mock_about_data
        mock_extract_experience.return_value = mock_experience_data
        mock_extract_education.return_value = mock_education_data
        mock_extract_certificate.return_value = mock_certificates_data
        mock_extract_volunteering.return_value = mock_volunteering_data

        # Simulate a driver instance
        driver_instance = mock_driver.return_value

        # Call the function you want to test
        profile_data = scrape_profile(driver_instance, "https://mock_profile_url", visited_profiles=[])

        # Assert that the data matches the mock data
        self.assertEqual(profile_data['intro'], mock_intro_data)
        self.assertEqual(profile_data['about'], mock_about_data)
        self.assertEqual(profile_data['experience'], mock_experience_data)
        self.assertEqual(profile_data['education'], mock_education_data)
        self.assertEqual(profile_data['certificate'], mock_certificates_data)
        self.assertEqual(profile_data['volunteering'], mock_volunteering_data)

if __name__ == "__main__":
    unittest.main()
