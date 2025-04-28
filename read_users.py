import requests
import json

# Airtable API configuration
AIRTABLE_PAT = "patWHuF2gFQ21OC7T.e9547c1767d09023fe68ab84daeb70ffc07aa5327458b55a7a17bfad6ebde39d"
BASE_ID = "appsCxfQMU3zteRBo"
TABLE_ID = "tblZi7cofdYWRbaW9"  # This is the ID from the table creation response
BASE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

def read_users():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PAT}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(BASE_URL, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("\nUsers in the table:")
        print("------------------")
        
        if not data.get('records'):
            print("No users found in the table yet.")
            return
            
        for record in data['records']:
            fields = record['fields']
            print(f"\nUser ID: {fields.get('User ID', 'N/A')}")
            print(f"Email: {fields.get('Email', 'N/A')}")
            print(f"Full Name: {fields.get('Full Name', 'N/A')}")
            print(f"Role: {fields.get('Role', 'N/A')}")
            print(f"Status: {fields.get('Status', 'N/A')}")
            print(f"Department: {fields.get('Department', 'N/A')}")
            print(f"Notes: {fields.get('Notes', 'N/A')}")
            print("------------------")
    else:
        print(f"Error reading table: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    read_users() 