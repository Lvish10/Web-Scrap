from flask import Flask, render_template, send_from_directory
import pandas as pd
import os

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

@app.route('/plots')
def plots():
    return render_template('plots.html')

@app.route('/plots/<filename>')
def get_plot(filename):
    return send_from_directory('plots', filename)

if __name__ == '__main__':
    app.run(debug=True)
