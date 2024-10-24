import schedule
import time
import threading
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import os
import sys
from datetime import datetime

def scrape_jobs(partial=False):
    # Path to Microsoft Edge WebDriver executable
    edge_driver_path = r'C:\Users\Lavish\Downloads\edgedriver_win64\msedgedriver.exe'  # Update this path

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

                # Check if any column has non-empty data before appending
                if any(col.text.strip() for col in cols):
                    job_number = cols[0].text.strip() if len(cols) > 0 else "N/A"
                    job_title = cols[1].text.strip() if len(cols) > 1 else "N/A"
                    economic_sector = cols[2].text.strip() if len(cols) > 2 else "N/A"
                    company = cols[3].text.strip() if len(cols) > 3 else "N/A"
                    country = cols[4].text.strip() if len(cols) > 4 else "N/A"
                    closing_date = cols[5].text.strip() if len(cols) > 5 else "N/A"

                    jobs_data.append({
                        'Job Number': job_number,
                        'Title': job_title,
                        'Economic Sector': economic_sector,
                        'Company': company,
                        'Country': country,
                        'Closing Date': closing_date
                    })

                if partial and len(jobs_data) >= 10:  # If partial scrape is requested, stop after 10 jobs
                    break

            if partial and len(jobs_data) >= 10:
                break

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

            # Remove any rows where all columns are NaN or empty strings
            df.replace('', pd.NA, inplace=True)
            df.dropna(how='all', inplace=True)

            # Save to CSV and Excel
            # Construct file paths
            csv_file_path = os.path.join(script_dir, 'construction_jobs.csv')
            excel_file_path = os.path.join(script_dir, 'construction_jobs.xlsx')

            df.to_csv(csv_file_path, index=False)
            df.to_excel(excel_file_path, index=False)

            print("Scraping complete. Data saved to 'construction_jobs.csv' and 'construction_jobs.xlsx'")

            # Log the time of scraping
            log_file_path = os.path.join(script_dir, 'scrape_log.csv')
            log_data = {'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]}
            log_df = pd.DataFrame(log_data)

            if not os.path.exists(log_file_path):
                log_df.to_csv(log_file_path, index=False)
            else:
                log_df.to_csv(log_file_path, mode='a', header=False, index=False)

            print("Scraping time logged.")

        else:
            print("No job data to save.")

        # Quit the driver
        driver.quit()

def job_schedule(time_str=None, interval=None):
    def job():
        print("Starting scheduled job scrape...")
        scrape_jobs()
        print("Scheduled job scrape completed.")
    
    if interval:
        schedule.every(interval).minutes.do(job)
    elif time_str:
        schedule.every().day.at(time_str).do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(10)  # Wait between checks

def start_admin():
    while True:
        print("\nAdministrative Menu:")
        print("1. Start Scraping Immediately")
        print("2. Schedule Scraping Daily")
        print("3. Schedule Scraping Every 5 Minutes")
        print("4. Exit Program")
        
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            print("Starting immediate job scrape...")
            scrape_jobs()
            print("Immediate job scrape completed.")
        
        elif choice == '2':
            time_str = input("Enter the time to schedule scraping (HH:MM, 24-hour format): ")
            print(f"Scraping scheduled at {time_str} every day.")
            threading.Thread(target=job_schedule, args=(time_str,)).start()
        
        elif choice == '3':
            print("Scraping scheduled every 5 minutes.")
            threading.Thread(target=job_schedule, args=(None, 5)).start()
        
        elif choice == '4':
            print("Exiting program...")
            sys.exit()
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    start_admin()
