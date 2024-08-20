from flask import Flask, render_template, send_from_directory, redirect, url_for
import pandas as pd
import os
from threading import Thread  # To run the scrape function in the background

# Import your scrape_jobs function
from scrape_jobs_selenium import scrape_jobs

app = Flask(__name__)

@app.route('/')
def home():
    # Path to the CSV file
    csv_path = r'C:\Users\user\.vscode\Assignmnt\Web Scraping\Web-Scrap\construction_jobs.csv'

    # Check if the CSV file exists
    if not os.path.isfile(csv_path):
        return render_template('index.html', jobs=None, error='CSV file not found.')

    try:
        # Load job data from CSV
        data = pd.read_csv(csv_path)
        jobs = data.to_dict(orient='records')
    except Exception as e:
        return render_template('index.html', jobs=None, error=str(e))

    return render_template('index.html', jobs=jobs, error=None)

@app.route('/scrape')
def scrape():
    # Run the scrape_jobs function in a separate thread so it doesn't block the main thread
    Thread(target=scrape_jobs).start()

    # Redirect back to the home page after starting the scrape
    return redirect(url_for('home'))

@app.route('/plots')
def plots():
    plot_dir = 'Web-Scrap/plots'
    try:
        plot_files = [f for f in os.listdir(plot_dir) if os.path.isfile(os.path.join(plot_dir, f))]
    except Exception as e:
        return render_template('plots.html', plots=None, error=str(e))

    return render_template('plots.html', plots=plot_files)


@app.route('/plots/<filename>')
def get_plot(filename):
    return send_from_directory('plots', filename)

if __name__ == '__main__':
    app.run(debug=True)
