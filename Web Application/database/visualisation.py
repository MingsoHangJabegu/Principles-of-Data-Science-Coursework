from connection import run_query
import matplotlib.pyplot as plt
import seaborn as sns

def house_prices_visualisation(oxford_wards, cherwell_wards):
    # Combine the ward lists for the IN clause
    wards = oxford_wards + cherwell_wards
    
    # Create placeholders for the IN clause
    placeholders = ','.join('?' * len(wards))
    
    # Query for question 13
    query = f"""
    SELECT w.ward_name, l.local_authority_name, hp.period, hp.median_price
    FROM house_price hp
    JOIN ward w ON hp.ward_code = w.ward_code
    JOIN local_authority l ON w.local_authority_code = l.local_authority_code
    WHERE w.ward_name IN ({placeholders})
    AND hp.period BETWEEN 'Mar 2013' AND 'Mar 2023'
    """

    # Execute the query with parameters
    data = run_query(query, params=tuple(wards))
    
    # Extract year from period string
    data['year'] = data['period'].str.extract(r'(\d{4})').astype(int)
    
    # Line plot
    fig1, ax1 = plt.subplots(figsize=(14, 7))
    sns.lineplot(data=data, x='year', y='median_price', hue='ward_name', marker='o', ax=ax1)
    ax1.set_title('House Price Trends (2013 - 2023)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Median House Price (£)')
    ax1.grid(True, alpha=0.2)
    ax1.legend(title="Ward", bbox_to_anchor=(1.05, 1), loc='upper left')
    fig1.tight_layout()
    
    # Bar chart - Grouped comparison by first and last year
    first_year = data['year'].min()
    last_year = data['year'].max()
    bar_data = data[data['year'].isin([first_year, last_year])]
    
    fig2, ax2 = plt.subplots(figsize=(14, 6))
    sns.barplot(data=bar_data, x='ward_name', y='median_price', hue='year', ax=ax2, palette=['#3498db', '#e74c3c'])
    ax2.set_title(f'House Price Comparison by Ward ({first_year} vs {last_year})')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    ax2.set_xlabel('Ward')
    ax2.set_ylabel('Median Price (£)')
    ax2.grid(True, alpha=0.2, axis='y')
    ax2.legend(title='Year')
    fig2.tight_layout()

    return fig1, fig2

if __name__ == '__main__':
    oxford_wards = ['Blackbird Leys', 'Carfax', 'Churchill', 'Barton and Sandhills', 'Headington']
    cherwell_wards = ['Banbury Hardwick', 'Bicester East', 'Deddington', 'Kidlington East', 'Launton and Otmoor']
    line_plot, bar_chart = house_prices_visualisation(oxford_wards, cherwell_wards)
    plt.show()