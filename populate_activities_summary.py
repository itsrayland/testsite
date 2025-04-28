import requests
from datetime import datetime
from collections import defaultdict
from airtable_config import AIRTABLE_CONFIG

def get_activities_data():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_CONFIG['PAT']}"
    }
    
    activities_url = f"https://api.airtable.com/v0/{AIRTABLE_CONFIG['BASE_ID']}/Activities"
    all_records = []
    
    try:
        # Fetch all records with pagination
        while True:
            response = requests.get(activities_url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            
            if 'records' in data:
                all_records.extend(data['records'])
                print(f"Fetched {len(data['records'])} records...")
            
            if 'offset' in data:
                activities_url = f"https://api.airtable.com/v0/{AIRTABLE_CONFIG['BASE_ID']}/Activities?offset={data['offset']}"
            else:
                break
    except requests.exceptions.RequestException as e:
        print(f"Error fetching activities: {e}")
        return []
    
    return all_records

def get_quarter(month):
    return f"Q{(month - 1) // 3 + 1}"

def get_month_name(month):
    return datetime(2000, month, 1).strftime('%B')

def aggregate_activities(records):
    summaries = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {
        'total_reach': 0,
        'total_cost': 0,
        'total_peanut_packs': 0,
        'total_peanut_cans': 0,
        'total_pb_jars': 0,
        'total_promo_items': 0,
        'total_materials': 0,
        'total_partners': 0,
        'activity_count': 0,
        'core_programs': set(),
        'focus_areas': set()
    })))
    
    skipped_records = 0
    processed_records = 0
    
    for record in records:
        try:
            fields = record.get('fields', {})
            
            # Try different possible date field names
            date_str = None
            for date_field in ['Date', 'START', 'Start Date', 'Activity Date']:
                if date_field in fields:
                    date_str = fields[date_field]
                    break
            
            if not date_str:
                skipped_records += 1
                continue
                
            date = datetime.strptime(date_str, '%Y-%m-%d')
            year = str(date.year)
            quarter = get_quarter(date.month)
            month = get_month_name(date.month)
            
            summary = summaries[year][quarter][month]
            
            # Print first record's fields for debugging
            if processed_records == 0:
                print("\nFirst record fields:")
                for key, value in fields.items():
                    print(f"{key}: {value}")
            
            # Aggregate numeric fields with various possible field names
            summary['total_reach'] += int(fields.get('Actual Reach', fields.get('REACH: ACTUAL', fields.get('Reach', 0))))
            summary['total_cost'] += float(fields.get('Total Cost', fields.get('TOTAL COST', fields.get('Cost', 0))))
            summary['total_peanut_packs'] += int(fields.get('Actual Peanut Packs', fields.get('PACKS OF PEANUTS: ACTUAL', 0)))
            summary['total_peanut_cans'] += int(fields.get('Actual Peanut Cans', fields.get('CANS OF PEANUTS: ACTUAL', 0)))
            summary['total_pb_jars'] += int(fields.get('Actual PB Jars', fields.get('JARS OF PEANUT BUTTER: ACTUAL', 0)))
            summary['total_promo_items'] += int(fields.get('Actual Promo Items', fields.get('# PROMO ITEMS PROVIDED: ACTUAL', 0)))
            summary['total_materials'] += int(fields.get('Actual Materials', fields.get('Materials Provided: Actual', 0)))
            summary['total_partners'] += int(fields.get('Partners', fields.get('NUMBER OF PARTNERS', 0)))
            summary['activity_count'] += 1
            
            # Aggregate multi-select fields
            core_program = fields.get('Core Program', fields.get('CORE PROGRAM', []))
            focus_area = fields.get('Focus Area', fields.get('FOCUS', []))
            
            if isinstance(core_program, list):
                summary['core_programs'].update(core_program)
            if isinstance(focus_area, list):
                summary['focus_areas'].update(focus_area)
            
            processed_records += 1
            
        except Exception as e:
            print(f"Error processing record: {e}")
            skipped_records += 1
    
    print(f"\nProcessed {processed_records} records")
    print(f"Skipped {skipped_records} records")
    
    return summaries

def clean_value(value):
    # Remove extra spaces and quotes
    return value.strip().strip('"')

def create_summary_record(year, quarter, month, data):
    # Define valid options based on the table schema
    valid_core_programs = {
        "Advocacy",
        "Philanthropy",
        "Promotion",
        "Education",
        "Partnerships"
    }
    
    valid_focus_areas = {
        "Industry",
        "Consumer"
    }
    
    # Clean and filter core programs
    core_programs = set()
    for program in data['core_programs']:
        cleaned = clean_value(program)
        if cleaned in valid_core_programs:
            core_programs.add(cleaned)
    
    # Clean and filter focus areas
    focus_areas = set()
    for area in data['focus_areas']:
        cleaned = clean_value(area)
        if cleaned in valid_focus_areas:
            focus_areas.add(cleaned)
    
    return {
        "fields": {
            "Year": year,
            "Quarter": quarter,
            "Month": month,
            "Total Reach": data['total_reach'],
            "Total Cost": data['total_cost'],
            "Total Peanut Packs": data['total_peanut_packs'],
            "Total Peanut Cans": data['total_peanut_cans'],
            "Total PB Jars": data['total_pb_jars'],
            "Total Promo Items": data['total_promo_items'],
            "Total Materials": data['total_materials'],
            "Total Partners": data['total_partners'],
            "Activity Count": data['activity_count'],
            "Core Programs": list(core_programs),
            "Focus Areas": list(focus_areas)
        }
    }

def populate_activities_summary():
    print("Fetching activities data...")
    records = get_activities_data()
    print(f"Found {len(records)} activities")
    
    if not records:
        print("No activities found. Exiting.")
        return
    
    print("\nAggregating data...")
    summaries = aggregate_activities(records)
    
    if not summaries:
        print("No summaries generated. Exiting.")
        return
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_CONFIG['PAT']}",
        "Content-Type": "application/json"
    }
    
    summary_url = f"https://api.airtable.com/v0/{AIRTABLE_CONFIG['BASE_ID']}/Activities%20Summary"
    
    print("\nPopulating summary table...")
    success_count = 0
    error_count = 0
    
    for year in summaries:
        for quarter in summaries[year]:
            for month in summaries[year][quarter]:
                try:
                    data = summaries[year][quarter][month]
                    record = create_summary_record(year, quarter, month, data)
                    
                    response = requests.post(summary_url, headers=headers, json={"records": [record]})
                    response.raise_for_status()
                    
                    print(f"Successfully created summary for {month} {year}")
                    success_count += 1
                    
                except requests.exceptions.RequestException as e:
                    print(f"Error creating summary for {month} {year}: {e}")
                    if hasattr(e.response, 'text'):
                        print(f"Response: {e.response.text}")
                    error_count += 1
    
    print(f"\nSummary:")
    print(f"Successfully created {success_count} summaries")
    print(f"Failed to create {error_count} summaries")

if __name__ == "__main__":
    populate_activities_summary() 