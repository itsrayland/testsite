import requests
from airtable_config import AIRTABLE_CONFIG

def create_test_table():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_CONFIG['PAT']}",
        "Content-Type": "application/json"
    }
    
    # Define the table schema
    table_data = {
        "name": "TEST",
        "description": "Test table with a single field",
        "fields": [
            {
                "name": "field",
                "type": "singleLineText",
                "description": "Test single line text field"
            }
        ]
    }
    
    # Create the table
    base_url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_CONFIG['BASE_ID']}/tables"
    response = requests.post(base_url, headers=headers, json=table_data)
    
    if response.status_code == 200:
        print("Successfully created TEST table!")
        print(response.json())
    else:
        print(f"Error creating table: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    create_test_table() 