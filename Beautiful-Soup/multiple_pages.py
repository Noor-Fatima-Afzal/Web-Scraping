import requests
from bs4 import BeautifulSoup 
import pandas as pd
import re

url = 'https://www.linkedin.com/jobs/lahore-jobs/?currentJobId=3949138887'
r = requests.get(url)
print(r)

soup = BeautifulSoup(r.text, 'lxml')
job_title_element = soup.find('a', class_='job-card-container__link job-card-list__title job-card-list__title--link')
if job_title_element:
        # Extract the job title text
        job_title = job_title_element.get_text(strip=True)
        print(job_title)
else:
    print("Job title element not found.")

# titles  = soup.find_all('a', class_ = 'disabled ember-view job-card-container__link job-card-list__title job-card-list__title--link')