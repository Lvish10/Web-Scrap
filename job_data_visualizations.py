import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from squarify import plot as squarify_plot

# Load data from CSV file
data = pd.read_csv(r'C:\Users\user\.vscode\Assignmnt\Web Scraping\Web-Scrap\construction_jobs.csv')

# Handle potential NaN values in Title and Country columns
data = data.dropna(subset=['Title', 'Company', 'Country'])

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Create a directory to save the plots within the script's directory
plot_dir = os.path.join(script_dir, 'plots')
os.makedirs(plot_dir, exist_ok=True)

# Set Seaborn style for aesthetics
sns.set(style="whitegrid")

# Plot 1: Job Titles Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=data, y='Title', order=data['Title'].value_counts().index, palette='viridis')
plt.title('Job Titles Distribution')
plt.xlabel('Number of Jobs')
plt.ylabel('Job Title')
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, 'job_titles_distribution.png'))
plt.close()

# Plot 2: Company Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=data, y='Company', order=data['Company'].value_counts().index, palette='coolwarm')
plt.title('Company Distribution')
plt.xlabel('Number of Jobs')
plt.ylabel('Company')
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, 'company_distribution.png'))
plt.close()

# Plot 3: Job Locations Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=data, y='Country', order=data['Country'].value_counts().index, palette='magma')
plt.title('Job Locations Distribution')
plt.xlabel('Number of Jobs')
plt.ylabel('Country')
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, 'job_locations_distribution.png'))
plt.close()

# Plot 4: Closing Date Frequency
data['Closing Date'] = pd.to_datetime(data['Closing Date'], format='%d/%m/%Y', errors='coerce')
data['Closing Date'] = data['Closing Date'].dt.to_period('M')  # Convert to monthly frequency
closing_date_counts = data['Closing Date'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
closing_date_counts.plot(kind='bar', color='teal')
plt.title('Job Posting Closing Dates Frequency')
plt.xlabel('Month')
plt.ylabel('Number of Jobs')
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, 'closing_date_frequency.png'))
plt.close()

# Plot 5: Heatmap of Job Counts by Company and Location
job_counts = pd.crosstab(data['Company'], data['Country'])
plt.figure(figsize=(12, 8))
sns.heatmap(job_counts, cmap='Blues', annot=True, fmt='d', linewidths=.5)
plt.title('Job Counts Heatmap by Company and Location')
plt.xlabel('Country')
plt.ylabel('Company')
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, 'heatmap_job_counts.png'))
plt.close()

# Plot 6: Job Title Length Distribution
data['Title'] = data['Title'].astype(str)
data['Title Length'] = data['Title'].apply(lambda x: len(x) if x != 'nan' else 0)

plt.figure(figsize=(10, 6))
sns.histplot(data['Title Length'], kde=True, color='orange')
plt.title('Job Title Length Distribution')
plt.xlabel('Title Length')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, 'title_length_distribution.png'))
plt.close()

# Plot 7: Donut Chart for Job Distribution by Country
plt.figure(figsize=(8, 8))
country_counts = data['Country'].value_counts()
plt.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'), startangle=140, wedgeprops=dict(width=0.4))
plt.title('Job Distribution by Country')
plt.savefig(os.path.join(plot_dir, 'donut_chart_job_distribution_by_country.png'))
plt.close()

# Plot 8: Box Plot for Closing Dates by Economic Sector
# Convert 'Closing Date' to a numeric format for boxplot
data['Closing Date Numeric'] = pd.to_numeric(data['Closing Date'].astype(int), errors='coerce')

plt.figure(figsize=(12, 8))
sns.boxplot(data=data, x='Economic Sector', y='Closing Date Numeric', palette='muted', hue='Economic Sector', legend=False)
plt.title('Closing Dates by Economic Sector')
plt.xlabel('Economic Sector')
plt.ylabel('Closing Date')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, 'box_plot_closing_dates_by_sector.png'))
plt.close()

# Plot 9: FacetGrid for Job Distribution by Company and Country
g = sns.FacetGrid(data, col='Company', col_wrap=4, height=5, aspect=1.5)
g.map(sns.countplot, 'Country', palette='husl')
g.set_titles(col_template="{col_name}")
g.set_axis_labels('Country', 'Number of Jobs')
g.tight_layout()
g.savefig(os.path.join(plot_dir, 'facet_grid_job_distribution_by_company.png'))
plt.close()

# Plot 10: Violin Plot for Job Titles Length by Economic Sector
plt.figure(figsize=(12, 8))
sns.violinplot(data=data, x='Economic Sector', y='Title Length', palette='viridis')
plt.title('Job Title Length by Economic Sector')
plt.xlabel('Economic Sector')
plt.ylabel('Title Length')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, 'violin_plot_title_length_by_sector.png'))
plt.close()

# Plot 11: Scatter Plot with Regression Line
plt.figure(figsize=(10, 6))
sns.regplot(data=data, x='Title Length', y='Closing Date Numeric', scatter_kws={'s':50}, line_kws={'color':'red'})
plt.title('Job Title Length vs. Closing Date')
plt.xlabel('Title Length')
plt.ylabel('Closing Date')
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, 'scatter_plot_title_length_vs_closing_date.png'))
plt.close()

# Plot 12: Treemap for Job Counts by Economic Sector
plt.figure(figsize=(10, 8))
sizes = data['Economic Sector'].value_counts()
labels = sizes.index
plot_data = pd.DataFrame({'labels': labels, 'sizes': sizes})
squarify_plot(sizes, label=labels, alpha=0.8, color=sns.color_palette('husl', len(labels)))
plt.title('Job Counts by Economic Sector')
plt.axis('off')
plt.savefig(os.path.join(plot_dir, 'treemap_job_counts_by_sector.png'))
plt.close()

# Plot 13: Pair Grid to Explore Relationships Between Multiple Variables
plt.figure(figsize=(12, 10))
g = sns.PairGrid(data[['Title Length', 'Closing Date Numeric', 'Economic Sector']].dropna(), hue='Economic Sector', palette='Set2')
g.map_lower(sns.scatterplot)
g.map_diag(sns.histplot)
g.add_legend()
g.savefig(os.path.join(plot_dir, 'pair_grid_relationships.png'))
plt.close()
