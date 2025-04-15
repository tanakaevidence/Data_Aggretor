import requests  # Use requests to talk to websites and get data
from bs4 import BeautifulSoup  # BeautifulSoup helps read and extract useful info from HTML
import pandas as pd  # pandas helps work with data in tables (CSV/Excel)
from datetime import datetime  # To work with date and time
import time  # To add delays in between requests

# Function to scrape job listings from the website
def scrape_jobs():
    base_url = "https://vacancymail.co.zw/jobs/"  # Base URL of the jobs page
    headers = {'User-Agent': 'Mozilla/5.0'}  # Pretend to be a browser
    jobs = []  # List to store job data

    # Loop through first 10 pages
    for page in range(1, 11):
        try:
            # Make a request to the page and get the HTML
            response = requests.get(f"{base_url}?page={page}", headers=headers, timeout=10)
            response.raise_for_status()  # Raise error if response is not successful
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content

            # Find all job listings on the page
            for job in soup.find_all('div', class_='job-listing-description'):
                try:
                    # Extract job details
                    jobs.append({
                        "Title": job.find('h3', class_='job-listing-title').get_text(strip=True),
                        "Company": job.find('h4', class_='job-listing-company').get_text(strip=True),
                        "Location": job.find('span', class_='job-location').get_text(strip=True) if job.find('span', class_='job-location') else 'N/A',
                        "Description": job.find('p', class_='job-listing-text').get_text(strip=True),
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Expiry Date": job.find('span', class_='job-expiry-date').get_text(strip=True) if job.find('span', class_='job-expiry-date') else 'N/A',
                    })
                except AttributeError:
                    continue  # Skip jobs missing any details

            time.sleep(1)  # Be polite and wait for 1 second between requests

        except requests.RequestException:
            break  # Stop if there are any connection issues

    # If jobs are found, save to CSV and Excel
    if jobs:
        df = pd.DataFrame(jobs).drop_duplicates()  # Remove duplicates
        df.to_csv("scraped_data.csv", index=False)  # Save to CSV
        df.to_excel("scraped_data.xlsx", index=False)  # Save to Excel
        print(f"Saved {len(df)} jobs to CSV and Excel")
    else:
        print("No jobs found")  # If no jobs were found

# Only run this script if it is executed directly (not imported in another script)
if __name__ == "__main__":
    scrape_jobs()