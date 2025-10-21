import argparse
import requests


GCP_DEV = 'https://backend-dev-811210300089.us-east4.run.app/'
LOCAL_HOST = "http://localhost:8000/"
GCP_PROD = 'https://rootlogic-crm-811210300089.us-east4.run.app/'

parser = argparse.ArgumentParser(description="Run API tests")


urls = {
    'dev': GCP_DEV,
    'local': LOCAL_HOST,
    'prod': GCP_PROD
}

parser.add_argument('-k', '--key', type=str, choices=urls.keys(), help='Key to select the base URL from predefined options')

args = parser.parse_args()
BASE_URL = urls[args.key]
print(f"Using BASE_URL: {BASE_URL}")

def test_customer_crud():
    print("Testing Customer CRUD...")
    
    uri = f"api/customers/"

    # Create
    response = requests.post(f"{BASE_URL}{uri}", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone_number": "1234567890"
    })

    print("Create Response:", response.status_code, response.text)
    assert response.status_code == 201
    customer_id = response.json()['id']
    print(f"Created customer: {customer_id}")
    
    # Read
    uri = f"api/customers/{customer_id}/"
    response = requests.get(f"{BASE_URL}{uri}")
    assert response.status_code == 200
    print("Retrieved customer")
    
    # Update
    uri = f"api/customers/{customer_id}/"
    response = requests.patch(f"{BASE_URL}{uri}", json={
        "phone_number": "9876543210"
    })
    assert response.status_code == 200
    assert response.json()['phone_number'] == "9876543210"
    print("Updated customer")
    
    # Delete
    uri = f"api/customers/{customer_id}/"
    response = requests.delete(f"{BASE_URL}{uri}")
    assert response.status_code == 204
    print("Deleted customer")
    
    print("\nAll Customer CRUD tests passed!")


def test_customer_email_validation():
    print("Testing Customer Email Validation...")
    
    uri = f"api/customers/"

    # Create with invalid email
    response = requests.post(f"{BASE_URL}{uri}", json={
        "first_name": "Invalid",
        "last_name": "Email",
        "email": "invalid-email",
        "phone_number": "1234567890"
    })

    print("Create with invalid email Response:", response.status_code, response.text)
    assert response.status_code == 400
    assert "Enter a valid email address." in response.text
    print("Email validation test passed!")

def test_customer_phone_validation():
    print("Testing Customer Phone Number Validation...")
    
    uri = f"api/customers/"

    # Create with invalid phone number
    response = requests.post(f"{BASE_URL}{uri}", json={
        "first_name": "Invalid",
        "last_name": "Phone",
        "email": "e@e.io",
        "phone_number": "12345"
    })
    print("Create with invalid phone Response:", response.status_code, response.text)
    assert response.status_code == 400
    assert "Phone number must have at least 10 digits" in response.text
    print("Phone number validation test passed!")

def test_customer_phone_uniqueness():
    print("Testing Customer Phone Number Uniqueness Validation...")
    
    uri = f"api/customers/"

    # Create first customer
    response = requests.post(f"{BASE_URL}{uri}", json={
        "first_name": "Unique",
        "last_name": "Phone1",
        "email": "a@a.com",
        "phone_number": "+12345678901"
    })
    unique1_id = response.json().get('id')
    assert response.status_code == 201
    print("Created first customer with unique phone number")
    # Create second customer with same phone number
    response = requests.post(f"{BASE_URL}{uri}", json={
        "first_name": "Unique",
        "last_name": "Phone2",
        "email": "b@b.com",
        "phone_number": "+12345678901"
    })
    print("Create with duplicate phone Response:", response.status_code, response.text)
    assert response.status_code == 400
    assert "A customer with this phone number already exists." in response.text
    print("Phone number uniqueness validation test passed!")

    # Cleanup
    uri = f"api/customers/{unique1_id}/"
    response = requests.delete(f"{BASE_URL}{uri}")
    assert response.status_code == 204
    print("Cleaned up created customer")

def test_email_uniqueness():
    print("Testing Customer Email Uniqueness Validation...")
    
    uri = f"api/customers/"

    # Create first customer
    response = requests.post(f"{BASE_URL}{uri}", json={
        "first_name": "Unique",
        "last_name": "Email1",
        "email": "a@a.com",
        "phone_number": "1234567890"
    })
    unique1_id = response.json().get('id')
    assert response.status_code == 201
    print("Created first customer with unique email")
    # Create second customer with same email
    response = requests.post(f"{BASE_URL}{uri}", json={
        "first_name": "Unique",
        "last_name": "Email2",
        "email": "a@a.com",
        "phone_number": "0987654321"
    })
    print("Create with duplicate email Response:", response.status_code, response.text)
    assert response.status_code == 400
    print("Email uniqueness validation test passed!")
    # Cleanup
    uri = f"api/customers/{unique1_id}/"
    response = requests.delete(f"{BASE_URL}{uri}")
    assert response.status_code == 204
    print("Cleaned up created customer")

if __name__ == "__main__":
    test_customer_crud()
    test_customer_email_validation()
    test_customer_phone_validation()
    test_customer_phone_uniqueness()
    test_email_uniqueness()