import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from collections import defaultdict
from airtable_config import AIRTABLE_CONFIG

def get_summary_data():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_CONFIG['PAT']}"
    }
    
    summary_url = f"https://api.airtable.com/v0/{AIRTABLE_CONFIG['BASE_ID']}/Activities%20Summary"
    all_records = []
    
    print("Fetching summary data...")
    while True:
        response = requests.get(summary_url, headers=headers)
        data = response.json()
        
        if 'records' in data:
            all_records.extend(data['records'])
        
        if 'offset' in data:
            summary_url = f"https://api.airtable.com/v0/{AIRTABLE_CONFIG['BASE_ID']}/Activities%20Summary?offset={data['offset']}"
        else:
            break
    
    return all_records

def create_visualizations():
    records = get_summary_data()
    
    if not records:
        print("No data found to visualize.")
        return
    
    # Convert records to DataFrame
    data = []
    for record in records:
        fields = record['fields']
        data.append({
            'Year': fields['Year'],
            'Quarter': fields['Quarter'],
            'Month': fields['Month'],
            'Total Reach': fields['Total Reach'],
            'Total Cost': fields['Total Cost'],
            'Activity Count': fields['Activity Count'],
            'Total Peanut Packs': fields['Total Peanut Packs'],
            'Total Peanut Cans': fields['Total Peanut Cans'],
            'Total PB Jars': fields['Total PB Jars'],
            'Core Programs': fields.get('Core Programs', []),
            'Focus Areas': fields.get('Focus Areas', [])
        })
    
    df = pd.DataFrame(data)
    
    # Set style
    plt.style.use('seaborn')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Monthly Activity Count
    plt.subplot(2, 2, 1)
    monthly_activities = df.groupby('Month')['Activity Count'].sum().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    monthly_activities.plot(kind='bar')
    plt.title('Monthly Activity Distribution')
    plt.xlabel('Month')
    plt.ylabel('Number of Activities')
    plt.xticks(rotation=45)
    
    # 2. Quarterly Trends
    plt.subplot(2, 2, 2)
    quarterly_data = df.groupby(['Year', 'Quarter']).agg({
        'Activity Count': 'sum',
        'Total Reach': 'sum',
        'Total Cost': 'sum'
    }).reset_index()
    quarterly_data['Period'] = quarterly_data['Year'] + '-' + quarterly_data['Quarter']
    
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    ax1.plot(quarterly_data['Period'], quarterly_data['Activity Count'], 'b-', label='Activities')
    ax2.plot(quarterly_data['Period'], quarterly_data['Total Cost'], 'r-', label='Cost')
    
    ax1.set_xlabel('Quarter')
    ax1.set_ylabel('Number of Activities', color='b')
    ax2.set_ylabel('Total Cost ($)', color='r')
    plt.title('Quarterly Activity and Cost Trends')
    
    # 3. Distribution of Products
    plt.subplot(2, 2, 3)
    product_data = df[['Total Peanut Packs', 'Total Peanut Cans', 'Total PB Jars']].sum()
    product_data.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Products Distributed')
    
    # 4. Cost vs Reach Scatter
    plt.subplot(2, 2, 4)
    plt.scatter(df['Total Cost'], df['Total Reach'], alpha=0.6)
    plt.title('Cost vs Reach Relationship')
    plt.xlabel('Total Cost ($)')
    plt.ylabel('Total Reach')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('activities_visualizations.png', dpi=300, bbox_inches='tight')
    print("Visualizations have been saved to activities_visualizations.png")
    
    # Create additional visualizations
    fig2 = plt.figure(figsize=(20, 10))
    
    # 5. Monthly Reach Trends
    plt.subplot(1, 2, 1)
    monthly_reach = df.groupby('Month')['Total Reach'].sum().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    monthly_reach.plot(kind='line', marker='o')
    plt.title('Monthly Reach Trends')
    plt.xlabel('Month')
    plt.ylabel('Total Reach')
    plt.xticks(rotation=45)
    
    # 6. Cost per Activity by Month
    plt.subplot(1, 2, 2)
    df['Cost per Activity'] = df['Total Cost'] / df['Activity Count']
    monthly_cost = df.groupby('Month')['Cost per Activity'].mean().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    monthly_cost.plot(kind='bar')
    plt.title('Average Cost per Activity by Month')
    plt.xlabel('Month')
    plt.ylabel('Average Cost per Activity ($)')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('activities_trends.png', dpi=300, bbox_inches='tight')
    print("Additional visualizations have been saved to activities_trends.png")

if __name__ == "__main__":
    create_visualizations() 