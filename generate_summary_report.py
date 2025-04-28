import requests
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

def generate_report():
    records = get_summary_data()
    
    if not records:
        return "No summary data found."
    
    # Initialize data structures for analysis
    yearly_data = defaultdict(lambda: defaultdict(int))
    quarterly_data = defaultdict(lambda: defaultdict(int))
    program_data = defaultdict(lambda: defaultdict(int))
    focus_area_data = defaultdict(lambda: defaultdict(int))
    
    # Process records
    for record in records:
        fields = record['fields']
        year = fields['Year']
        quarter = fields['Quarter']
        month = fields['Month']
        
        # Yearly aggregations
        yearly_data[year]['total_reach'] += fields['Total Reach']
        yearly_data[year]['total_cost'] += fields['Total Cost']
        yearly_data[year]['total_activities'] += fields['Activity Count']
        yearly_data[year]['total_peanut_packs'] += fields['Total Peanut Packs']
        yearly_data[year]['total_peanut_cans'] += fields['Total Peanut Cans']
        yearly_data[year]['total_pb_jars'] += fields['Total PB Jars']
        
        # Quarterly aggregations
        quarterly_data[f"{year}-{quarter}"]['total_reach'] += fields['Total Reach']
        quarterly_data[f"{year}-{quarter}"]['total_cost'] += fields['Total Cost']
        quarterly_data[f"{year}-{quarter}"]['total_activities'] += fields['Activity Count']
        
        # Program and focus area analysis
        for program in fields.get('Core Programs', []):
            program_data[program]['total_activities'] += fields['Activity Count']
            program_data[program]['total_reach'] += fields['Total Reach']
            program_data[program]['total_cost'] += fields['Total Cost']
        
        for area in fields.get('Focus Areas', []):
            focus_area_data[area]['total_activities'] += fields['Activity Count']
            focus_area_data[area]['total_reach'] += fields['Total Reach']
            focus_area_data[area]['total_cost'] += fields['Total Cost']
    
    # Generate report
    report = []
    report.append("ACTIVITIES SUMMARY REPORT")
    report.append("=" * 50)
    report.append("\n1. YEARLY OVERVIEW")
    report.append("-" * 30)
    
    # Yearly summary
    for year in sorted(yearly_data.keys()):
        data = yearly_data[year]
        report.append(f"\n{year}:")
        report.append(f"  Total Activities: {data['total_activities']}")
        report.append(f"  Total Reach: {data['total_reach']:,}")
        report.append(f"  Total Cost: ${data['total_cost']:,.2f}")
        report.append(f"  Total Peanut Packs: {data['total_peanut_packs']:,}")
        report.append(f"  Total Peanut Cans: {data['total_peanut_cans']:,}")
        report.append(f"  Total PB Jars: {data['total_pb_jars']:,}")
        if data['total_activities'] > 0:
            report.append(f"  Average Cost per Activity: ${data['total_cost']/data['total_activities']:,.2f}")
            report.append(f"  Average Reach per Activity: {data['total_reach']/data['total_activities']:,.0f}")
    
    # Quarterly summary
    report.append("\n\n2. QUARTERLY TRENDS")
    report.append("-" * 30)
    for period in sorted(quarterly_data.keys()):
        data = quarterly_data[period]
        report.append(f"\n{period}:")
        report.append(f"  Total Activities: {data['total_activities']}")
        report.append(f"  Total Reach: {data['total_reach']:,}")
        report.append(f"  Total Cost: ${data['total_cost']:,.2f}")
        if data['total_activities'] > 0:
            report.append(f"  Average Cost per Activity: ${data['total_cost']/data['total_activities']:,.2f}")
            report.append(f"  Average Reach per Activity: {data['total_reach']/data['total_activities']:,.0f}")
    
    # Program analysis
    report.append("\n\n3. PROGRAM ANALYSIS")
    report.append("-" * 30)
    for program in sorted(program_data.keys()):
        data = program_data[program]
        report.append(f"\n{program}:")
        report.append(f"  Total Activities: {data['total_activities']}")
        report.append(f"  Total Reach: {data['total_reach']:,}")
        report.append(f"  Total Cost: ${data['total_cost']:,.2f}")
        if data['total_activities'] > 0:
            report.append(f"  Average Cost per Activity: ${data['total_cost']/data['total_activities']:,.2f}")
            report.append(f"  Average Reach per Activity: {data['total_reach']/data['total_activities']:,.0f}")
    
    # Focus area analysis
    report.append("\n\n4. FOCUS AREA ANALYSIS")
    report.append("-" * 30)
    for area in sorted(focus_area_data.keys()):
        data = focus_area_data[area]
        report.append(f"\n{area}:")
        report.append(f"  Total Activities: {data['total_activities']}")
        report.append(f"  Total Reach: {data['total_reach']:,}")
        report.append(f"  Total Cost: ${data['total_cost']:,.2f}")
        if data['total_activities'] > 0:
            report.append(f"  Average Cost per Activity: ${data['total_cost']/data['total_activities']:,.2f}")
            report.append(f"  Average Reach per Activity: {data['total_reach']/data['total_activities']:,.0f}")
    
    # Key insights
    report.append("\n\n5. KEY INSIGHTS")
    report.append("-" * 30)
    
    # Most active program
    most_active_program = max(program_data.items(), key=lambda x: x[1]['total_activities'])
    report.append(f"\nMost Active Program: {most_active_program[0]} with {most_active_program[1]['total_activities']} activities")
    
    # Most cost-effective program
    cost_effective_program = min(
        [(p, d['total_cost']/d['total_activities']) for p, d in program_data.items() if d['total_activities'] > 0],
        key=lambda x: x[1]
    )
    report.append(f"Most Cost-Effective Program: {cost_effective_program[0]} at ${cost_effective_program[1]:,.2f} per activity")
    
    # Highest reach program
    highest_reach_program = max(
        [(p, d['total_reach']/d['total_activities']) for p, d in program_data.items() if d['total_activities'] > 0],
        key=lambda x: x[1]
    )
    report.append(f"Highest Reach Program: {highest_reach_program[0]} with {highest_reach_program[1]:,.0f} average reach per activity")
    
    # Busiest quarter
    busiest_quarter = max(quarterly_data.items(), key=lambda x: x[1]['total_activities'])
    report.append(f"\nBusiest Quarter: {busiest_quarter[0]} with {busiest_quarter[1]['total_activities']} activities")
    
    # Most expensive quarter
    most_expensive_quarter = max(quarterly_data.items(), key=lambda x: x[1]['total_cost'])
    report.append(f"Most Expensive Quarter: {most_expensive_quarter[0]} with ${most_expensive_quarter[1]['total_cost']:,.2f} total cost")
    
    return "\n".join(report)

def save_report():
    report = generate_report()
    with open("activities_summary_report.txt", "w") as f:
        f.write(report)
    print("Report has been saved to activities_summary_report.txt")

if __name__ == "__main__":
    save_report() 