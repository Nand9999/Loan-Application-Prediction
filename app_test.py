import unittest
from main import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    # Test if missing field in prediction form returns proper message
    def test_missing_field(self):
        tester = app.test_client(self)
        response = tester.post('/predict', data={
            'gender': 'Male',
            'married': 'Yes',
            'dependents': '',
            'education': 'Graduate',
            'self_employed': 'No',
            'applicant_income': '5000',
            'coapplicant_income': '0',
            'loan_amount': '200',
            'loan_amount_term': '360',
            'credit_history': '1',
            'property_area': 'Urban'
        }, follow_redirects=True)
        self.assertIn(b'Please fill all the fields.', response.data)

    def test_invalid_input_numerical(self):
        tester = app.test_client(self)
        response=tester.post('/predict',data = {
            'gender': 'Male',
            'married': 'Yes',
            'dependents': '1',
            'education': 'Graduate',
            'self_employed': 'No',
            'applicant_income': 'invalid',
            'coapplicant_income': 'invalid',
            'loan_amount': 'invalid',
            'loan_amount_term': 'invalid',
            'credit_history': 'invalid',
            'property_area': 'Urban'
        },follow_redirects=True)
        self.assertIn(b'Invalid input for numerical fields.', response.data)

    def test_invalid_input_dependents(self):
        tester = app.test_client(self)
        response = tester.post('/predict', data={
            'gender': 'Male',
            'married': 'Yes',
            'dependents': 'invalid',
            'education': 'Graduate',
            'self_employed': 'No',
            'applicant_income': '5000',
            'coapplicant_income': '0',
            'loan_amount': '200',
            'loan_amount_term': '360',
            'credit_history': '1',
            'property_area': 'Urban'
        }, follow_redirects=True)
        self.assertIn(b'Invalid input for Dependents.', response.data)


    # Test if prediction result is as expected for a sample input
    def test_prediction_result(self):
        tester = app.test_client(self)
        response = tester.post('/predict', data={
            'gender': 'Male',
            'married': 'Yes',
            'dependents': '1',
            'education': 'Graduate',
            'self_employed': 'No',
            'applicant_income': '5000',
            'coapplicant_income': '0',
            'loan_amount': '200',
            'loan_amount_term': '360',
            'credit_history': '1',
            'property_area': 'Urban'
        }, follow_redirects=True)
        self.assertIn(b'Approved', response.data)

   

if __name__ == '__main__':
    unittest.main()




