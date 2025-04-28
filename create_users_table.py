import requests
import json

# Airtable API configuration
AIRTABLE_PAT = "patWHuF2gFQ21OC7T.e9547c1767d09023fe68ab84daeb70ffc07aa5327458b55a7a17bfad6ebde39d"
BASE_ID = "appsCxfQMU3zteRBo"
BASE_URL = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"

def create_users_table():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PAT}",
        "Content-Type": "application/json"
    }
    
    # Define the table schema
    table_data = {
        "name": "Users",
        "description": "Table for managing user information and access",
        "fields": [
            {
                "name": "User ID",
                "type": "singleLineText",
                "description": "Unique identifier for each user"
            },
            {
                "name": "Email",
                "type": "email",
                "description": "User's email address"
            },
            {
                "name": "Full Name",
                "type": "singleLineText",
                "description": "User's full name"
            },
            {
                "name": "Role",
                "type": "singleSelect",
                "options": {
                    "choices": [
                        {"name": "Admin"},
                        {"name": "Manager"},
                        {"name": "User"}
                    ]
                },
                "description": "User's role in the system"
            },
            {
                "name": "Status",
                "type": "singleSelect",
                "options": {
                    "choices": [
                        {"name": "Active"},
                        {"name": "Inactive"},
                        {"name": "Pending"}
                    ]
                },
                "description": "Current user status"
            },
            {
                "name": "Department",
                "type": "singleLineText",
                "description": "User's department or team"
            },
            {
                "name": "Notes",
                "type": "multilineText",
                "description": "Additional notes about the user"
            }
        ]
    }
    
    response = requests.post(BASE_URL, headers=headers, json=table_data)
    
    if response.status_code == 200:
        print("Users table created successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error creating table: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    create_users_table() 