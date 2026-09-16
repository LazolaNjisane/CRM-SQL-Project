import pandas as pd
import numpy as np
import seaborn as sns

# Load the dataset
accounts = pd.read_csv('/Users/lazolanjisane/Documents/Workspace/VS Code Projects/CRM Projects/CRM Datasets/Origianl_CRM_Dataset/accounts.csv')
products = pd.read_csv('/Users/lazolanjisane/Documents/Workspace/VS Code Projects/CRM Projects/CRM Datasets/Origianl_CRM_Dataset/products.csv')
sales_pipeline = pd.read_csv('/Users/lazolanjisane/Documents/Workspace/VS Code Projects/CRM Projects/CRM Datasets/Origianl_CRM_Dataset/sales_pipeline.csv')
sales_teams = pd.read_csv('/Users/lazolanjisane/Documents/Workspace/VS Code Projects/CRM Projects/CRM Datasets/Origianl_CRM_Dataset/sales_teams.csv')

#Creating master function
def generate_custom_id(df, source_column, id_num, padding=4):
    sequence = range(1, len(df) + 1)
    pad_num = pd.Series(sequence).apply(lambda x: str(x).zfill(padding))
    prefixes = df[source_column].astype(str).str[:2].str.strip().str.upper()
    df[id_num] = prefixes + pad_num
    df = df[[id_num] + [col for col in df.columns if col != id_num]]
    return df.set_index(id_num)

#Dictionary for actual dataframes
data_cabinet = {
    'accounts': accounts,
    'products': products,
    'sales_teams': sales_teams
}

# #Dictionary for table configuration
table_config = {
    'accounts': {
        'source_column': 'account',        
        'id_num': 'account_ID', 
        'padding': 3
    },
    'products': {
        'source_column': 'series',
        'id_num': 'product_ID',
        'padding': 4
    },
    'sales_teams': {
        'source_column': 'regional_office',
        'id_num': 'team_ID',
        'padding': 4
    }
}

# Apply the function to each dataframe
for key, config in table_config.items():
    actual_data = data_cabinet[key].copy()
    cleaned_ver = generate_custom_id(
        df = actual_data, 
        source_column=config['source_column'], 
        id_num=config['id_num'], 
        padding=config['padding'])
    data_cabinet[key] = cleaned_ver

# Store new data cabinets into their dataframes

accounts = data_cabinet['accounts']
products = data_cabinet['products']
sales_teams = data_cabinet['sales_teams']

print("All dataframes have been updated and saved with new IDs.")

#Rename columns
accounts.rename(columns={'revenue': 'revenue_in_mill'}, inplace=True)

# Creating a duration column in pipelines table
close_date = pd.to_datetime(sales_pipeline['close_date'])
engage_date = pd.to_datetime(sales_pipeline['engage_date'])
duration = (close_date - engage_date).dt.days

sales_pipeline['duration'] = duration.astype('Int64')

print(sales_pipeline[['opportunity_id', 'sales_agent', 'product', 'account', 'deal_stage', 'engage_date', 'close_date','duration', 'close_value']].head())

# Column for company size in accounts
#Convert to Millions
def determine_company_size(accounts):
    # Pull individual row data from the conveyor belt
    revenue_in_mills = accounts['revenue_in_mill'] * 1_000
    emp = accounts['employees']
    
    # Tier 4: Large Enterprises & Corporations ($1 Billion+ OR 2,000+ employees)
    if revenue_in_mills >= 1_000_000_000 or emp >= 2000:
        return 'Large Enterprise & Corporation'
    
    # Tier 3: Mid-Market / Mid-Size Enterprises ($50M to $1B OR 250 to 1,999 employees)
    elif (1_000_000_000  <= revenue_in_mills < 50_000_000) or (250 <= emp < 2000):
        return 'Mid-Market / Mid-Size Enterprise'
    
    # Tier 2: Medium Businesses ($10M to $50M OR 50 to 249 employees)
    elif (50_000_000 <= revenue_in_mills <= 1_000_000_000) or (50 <= emp <= 250):
        return 'Medium Business'
    
    # Tier 1: Small Businesses (Under $10M and under 50 employees)
    else:
        return 'Small Business'

# This runs the function row-by-row and saves the list of results into the variable
business_type = accounts.apply(determine_company_size, axis=1)

# Now attach that compiled data straight to your table as a new column
accounts['business_type'] = business_type

# Change data types in sales pipeline
sales_pipeline[['close_date','engage_date']] = sales_pipeline[['close_date','engage_date']].astype('datetime64[us]')

# Print dataframes
print("--- ACCOUNTS ---")
print(accounts.head())

print("--- Sales Pipeline ---")
print(sales_pipeline.set_index('opportunity_id').head())

print("\n--- PRODUCTS ---")
print(products.head())

print("\n--- TEAMS ---")
print(sales_teams.head())

# null values in business_type
print("\nNull values in business_type column:")
print(sales_pipeline.isnull().sum())

# #Downlaod dataframes to csv
accounts.to_csv('/Users/lazolanjisane/Documents/Workspace/VS Code Projects/CRM Projects/CRM Datasets/Updated_CRM_Dataset/accounts_updated.csv')
products.to_csv('/Users/lazolanjisane/Documents/Workspace/VS Code Projects/CRM Projects/CRM Datasets/Updated_CRM_Dataset/products_updated.csv')
sales_teams.to_csv('/Users/lazolanjisane/Documents/Workspace/VS Code Projects/CRM Projects/CRM Datasets/Updated_CRM_Dataset/sales_teams_updated.csv')
sales_pipeline.to_csv('/Users/lazolanjisane/Documents/Workspace/VS Code Projects/CRM Projects/CRM Datasets/Updated_CRM_Dataset/sales_pipeline_updated.csv')
