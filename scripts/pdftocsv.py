import os
import fitz  # PyMuPDF
import pandas as pd
import re
from datetime import datetime

# Define the directory where your PDF files are stored
pdf_directory = 'path/to/folder'  # Change this to your PDF directory

# Ensure the output directory exists and is writable
output_directory = 'path/to/final-folder'
os.makedirs(output_directory, exist_ok=True)
if not os.access(output_directory, os.W_OK):
    print(f"Cannot write to directory: {output_directory}")
    exit(1)  # Exit the script if the directory is not writable

# Initialize a list to hold all the leads
leads_data = []
companies_data = []

# Constants for Deals - set these as per your HubSpot configuration
DEAL_PIPELINE = 'default_pipeline'  # Replace with your pipeline identifier
DEAL_STAGE = 'initial_stage'  # Replace with your deal stage identifier

# Loop through all the PDF files in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        # Open the PDF file
        with fitz.open(os.path.join(pdf_directory, filename)) as pdf:
            # Extract text from the first page
            page_text = pdf[0].get_text()

            # Use regex to find each field in the page text
            email_match = re.search(r'Email: (\S+@\S+)', page_text)
            phone_match = re.search(r'number: ([+\d\s\-\(\)]+)', page_text)
            service_match = re.search(r'Service: (.+)', page_text)
            category = re.search(r'Category: (.+)', page_text)
            city_or_suburb = re.search(r'City or suburb: (.+)', page_text)
            requirement = re.search(r'What do you need\?: (.+)', page_text)
            type_of_website = re.search(r'What type of website do you need\?: (.+)', page_text)
            project_description = re.search(r'Describe your project (.+)', page_text)
            
            # Define 'Deal Name' and 'Company Name'
            deal_name = service_match.group(1).strip() if service_match else 'Unnamed Deal'
            company_name = filename.replace('Lead - ', '').replace('.pdf', '')  # Remove 'Lead - ' and '.pdf' from the filename
            
            lead_info = {
                'Email': email_match.group(1) if email_match else 'Not found',
                'Phone': phone_match.group(1).strip() if phone_match else 'Not found',
                'Deal Name': deal_name,
                'Pipeline': DEAL_PIPELINE,
                'Deal Stage': DEAL_STAGE,
                'Lead Source': 'procompare.co.za'
            }

            company_info = {
                'Company Name': company_name,
                'Deal Name': deal_name
            }
            
            # Append the lead info to the leads_data list and company info to companies_data
            leads_data.append(lead_info)
            companies_data.append(company_info)

# Convert the lists of leads and companies to DataFrames
leads_df = pd.DataFrame(leads_data)
companies_df = pd.DataFrame(companies_data)

# Get the current date and format it as YYYY-MM-DD
current_date = datetime.now().strftime('%Y-%m-%d')

# Define file names
leads_csv_file_name = f'leads_{current_date}.csv'
companies_csv_file_name = f'companies_{current_date}.csv'

# Define file paths
leads_csv_file_path = os.path.join(output_directory, leads_csv_file_name)
companies_csv_file_path = os.path.join(output_directory, companies_csv_file_name)

# Attempt to save the DataFrames to CSV files
try:
    leads_df.to_csv(leads_csv_file_path, index=False)
    companies_df.to_csv(companies_csv_file_path, index=False)
    print(f"Leads CSV file created at {leads_csv_file_path}")
    print(f"Companies CSV file created at {companies_csv_file_path}")
except PermissionError as e:
    print(f"PermissionError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
