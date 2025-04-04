from datetime import date
import json
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome options
options = Options()
options.add_argument("--start-maximized")  # Example: Start browser maximized

# Path to your ChromeDriver executable
driver_path = r'C:\drivers\chromedriver-win64\chromedriver.exe'

# Initialize WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.saudiexchange.sa/wps/portal/tadawul/markets/equities/indices/today/!ut/p/z1/rZJdT8IwFIZ_ixe9lJ7BBPWuMWHWTCKR4ezNUroqM_1YusLw31u4M9GigXPXnOdJ874tZrjEzPBt8859Yw1X4fzKxtVweHed3KSQQz5JgIwzoPPHdJRNAb_EAMgSzP7lZ3Q2ATIn98vpchH80Wk-pH_z4ZchcNxnUWSWxIFDRd-BHzqIAvuQByCS4uFYjvDQa-_bWwQI-r4fNCs9EFYj2GllOgStszWCmnvuP1uJQFjjpfEInOzsxgl5KaxSUuz_TYeZ5ytqarnD5ZN0b9ZpboQ89yVizZ2vPO-aSmycC2TVhaV1uFyQZ4pbXRRFCQ39uFLbnFx8AZWL71c!/p0/IZ7_NHLCH082KGN530A68FC4AN2O63=CZ6_22C81940L0L710A6G0IQM43GF0=MEtabIndex!ListedCompanies=chart_tasi_current_sector!TASI==/?")

def extract_company_data(driver, index):
    try:
        # Scroll to element
        element = driver.find_element(By.CSS_SELECTOR, f'#table5 > tbody > tr:nth-child({index}) > td:nth-child(2) > a')
        coordinates = element.location_once_scrolled_into_view
        driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))
        element.click()

        time.sleep(3)  # Optional: Use explicit waits instead of sleep

        # Extract data
        company_data = {
            "Reference Number": driver.find_element(By.CSS_SELECTOR, '#index_head > p').text,
            "Company Name": driver.find_element(By.CSS_SELECTOR, '#index_head > div > h2').text,
            "Trading Name": driver.find_element(By.CSS_SELECTOR, '#index_head > div > p:nth-child(2) > strong').text,
            "Sector Name": driver.find_element(By.CSS_SELECTOR, '#index_head > div > p:nth-child(3) > strong').text,
            "Industry Group": driver.find_element(By.CSS_SELECTOR, '#index_head > div > p:nth-child(3) > a').text,
            "Price": driver.find_element(By.XPATH, '//*[@id="chart_tab1"]/div[1]/div[1]/div[1]/dl/dd').text,
            "Change Value": driver.find_element(By.XPATH, '//*[@id="chart_tab1"]/div[1]/div[1]/div[2]/dl/dd').text.split('(')[0],
            "Change Percentage": re.search(r'\((.*?)\)', driver.find_element(By.XPATH, '//*[@id="chart_tab1"]/div[1]/div[1]/div[2]/dl/dd').text).group(1),
            # Add more fields as needed
        }

        # Go back to the main table
        driver.execute_script("window.history.go(-1)")
        return company_data

    except Exception as e:
        print(f"Error extracting data for company index {index}: {e}")
        return None

# Set the number of pages you want to scrape
pages = 5  # Replace with the correct number of pages

data = []
for page in range(1, pages + 1):
    # Wait for the pagination dropdown to be present before interacting with it
    wait = WebDriverWait(driver, 10)
    pagination_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#table5_paginate > select')))
    select = Select(pagination_select)
    select.select_by_value(str(page))
    time.sleep(2)  # Optional: Replace with explicit waits

    rows = len(driver.find_elements(By.CSS_SELECTOR, '#table5 tbody tr'))
    for row in range(1, rows + 1):
        company_data = extract_company_data(driver, row)
        if company_data:
            data.append(company_data)

# Save the data to a JSON file
output_file = f'TASI_Data_{date.today()}.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Data saved to {output_file}")

# Close browser
driver.quit()
