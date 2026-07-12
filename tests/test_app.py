import json
import os
import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)

    def test_prediction_endpoint(self):
        payload = {
            'applicant_name': 'Jane Doe',
            'Applicant_Income': 120000,
            'Coapplicant_Income': 40000,
            'Loan_Amount': 900000,
            'Credit_Score': 750,
            'DTI_Ratio': 0.35,
            'Savings': 200000,
            'Employment_Status': 'Employed',
            'Marital_Status': 'Single',
            'Loan_Purpose': 'Education',
            'Property_Area': 'Urban',
            'Gender': 'Female',
            'Education_Level': 'Graduate',
            'Employer_Category': 'Private',
            'Age': 29,
            'Dependents': 1,
            'Existing_Loans': 1,
        }
        response = self.client.post('/predict', json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertIn('result', body)
        self.assertIn('probability', body)


if __name__ == '__main__':
    unittest.main()
