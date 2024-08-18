import schedule
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import os

def scrape_jobs():
    # Path to Microsoft Edge WebDriver executable
    edge_driver_path = r'C:\Users\user\Downloads\edgedriver_win64\msedgedriver.exe'  # Update this path

    # Set up Selenium WebDriver with Edge
    options = Options()
    options.headless = False  # Set to True if you don't want to see the browser
    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service, options=options)

    try:
        # Open Mauritius Jobs page
        driver.get('https://mauritiusjobs.govmu.org/jobsearch')

        # Debug: Print page title to ensure correct page is loaded
        print("Page title:", driver.title)

        # Wait for the dropdown to be available
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'sector'))
        )

        # Select "Construction" from the dropdown
        sector_dropdown = Select(driver.find_element(By.ID, 'sector'))
        sector_dropdown.select_by_visible_text('Construction')
        time.sleep(2)  # Delay to ensure dropdown selection is applied

        # Click the search button to perform the search
        try:
            search_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Search"]')
            search_button.click()
            time.sleep(5)  # Delay to ensure the search results load
        except Exception as e:
            print("Search button not found or error:", e)
            driver.quit()
            return

        # Wait for the job list to load
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.job_list'))  # Adjust based on actual HTML structure
            )
        except Exception as e:
            print("Job list not found or error:", e)
            driver.quit()
            return

        jobs_data = []

        while True:
            print("Processing page...")  # Debug print

            # Extract job table
            job_table = driver.find_element(By.CSS_SELECTOR, '.job_list')
            rows = job_table.find_elements(By.TAG_NAME, 'tr')

            # Skip the header row
            for row in rows[1:]:
                cols = row.find_elements(By.TAG_NAME, 'td')
                if len(cols) < 6:  # Ensure the row has enough columns
                    continue
                
                job_number = cols[0].text.strip() if cols[0] else "N/A"
                job_title = cols[1].text.strip() if cols[1] else "N/A"
                economic_sector = cols[2].text.strip() if cols[2] else "N/A"
                company = cols[3].text.strip() if cols[3] else "N/A"
                country = cols[4].text.strip() if cols[4] else "N/A"
                closing_date = cols[5].text.strip() if cols[5] else "N/A"

                jobs_data.append({
                    'Job Number': job_number,
                    'Title': job_title,
                    'Economic Sector': economic_sector,
                    'Company': company,
                    'Country': country,
                    'Closing Date': closing_date
                })

            # Find and click the "Next" button
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, '.pagination-next')  # Update based on actual HTML structure
                next_button.click()
                time.sleep(3)  # Delay to ensure the next page loads
                
            except Exception as e:
                print("No more pages or error:", e)
                break

    finally:
        # Determine the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if 'jobs_data' in locals() and jobs_data:
            # Create DataFrame
            df = pd.DataFrame(jobs_data)

            # Save to CSV and Excel
            # Construct file paths
            csv_file_path = os.path.join(script_dir, 'construction_jobs.csv')
            excel_file_path = os.path.join(script_dir, 'construction_jobs.xlsx')

            print("Scraping complete. Data saved to 'construction_jobs.csv' and 'construction_jobs.xlsx'")
        else:
            print("No job data to save.")

        # Quit the driver
        driver.quit()

def job_schedule():
    print("Starting job scrape...")
    scrape_jobs()
    print("Job scrape completed.")

# Schedule the job to run at a specific time
schedule.every().day.at("23:33").do(job_schedule)  # Set to your desired time

print("Scheduler started. Waiting to run at the specified time...")

while True:
    schedule.run_pending()
    time.sleep(10)  # Wait a minute between checks
