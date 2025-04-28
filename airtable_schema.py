import requests
import json

# Airtable API configuration
AIRTABLE_PAT = "patWHuF2gFQ21OC7T.e9547c1767d09023fe68ab84daeb70ffc07aa5327458b55a7a17bfad6ebde39d"
BASE_URL = "https://api.airtable.com/v0/meta/bases"

def get_bases():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PAT}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching bases: {response.status_code}")
        print(response.text)
        return None

def get_base_schema(base_id):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PAT}",
        "Content-Type": "application/json"
    }
    
    url = f"{BASE_URL}/{base_id}/tables"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching schema: {response.status_code}")
        print(response.text)
        return None

def main():
    # First, get all bases
    bases = get_bases()
    if not bases:
        return
    
    print("Available Bases:")
    print("----------------")
    for base in bases.get('bases', []):
        print(f"Base ID: {base['id']}")
        print(f"Name: {base['name']}")
        print("----------------")
        
        # Get schema for each base
        schema = get_base_schema(base['id'])
        if schema:
            print("\nTables in this base:")
            print("-------------------")
            for table in schema.get('tables', []):
                print(f"\nTable: {table['name']}")
                print("Fields:")
                for field in table.get('fields', []):
                    print(f"  - {field['name']} ({field['type']})")
                print("-------------------")

if __name__ == "__main__":
    main() 