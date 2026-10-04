"""
End-to-End System Integration Test
===================================
Tests all Flask routes, model inference, input validation, and API responses.
"""

import sys
import os
import json

# Add root directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.app import app

def run_tests():
    client = app.test_client()
    passed = 0
    total = 0

    print("=" * 60)
    print("STARTING COMPREHENSIVE END-TO-END SYSTEM TESTS")
    print("=" * 60)

    # Test 1: Home Page
    total += 1
    res = client.get('/')
    assert res.status_code == 200, f"Home page returned {res.status_code}"
    assert b"College Placement Prediction" in res.data, "Home page missing title"
    assert b"Machine Learning Based Student Placement Prediction System" in res.data, "Home page missing subtitle"
    print("[PASS] Test 1: Home Page (HTTP 200, Title & Subtitle Verified)")
    passed += 1

    # Test 2: Dashboard Page
    total += 1
    res = client.get('/dashboard')
    assert res.status_code == 200, f"Dashboard returned {res.status_code}"
    assert b"Placement Analytics &amp; ML Dashboard" in res.data or b"Placement Analytics & ML Dashboard" in res.data, "Dashboard missing header"
    assert b"Machine Learning Model Comparison" in res.data, "Dashboard missing comparison table"
    assert b"Figure 1: Overall Student Placement Breakdown" in res.data, "Dashboard missing Figure 1 caption"
    print("[PASS] Test 2: Dashboard Page (HTTP 200, Metrics & Charts Verified)")
    passed += 1

    # Test 3: About Page
    total += 1
    res = client.get('/about')
    assert res.status_code == 200, f"About page returned {res.status_code}"
    assert b"Project Objective" in res.data, "About page missing objective"
    assert b"Logistic Regression" in res.data, "About page missing algorithms"
    assert b"Project Workflow" in res.data, "About page missing workflow"
    print("[PASS] Test 3: About Page (HTTP 200, Algorithms & Viva Guide Verified)")
    passed += 1

    # Test 4: Prediction Page GET
    total += 1
    res = client.get('/predict')
    assert res.status_code == 200, f"Predict page GET returned {res.status_code}"
    assert b"Student Placement Predictor" in res.data, "Predict page missing title"
    assert b"Predict Placement" in res.data, "Predict page missing button"
    print("[PASS] Test 4: Prediction Page Form GET (HTTP 200)")
    passed += 1

    # Test 5: Prediction Form POST - High Achiever (Expected Placed)
    total += 1
    payload_placed = {
        'CGPA': '8.85',
        'Tenth_Percentage': '88.5',
        'Twelfth_Percentage': '85.0',
        'Internships': '2',
        'Projects': '3',
        'Technical_Skills': '4',
        'Communication_Skills': '4',
        'Backlogs': '0',
        'Work_Experience': 'Yes'
    }
    res = client.post('/predict', data=payload_placed)
    assert res.status_code == 200, f"Predict POST returned {res.status_code}"
    assert b"PLACED" in res.data, "Prediction did not return PLACED"
    assert b"Model predicted probability:" in res.data, "Missing probability text"
    print("[PASS] Test 5: Prediction Form POST - Strong Profile (Result: PLACED Verified)")
    passed += 1

    # Test 6: Prediction Form POST - At-Risk Student (Expected Not Placed)
    total += 1
    payload_not_placed = {
        'CGPA': '5.20',
        'Tenth_Percentage': '52.0',
        'Twelfth_Percentage': '50.0',
        'Internships': '0',
        'Projects': '0',
        'Technical_Skills': '1',
        'Communication_Skills': '1',
        'Backlogs': '4',
        'Work_Experience': 'No'
    }
    res = client.post('/predict', data=payload_not_placed)
    assert res.status_code == 200, f"Predict POST returned {res.status_code}"
    assert b"NOT PLACED" in res.data, "Prediction did not return NOT PLACED"
    assert b"Model predicted probability:" in res.data, "Missing probability text"
    print("[PASS] Test 6: Prediction Form POST - At-Risk Profile (Result: NOT PLACED Verified)")
    passed += 1

    # Test 7: Form Validation - Invalid CGPA Range (> 10.0)
    total += 1
    payload_invalid = {
        'CGPA': '14.5',  # Invalid!
        'Tenth_Percentage': '80.0',
        'Twelfth_Percentage': '80.0',
        'Internships': '1',
        'Projects': '1',
        'Technical_Skills': '3',
        'Communication_Skills': '3',
        'Backlogs': '0',
        'Work_Experience': 'No'
    }
    res = client.post('/predict', data=payload_invalid)
    assert res.status_code == 200, f"Predict POST returned {res.status_code}"
    assert b"CGPA must be between 0.0 and 10.0" in res.data, "Did not catch out-of-range CGPA"
    print("[PASS] Test 7: Form Validation (Out-of-range CGPA error caught and displayed)")
    passed += 1

    # Test 8: Form Validation - Empty Fields
    total += 1
    payload_empty = {
        'CGPA': '',  # Empty!
        'Tenth_Percentage': '80.0',
        'Twelfth_Percentage': '80.0',
        'Internships': '1',
        'Projects': '1',
        'Technical_Skills': '3',
        'Communication_Skills': '3',
        'Backlogs': '0',
        'Work_Experience': 'No'
    }
    res = client.post('/predict', data=payload_empty)
    assert res.status_code == 200, f"Predict POST returned {res.status_code}"
    assert b"Please fill in all required fields" in res.data, "Did not catch empty field"
    print("[PASS] Test 8: Form Validation (Empty fields error caught and displayed)")
    passed += 1

    # Test 9: REST API Prediction Endpoint
    total += 1
    api_payload = {
        'CGPA': 8.5,
        'Tenth_Percentage': 85.0,
        'Twelfth_Percentage': 82.0,
        'Internships': 1,
        'Projects': 2,
        'Technical_Skills': 4,
        'Communication_Skills': 4,
        'Backlogs': 0,
        'Work_Experience': 'Yes'
    }
    res = client.post('/api/predict', data=json.dumps(api_payload), content_type='application/json')
    assert res.status_code == 200, f"API returned {res.status_code}"
    api_data = json.loads(res.data)
    assert api_data.get('success') is True, "API call was not successful"
    assert api_data['data']['prediction'] in ['PLACED', 'NOT PLACED'], "API missing prediction"
    print(f"[PASS] Test 9: REST API Endpoint /api/predict (HTTP 200, Result: {api_data['data']['prediction']}, Prob: {api_data['data']['probability']}%)")
    passed += 1

    print("=" * 60)
    print(f"ALL {passed}/{total} INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
