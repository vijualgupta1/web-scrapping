import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

listt = ["INFY"
]

def create_csv():# downlaod csv from link


    # Sending a GET request to fetch the page content
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parsing the page content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finding the balance sheet table
    # Adjust the selector based on the actual HTML structure of the page
    balance_sheet_section = soup.find('section', {'id': 'balance-sheet'})
    if not balance_sheet_section:
        raise ValueError('Balance sheet section not found on the page')

    # Extracting headers
    headers = [header.text.strip() for header in balance_sheet_section.find_all('th')]

    # Extracting rows
    rows = []
    for row in balance_sheet_section.find_all('tr'):
        cols = [col.text.strip() for col in row.find_all('td')]
        if cols:
            rows.append(cols)

    # Creating a DataFrame and saving it to a CSV file
    balance_sheet_df = pd.DataFrame(rows, columns=headers)
    balance_sheet_df.to_csv(i+".csv", index=False)

    


for i in listt:
    url = 'https://www.screener.in/company/'+i+'/consolidated/'
    create_csv()
    print(i)
    time.sleep(1)