import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

listt = ["TRENT",
"TATACONSUM",
"TITAN",
"BEL",
"LT",
"HEROMOTOCO",
"INDUSINDBK",
"NESTLEIND",
"ADANIPORTS",
"TATASTEEL",
"SHRIRAMFIN",
"DRREDDY",
"POWERGRID",
"ADANIENT",
"MARUTI",
"M&M",
"INFY",
"BPCL",
"BAJAJ-AUTO",
"HINDUNILVR",
"ITC",
"COALINDIA",
"TATAMOTORS",
"WIPRO",
"ONGC",
"SBIN",
"HINDALCO",
"BRITANNIA",
"NTPC",
"ASIANPAINT",
"SUNPHARMA",
"TECHM",
"EICHERMOT",
"HDFCLIFE",
"RELIANCE",
"HCLTECH",
"GRASIM",
"SBILIFE",
"APOLLOHOSP",
"HDFCBANK",
"CIPLA",
"ULTRACEMCO",
"AXISBANK",
"JSWSTEEL",
"BAJFINANCE",
"TCS",
"KOTAKBANK",
"BAJAJFINSV",
"ITCHOTELS",
"ICICIBANK",
"BHARTIARTL"
]  # Company symbols

def create_csv():  # Function to download CSV from the balance sheet data

    # Sending a GET request to fetch the page content
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parsing the page content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finding the balance sheet table
    balance_sheet_section = soup.find('section', {'id': 'balance-sheet'})
    if not balance_sheet_section:
        raise ValueError(f'Balance sheet section not found for {i}')

    # Extracting headers (for years)
    headers = [header.text.strip() for header in balance_sheet_section.find_all('th')]

    # Debugging: Print the extracted headers to see their actual content
    print(f"Extracted headers for {i}:", headers)

    # Check for variations of "Sep 24" in the headers
    sep_24_column = None
    for header in headers:
        if 'Sep 24' in header or '2024' in header:  # Adjust as per the actual format
            sep_24_column = header
            break

    if not sep_24_column:
        raise ValueError(f'Sep 24 column not found in the balance sheet for {i}')

    # Find the index of the "Sep 24" column
    sep_24_index = headers.index(sep_24_column)

    # Extracting rows and filtering only "Sep 24" data
    rows = []
    for row in balance_sheet_section.find_all('tr'):
        cols = [col.text.strip() for col in row.find_all('td')]
        if cols:
            # Only extract the relevant data for the "Sep 24" column
            rows.append([cols[0], cols[sep_24_index]])  # Assuming first column is the row label (e.g., "Assets")

    # Creating a DataFrame
    balance_sheet_df = pd.DataFrame(rows, columns=["Description", "Sep 24"])
    
    # Transpose the DataFrame so that 'Description' becomes the index
    transposed_df = balance_sheet_df.set_index("Description").T
    
    # Add the company name as a new column header
    transposed_df['Company'] = i
    
    return transposed_df

# List to hold the balance sheet data for all companies
all_data = []

for i in listt:
    url = 'https://www.screener.in/company/' + i + '/consolidated/'
    try:
        company_df = create_csv()
        all_data.append(company_df)
        print(f"Downloaded balance sheet for {i}")
    except Exception as e:
        print(f"Error for {i}: {e}")
    time.sleep(1)

# Concatenate all company data horizontally (axis=1)
combined_df = pd.concat(all_data, axis=0)

# Saving the combined data to a single CSV file in horizontal format
combined_df.to_csv("combined_balance_sheet_sep24_horizontal.csv", index=False)

print("Combined balance sheet data saved to combined_balance_sheet_sep24_horizontal.csv")