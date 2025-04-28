import requests
from airtable_config import AIRTABLE_CONFIG

def create_activities_summary_table():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_CONFIG['PAT']}",
        "Content-Type": "application/json"
    }
    
    # Define the table schema
    table_data = {
        "name": "Activities Summary",
        "description": "Quarterly and monthly summary of Activities data",
        "fields": [
            {
                "name": "Year",
                "type": "singleLineText",
                "description": "Year of the summary"
            },
            {
                "name": "Quarter",
                "type": "singleSelect",
                "description": "Quarter of the year",
                "options": {
                    "choices": [
                        {"name": "Q1"},
                        {"name": "Q2"},
                        {"name": "Q3"},
                        {"name": "Q4"}
                    ]
                }
            },
            {
                "name": "Month",
                "type": "singleSelect",
                "description": "Month of the year",
                "options": {
                    "choices": [
                        {"name": "January"},
                        {"name": "February"},
                        {"name": "March"},
                        {"name": "April"},
                        {"name": "May"},
                        {"name": "June"},
                        {"name": "July"},
                        {"name": "August"},
                        {"name": "September"},
                        {"name": "October"},
                        {"name": "November"},
                        {"name": "December"}
                    ]
                }
            },
            {
                "name": "Total Reach",
                "type": "number",
                "description": "Sum of actual reach across all activities",
                "options": {
                    "precision": 0
                }
            },
            {
                "name": "Total Cost",
                "type": "currency",
                "description": "Sum of total costs across all activities",
                "options": {
                    "precision": 2,
                    "symbol": "$"
                }
            },
            {
                "name": "Total Peanut Packs",
                "type": "number",
                "description": "Sum of actual peanut packs distributed",
                "options": {
                    "precision": 0
                }
            },
            {
                "name": "Total Peanut Cans",
                "type": "number",
                "description": "Sum of actual peanut cans distributed",
                "options": {
                    "precision": 0
                }
            },
            {
                "name": "Total PB Jars",
                "type": "number",
                "description": "Sum of actual peanut butter jars distributed",
                "options": {
                    "precision": 0
                }
            },
            {
                "name": "Total Promo Items",
                "type": "number",
                "description": "Sum of actual promotional items distributed",
                "options": {
                    "precision": 0
                }
            },
            {
                "name": "Total Materials",
                "type": "number",
                "description": "Sum of actual materials provided",
                "options": {
                    "precision": 0
                }
            },
            {
                "name": "Total Partners",
                "type": "number",
                "description": "Sum of partners involved",
                "options": {
                    "precision": 0
                }
            },
            {
                "name": "Activity Count",
                "type": "number",
                "description": "Number of activities in this period",
                "options": {
                    "precision": 0
                }
            },
            {
                "name": "Core Programs",
                "type": "multipleSelects",
                "description": "Core programs involved in this period",
                "options": {
                    "choices": [
                        {"name": "Advocacy"},
                        {"name": "Philanthropy"},
                        {"name": "Promotion"},
                        {"name": "Education"},
                        {"name": "Partnerships"}
                    ]
                }
            },
            {
                "name": "Focus Areas",
                "type": "multipleSelects",
                "description": "Focus areas covered in this period",
                "options": {
                    "choices": [
                        {"name": "Industry"},
                        {"name": "Consumer"}
                    ]
                }
            },
            {
                "name": "Notes",
                "type": "multilineText",
                "description": "Additional notes about the period"
            }
        ]
    }
    
    # Create the table
    base_url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_CONFIG['BASE_ID']}/tables"
    response = requests.post(base_url, headers=headers, json=table_data)
    
    if response.status_code == 200:
        print("Successfully created Activities Summary table!")
        print(response.json())
    else:
        print(f"Error creating table: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    create_activities_summary_table() 