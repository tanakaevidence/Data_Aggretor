import requests#"Hey, I want to use a tool (called requests) that helps me talk to websites and get data from them."

from bs4 import BeautifulSoup#"I want to use a tool that helps me read and pull out useful info from messy web page code (like HTML)."

import pandas as pd#"I want to use pandas, a powerful tool that helps me work with data in tables, like Excel sheets or CSV files."

from datetime import datetime#You're telling Python to import the datetime class from the datetime module.

import time#You're telling Python to load the built-in time module, which gives you access to functions that work with time and delays.


#You're creating a tool called scrape_jobs() that will visit the job site, act like a browser, and prepare a place (jobs = []) to store the job listings it finds.
def scrape_jobs():
    base_url = "https://vacancymail.co.zw/jobs/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    jobs = []
    
#"For each page from 1 to 10, ask the website for the page's content, make sure it worked, and turn the page into a format I can search through easily."
    for page in range(1, 11): 
        try:
            response = requests.get(f"{base_url}?page={page}", headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

 #"For each job post found on the page, collect the title, company, location, description, and today's date, then save it in a list."           
            for job in soup.find_all('div', class_='job-listing-description'):
                try:
                  jobs.append({
    "Title": job.find('h3', class_='job-listing-title').get_text(strip=True),
    "Company": job.find('h4', class_='job-listing-company').get_text(strip=True),
    "Location": job.find('span', class_='job-location').get_text(strip=True) if job.find('span', class_='job-location') else 'N/A',
    "Description": job.find('p', class_='job-listing-text').get_text(strip=True),
    "Date": datetime.now().strftime("%Y-%m-%d"),
    "Expiry Date": job.find('span', class_='job-expiry-date').get_text(strip=True) if job.find('span', class_='job-expiry-date') else 'N/A',
})


#"If a job post is missing some info, skip it. After each page, wait 1 second to be polite. If the site has any connection issue, stop scraping."
                except AttributeError:
                    continue
            
            time.sleep(1)  
            
        except requests.RequestException:
            break

#"If we found any jobs, save them to CSV and Excel files with the current date/time in the name. If we didn’t find any, let the user know."
    if jobs:
        df = pd.DataFrame(jobs).drop_duplicates()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        df.to_csv(f"jobs_{timestamp}.csv", index=False)
        df.to_excel(f"jobs_{timestamp}.xlsx", index=False)
        print(f"Saved {len(df)} jobs to CSV and Excel")
    else:
        print("No jobs found")


#"Only run the scrape_jobs() function if this file is being run directly, not if it's being imported into another file."
if __name__ == "__main__":
    scrape_jobs()

         