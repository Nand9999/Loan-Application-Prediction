from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import unittest

class TestFrontend(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Chrome(executable_path='C:\Program Files\Google\Chrome\Application/chrome.exe')  # Provide path to your chromedriver
        chrome_options = Options()  # Create an instance of Options
        self.driver = webdriver.Chrome(options=chrome_options)  
        self.driver.get('http://localhost:5000')  # Assuming your Flask app is running locally

    def tearDown(self):
        self.driver.quit()

    def test_empty_form_submission(self):
        # Wait for the predict button to be clickable
        predict_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'predict-button'))
        )
        # Click the predict button
        predict_button.click()
        # Wait for the result element to appear
        result_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
        )
        self.assertIn('Loan Prediction Result', result_element.text)

    
    def test_invalid_input_numerical(self):
        # Wait for the input fields to be interactable
        applicant_income = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'applicant_income'))
        )
        coapplicant_income = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'coapplicant_income'))
        )
        loan_amount = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'loan_amount'))
        )
        loan_amount_term = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'loan_amount_term'))
        )
        credit_history = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'credit_history'))
        )

        # Fill form with invalid input for numerical fields
        applicant_income.send_keys('invalid')
        coapplicant_income.send_keys('invalid')
        loan_amount.send_keys('invalid')
        loan_amount_term.send_keys('invalid')
        credit_history.send_keys('invalid')

        # Click the predict button
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'predict-button'))
        )
        submit_button.click()

        # Wait for the result element to appear
        result_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
        )

        # Assert the result
        self.assertIn('Loan Prediction Result', result_element.text)

    def test_invalid_input_dependents(self):
        # Wait for the dependents input field to be interactable
        dependents_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'dependents'))
        )

        # Fill form with invalid input for dependents
        dependents_input.send_keys('invalid')

        # Click the predict button
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'predict-button'))
        )
        submit_button.click()

        # Wait for the result element to appear
        result_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
        )

        # Assert the result
        self.assertIn('Loan Prediction Result', result_element.text)

    def test_valid_input(self):
        # Wait for the input fields to be interactable
        applicant_income = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'applicant_income'))
        )
        coapplicant_income = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'coapplicant_income'))
        )
        loan_amount = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'loan_amount'))
        )
        loan_amount_term = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'loan_amount_term'))
        )
        credit_history = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'credit_history'))
        )

        # Fill form with valid input
        applicant_income.send_keys('5000')
        coapplicant_income.send_keys('2000')
        loan_amount.send_keys('120')
        loan_amount_term.send_keys('360')
        credit_history.send_keys('1')

        # Click the predict button
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'predict-button'))
        )
        submit_button.click()

        # Wait for the result element to appear
        result_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
        )

        # Assert the result
        self.assertIn('Loan Prediction Result', result_element.text)

if __name__ == '__main__':
    unittest.main()




