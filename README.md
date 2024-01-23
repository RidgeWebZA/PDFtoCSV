
# PDF Leads Extraction Tool

This tool is designed to extract lead information from PDF files and compile it into a CSV file.

## Requirements

- Python 3
- Libraries: PyMuPDF, pandas. Install them using `pip install PyMuPDF pandas`.

## Usage

1. Place all your PDF files in a single directory.
2. Ensure that all PDFs have a similar structure for the script to correctly parse the information.
3. Update the `pdf_directory` variable in the script to the path of your PDF files directory.
4. Update the `csv_file_path` variable in the script to the desired output path for the CSV file.
5. Run the script with Python.

## Script Functionality

The script will loop through all PDF files in the specified directory, extract relevant information from each, and save it into a CSV file in the defined output path.

## Output

The output CSV file will contain the following columns:
- Lead Name
- Date
- Email
- Cell or WhatsApp Number
- Category
- Service
- City or Suburb
- Requirement
- Type of Website
- Project Description
- Lead Source

Please ensure that you have the legal right to process the data contained in the PDF files using this tool.
