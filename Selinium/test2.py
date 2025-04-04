from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up Chrome options
options = Options()
options.headless = False  # Set to False for debugging

# Initialize the webdriver
driver = webdriver.Chrome(service=Service(r"C:\drivers\chromedriver-win64\chromedriver.exe"), options=options)

# Open the target URL
url = 'https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch/theoritical-market-watch-today?locale=en'
driver.get(url)

# Wait for the table to load
wait = WebDriverWait(driver, 10)
header_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dataTables_scrollHead')))
table_body_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dataTables_scrollBody')))

# Extract the headers
header_cells = header_div.find_elements(By.TAG_NAME, 'th')
headers = [header.text.strip() for header in header_cells]
print(f"Headers: {headers}")

# Extract table rows
rows = table_body_div.find_elements(By.TAG_NAME, 'tr')

# Parse the table data
data = []
current_sector = None  # Track the current sector name
for i, row in enumerate(rows):
    # Check if the row is a sector header with <th> tags
    sector_header = row.find_elements(By.TAG_NAME, 'th')
    if sector_header:
        # Update the current sector name
        current_sector = sector_header[0].text.strip()
        print(f"Sector Found: {current_sector}")
        continue  # Move to the next row after recording the sector name

    # Check for data rows with <td> tags
    cells = row.find_elements(By.TAG_NAME, 'td')
    if cells:  # Skip rows without data
        row_data = [cell.text.strip() for cell in cells]
        row_data.insert(0, current_sector)  # Add the current sector name to the row
        data.append(row_data)
        print(f"Row {i + 1} Data: {row_data}")

# Add "Sector" as the first column in the headers
headers.insert(0, "Sector")

# Convert the collected data to a pandas DataFrame
df = pd.DataFrame(data, columns=headers)

# Save the data to a CSV file
df.to_csv('saudi_exchange_table_with_multiple_sectors.csv', index=False)

# Print the DataFrame for verification
print(df)

# Close the browser
driver.quit()
