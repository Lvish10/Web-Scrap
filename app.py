from flask import Flask, render_template, send_from_directory, redirect, url_for, request
import pandas as pd
import os
from threading import Thread
from scrape_jobs_selenium import scrape_jobs, job_schedule  # Import job_schedule

app = Flask(__name__)

@app.route('/')
def home():
    csv_path = r'C:\Users\Lavish\.vscode\Web Scrap\Web-Scrap\construction_jobs.csv'

    if not os.path.isfile(csv_path):
        return render_template('index.html', jobs=None, error='CSV file not found.')

    try:
        data = pd.read_csv(csv_path)
        jobs = data.to_dict(orient='records')
    except Exception as e:
        return render_template('index.html', jobs=None, error=str(e))

    return render_template('index.html', jobs=jobs, error=None)

@app.route('/scrape')
def scrape():
    Thread(target=scrape_jobs).start()
    return redirect(url_for('home'))

@app.route('/schedule_scrape', methods=['POST'])
def schedule_scrape():
    time_str = request.form.get('schedule_time')
    if time_str:
        Thread(target=job_schedule, args=(time_str,)).start()
        return redirect(url_for('home', message="Scraping scheduled at " + time_str))
    return redirect(url_for('home', error="Failed to schedule scraping."))

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
