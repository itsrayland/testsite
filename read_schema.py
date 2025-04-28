import requests
import json
from airtable_config import AIRTABLE_CONFIG

def read_schema():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_CONFIG['PAT']}",
        "Content-Type": "application/json"
    }
    
    # Get base schema
    base_url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_CONFIG['BASE_ID']}/tables"
    response = requests.get(base_url, headers=headers)
    
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
                print(f"\n{field['name']} ({field['type']})")
                print(f"  - Field ID: {field['id']}")
                
                # Print options for select fields
                if field['type'] in ['singleSelect', 'multipleSelects']:
                    options = field.get('options', {}).get('choices', [])
                    if options:
                        print("  - Options:")
                        for option in options:
                            print(f"    → {option['name']}")
                
                # Print linked table info for linked fields
                if field['type'] in ['multipleRecordLinks', 'singleRecordLink']:
                    linked_table = field.get('options', {}).get('linkedTableId')
                    if linked_table:
                        print(f"  - Linked to: {linked_table}")
            
            print("\n-------------------")
    else:
        print(f"Error fetching schema: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    read_schema() 