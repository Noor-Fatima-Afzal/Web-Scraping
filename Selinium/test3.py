from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import pandas as pd

# Set up Chrome options
options = Options()
options.headless = False  # Set to True for headless execution

# Initialize the webdriver
driver = webdriver.Chrome(service=Service(r"C:\drivers\chromedriver-win64\chromedriver.exe"), options=options)

# Open the target URL
base_url = 'https://www.saudiexchange.sa'
url = 'https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch/theoritical-market-watch-today?locale=en'
driver.get(url)

# Wait for the table body to load
wait = WebDriverWait(driver, 40)
try:
    body_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dataTables_scrollBody table tbody")))
    print("Table body found.")
except Exception as e:
    print(f"Error finding table body: {e}")
    driver.quit()
    exit()

# Find all rows (tr) in the tbody
rows = body_table.find_elements(By.TAG_NAME, 'tr')
print(f"Number of rows found: {len(rows)}")

# Parse the table data
data = []
for row in rows:
    try:
        # Find <a> tags with the class 'ellipsis' in each row
        link_element = row.find_element(By.CSS_SELECTOR, "td a.ellipsis")
        company_name = link_element.text.strip()  # Extract company name
        relative_url = link_element.get_attribute('href')  # Extract the href attribute
        absolute_url = urljoin(base_url, relative_url)  # Convert to absolute URL if needed
        data.append([company_name, absolute_url])
    except Exception as e:
        print(f"Error processing row: {e}")

# Check if data is collected
if data:
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data, columns=['Company Name', 'URL'])
    df.to_csv('company_urls.csv', index=False)
    print("Data saved to company_urls.csv")
    print(df)
else:
    print("No data extracted.")

# Close the browser
driver.quit()
