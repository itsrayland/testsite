import requests
from airtable_config import AIRTABLE_CONFIG

def clear_summaries():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_CONFIG['PAT']}"
    }
    
    # First, get all records from the summary table
    summary_url = f"https://api.airtable.com/v0/{AIRTABLE_CONFIG['BASE_ID']}/Activities%20Summary"
    all_records = []
    
    print("Fetching existing summaries...")
    while True:
        response = requests.get(summary_url, headers=headers)
        data = response.json()
        
        if 'records' in data:
            all_records.extend(data['records'])
            print(f"Found {len(data['records'])} records...")
        
        if 'offset' in data:
            summary_url = f"https://api.airtable.com/v0/{AIRTABLE_CONFIG['BASE_ID']}/Activities%20Summary?offset={data['offset']}"
        else:
            break
    
    if not all_records:
        print("No existing summaries found.")
        return
    
    print(f"\nDeleting {len(all_records)} summaries...")
    # Delete records in batches of 10
    for i in range(0, len(all_records), 10):
        batch = all_records[i:i+10]
        record_ids = [record['id'] for record in batch]
        
        response = requests.delete(
            summary_url,
            headers=headers,
            json={"records": record_ids}
        )
        
        if response.status_code == 200:
            print(f"Successfully deleted batch {i//10 + 1}")
        else:
            print(f"Error deleting batch {i//10 + 1}: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    clear_summaries() 