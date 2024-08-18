---

# Job Data Visualization Project

## Overview

This project involves scraping job listings from a website, processing the data, and visualizing it through various plots. The solution includes a web scraping script, a data visualization script, and a web application to display the visualizations. The primary focus of this project is web scraping and data visualization.

## Project Structure

- `scrape_jobs_selenium.py`: This script uses Selenium to scrape job listings from a website. It selects jobs based on a specific sector, extracts relevant information, and saves it to both CSV and Excel formats.
- `job_data_visualizations.py`: This script processes the scraped job data and generates various visualizations such as distributions, heatmaps, and treemaps, saving them as PNG files.
- `app.py`: This is the Flask application that serves the web pages for displaying job data and visualizations.
- `construction_jobs.csv`: The CSV file containing the scraped job data.
- `construction_jobs.xlsx`: The Excel file containing the scraped job data.
- `/plots`: Directory containing the PNG files of the visualizations.
- `/static`: Directory for static files, including `scripts.js` and `styles.css`.
- `/templates`: Directory for HTML templates, including `index.html` and `plots.html`.

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the Required Packages**

   Create a `requirements.txt` file with the following content:

   ```plaintext
   selenium
   pandas
   matplotlib
   seaborn
   squarify
   Flask
   ```

   Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download WebDriver**

   - Download the appropriate WebDriver for your browser (e.g., Microsoft Edge WebDriver).
   - Update the path to the WebDriver in `scrape_jobs_selenium.py`.

## Usage

1. **Run the Web Scraper**

   ```bash
   python scrape_jobs_selenium.py
   ```

   This script will scrape job data and save it to `construction_jobs.csv` and `construction_jobs.xlsx`.

2. **Generate Visualizations**

   ```bash
   python job_data_visualizations.py
   ```

   This script will create various plots and save them in the `/plots` directory.

3. **Run the Web Application**

   ```bash
   python app.py
   ```

   Open a web browser and navigate to `http://127.0.0.1:5000/` to view the job listings and visualizations.

## File Structure

- `scrape_jobs_selenium.py` - Web scraping script using Selenium.
- `job_data_visualizations.py` - Script for generating visualizations.
- `app.py` - Flask application to display visualizations.
- `construction_jobs.csv` - Scraped job data in CSV format.
- `construction_jobs.xlsx` - Scraped job data in Excel format.
- `/plots` - Directory containing visualization PNG files.
- `/static` - Directory containing static files (`scripts.js` and `styles.css`).
- `/templates` - Directory containing HTML templates (`index.html` and `plots.html`).

## Notes

- Ensure that the WebDriver path in `scrape_jobs_selenium.py` is correctly set according to your environment.
- Adjust the plot styles and visualization settings as needed for better presentation.

## Acknowledgements

- Done by Lavish

---
