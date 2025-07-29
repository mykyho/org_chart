import pandas as pd
import re
from collections import defaultdict

def clean_symetra_data():
    # Read the CSV file with encoding handling
    try:
        df = pd.read_csv('/Users/mykyho/Desktop/Myky Callsheet (MAIN).csv', encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv('/Users/mykyho/Desktop/Myky Callsheet (MAIN).csv', encoding='latin-1')
        except UnicodeDecodeError:
            df = pd.read_csv('/Users/mykyho/Desktop/Myky Callsheet (MAIN).csv', encoding='cp1252')
    
    # Filter for current Symetra employees only
    symetra_df = df[df['Company'] == 'Symetra'].copy()
    
    # Remove people who are no longer at Symetra
    # Look for indicators in the data that suggest they're no longer there
    current_indicators = [
        'No longer there',
        'Doesn\'t work there anymore',
        'Dead link',
        'hiring senior analytics engineer'
    ]
    
    # Filter out rows with these indicators
    for indicator in current_indicators:
        symetra_df = symetra_df[~symetra_df.apply(lambda x: x.astype(str).str.contains(indicator, case=False, na=False)).any(axis=1)]
    
    # Clean up job titles and identify hierarchy levels
    def categorize_level(job_title):
        if pd.isna(job_title):
            return 'Unknown'
        
        job_title = str(job_title).lower()
        
        # C-suite and top executives
        if any(word in job_title for word in ['chief', 'president', 'ceo', 'cto', 'cio', 'cfo']):
            return 'C-Suite'
        
        # Senior Vice Presidents
        if 'senior vice president' in job_title or 'senior vp' in job_title:
            return 'Senior VP'
        
        # Vice Presidents
        if 'vice president' in job_title or 'vp' in job_title:
            return 'VP'
        
        # Assistant Vice Presidents
        if 'assistant vp' in job_title or 'assistant vice president' in job_title:
            return 'Assistant VP'
        
        # Directors
        if 'director' in job_title:
            return 'Director'
        
        # Senior Managers
        if 'senior manager' in job_title:
            return 'Senior Manager'
        
        # Managers
        if 'manager' in job_title:
            return 'Manager'
        
        # Senior positions
        if 'senior' in job_title:
            return 'Senior'
        
        # Lead positions
        if 'lead' in job_title:
            return 'Lead'
        
        return 'Individual Contributor'
    
    # Apply categorization
    symetra_df['Level'] = symetra_df['Job Title'].apply(categorize_level)
    
    # Clean up names
    symetra_df['Full Name'] = symetra_df['First Name'] + ' ' + symetra_df['Last Name']
    
    # Sort by level hierarchy
    level_order = {
        'C-Suite': 1,
        'Senior VP': 2,
        'VP': 3,
        'Assistant VP': 4,
        'Director': 5,
        'Senior Manager': 6,
        'Manager': 7,
        'Senior': 8,
        'Lead': 9,
        'Individual Contributor': 10,
        'Unknown': 11
    }
    
    symetra_df['Level Order'] = symetra_df['Level'].map(level_order)
    symetra_df = symetra_df.sort_values(['Level Order', 'Full Name'])
    
    return symetra_df

def identify_c_suite(df):
    """Identify C-suite executives"""
    c_suite = df[df['Level'] == 'C-Suite']
    return c_suite

def identify_senior_vps(df):
    """Identify Senior Vice Presidents"""
    senior_vps = df[df['Level'] == 'Senior VP']
    return senior_vps

def create_org_chart(df):
    """Create a simple text-based org chart"""
    chart = []
    chart.append("SYMETRA ORGANIZATIONAL CHART")
    chart.append("=" * 50)
    chart.append("")
    
    # Group by level
    for level in ['C-Suite', 'Senior VP', 'VP', 'Assistant VP', 'Director', 'Senior Manager', 'Manager']:
        level_data = df[df['Level'] == level]
        if not level_data.empty:
            chart.append(f"\n{level.upper()}:")
            chart.append("-" * len(level))
            for _, row in level_data.iterrows():
                chart.append(f"  • {row['Full Name']} - {row['Job Title']}")
    
    return "\n".join(chart)

def analyze_departments(df):
    """Analyze by department/function"""
    dept_analysis = df.groupby('Job Function').agg({
        'Full Name': 'count',
        'Level': lambda x: list(x)
    }).rename(columns={'Full Name': 'Count'})
    
    return dept_analysis

if __name__ == "__main__":
    # Clean and analyze the data
    symetra_df = clean_symetra_data()
    
    print("CURRENT SYMETRA EMPLOYEES ANALYSIS")
    print("=" * 50)
    print(f"Total current employees: {len(symetra_df)}")
    print()
    
    # Identify C-suite
    c_suite = identify_c_suite(symetra_df)
    print("C-SUITE EXECUTIVES:")
    print("-" * 30)
    if not c_suite.empty:
        for _, row in c_suite.iterrows():
            print(f"• {row['Full Name']} - {row['Job Title']}")
    else:
        print("No C-suite executives identified in the data")
    print()
    
    # Identify Senior VPs
    senior_vps = identify_senior_vps(symetra_df)
    print("SENIOR VICE PRESIDENTS:")
    print("-" * 30)
    if not senior_vps.empty:
        for _, row in senior_vps.iterrows():
            print(f"• {row['Full Name']} - {row['Job Title']}")
    else:
        print("No Senior VPs identified in the data")
    print()
    
    # Create org chart
    org_chart = create_org_chart(symetra_df)
    print(org_chart)
    print()
    
    # Department analysis
    print("DEPARTMENT ANALYSIS:")
    print("-" * 30)
    dept_analysis = analyze_departments(symetra_df)
    for dept, data in dept_analysis.iterrows():
        print(f"{dept}: {data['Count']} employees")
    
    # Save detailed results to CSV
    symetra_df.to_csv('symetra_current_employees.csv', index=False)
    print(f"\nDetailed data saved to 'symetra_current_employees.csv'") 