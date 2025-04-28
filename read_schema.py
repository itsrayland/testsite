import requests
import json

# Airtable API configuration
AIRTABLE_PAT = "patWHuF2gFQ21OC7T.e9547c1767d09023fe68ab84daeb70ffc07aa5327458b55a7a17bfad6ebde39d"
BASE_ID = "appsCxfQMU3zteRBo"
BASE_URL = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"

def read_schema():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PAT}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(BASE_URL, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("\nAirtable Base Schema:")
        print("=====================")
        
        for table in data.get('tables', []):
            print(f"\nTable: {table['name']}")
            print(f"ID: {table['id']}")
            print(f"Description: {table.get('description', 'No description')}")
            print("\nFields:")
            print("-------")
            
            for field in table.get('fields', []):
                field_type = field['type']
                field_name = field['name']
                field_id = field['id']
                
                # Handle different field types
                if field_type == 'singleSelect':
                    choices = [choice['name'] for choice in field['options']['choices']]
                    print(f"  - {field_name} ({field_type})")
                    print(f"    ID: {field_id}")
                    print(f"    Options: {', '.join(choices)}")
                elif field_type == 'multipleSelect':
                    choices = [choice['name'] for choice in field['options']['choices']]
                    print(f"  - {field_name} ({field_type})")
                    print(f"    ID: {field_id}")
                    print(f"    Options: {', '.join(choices)}")
                else:
                    print(f"  - {field_name} ({field_type})")
                    print(f"    ID: {field_id}")
                
                if 'description' in field:
                    print(f"    Description: {field['description']}")
                print()
            
            print("Views:")
            print("------")
            for view in table.get('views', []):
                print(f"  - {view['name']} ({view['type']})")
                print(f"    ID: {view['id']}")
            print("\n" + "="*50)
    else:
        print(f"Error reading schema: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    read_schema() 