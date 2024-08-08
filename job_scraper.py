from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

def scrape_jobs():
    # Read the local HTML file
    with open(r"C:\Users\Lavish\.vscode\Web Scrap\Web-Scrap\test.html", "r", encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    jobs = []

    # Find the table with job listings
    table = soup.find('table', class_='job_list')
    if not table:
        print("No job list table found")
        return jobs
    
    rows = table.find_all('tr')[1:]  # Skip the header row
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue  # Skip rows that don't have enough columns
        
        job_title = cols[1].text.strip()
        sector = cols[2].text.strip()
        company = cols[3].text.strip()
        country = cols[4].text.strip()
        closing_date = cols[5].text.strip()
        
        jobs.append({
            'job_title': job_title,
            'sector': sector,
            'company': company,
            'country': country,
            'closing_date': closing_date
        })

    return jobs

def save_to_csv(jobs, filename='jobs.csv'):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)

def save_to_db(jobs, db_name='jobs.db'):
    df = pd.DataFrame(jobs)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        sector TEXT,
        company TEXT,
        country TEXT,
        closing_date TEXT
    )
    ''')
    
    # Insert data into the table
    for index, row in df.iterrows():
        cursor.execute('''
        INSERT INTO job_listings (job_title, sector, company, country, closing_date)
        VALUES (?, ?, ?, ?, ?)
        ''', (row['job_title'], row['sector'], row['company'], row['country'], row['closing_date']))
    
    conn.commit()
    conn.close()

def main():
    jobs = scrape_jobs()
    
    if jobs:
        csv_path = r"C:\Users\Lavish\.vscode\Web Scrap\Web-Scrap\jobs.csv"
        db_path = r"C:\Users\Lavish\.vscode\Web Scrap\Web-Scrap\jobs.db"
        
        # Save data to CSV and database
        save_to_csv(jobs, csv_path)
        save_to_db(jobs, db_path)
    else:
        print("No jobs found.")

if __name__ == "__main__":
    main()
