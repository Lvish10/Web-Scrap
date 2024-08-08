from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_job_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('jobs.db')
    query = 'SELECT job_title, sector, company, country, closing_date FROM job_listings'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_sector_counts():
    df = get_job_data()
    sector_counts = df['sector'].value_counts().to_dict()
    return sector_counts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    df = get_job_data()
    return df.to_json(orient='records')

@app.route('/sector-data')
def sector_data():
    sector_counts = get_sector_counts()
    return jsonify(sector_counts)

if __name__ == '__main__':
    app.run(debug=True)
