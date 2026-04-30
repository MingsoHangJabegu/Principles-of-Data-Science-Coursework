from .connection import run_query
import plotly.express as px


def house_prices_visualisation(wards, start_year='2013', end_year='2023'):
    if not wards:
        return None, None

    placeholders = ','.join('?' * len(wards))
    query = f"""
    SELECT w.ward_name, l.local_authority_name, hp.period, hp.median_price
    FROM house_price hp
    JOIN ward w ON hp.ward_code = w.ward_code
    JOIN local_authority l ON w.local_authority_code = l.local_authority_code
    WHERE w.ward_name IN ({placeholders})
    AND hp.period BETWEEN 'Mar {start_year}' AND 'Mar {end_year}'
    """

    data = run_query(query, params=tuple(wards))
    if data.empty:
        return None, None

    data['year'] = data['period'].str.extract(r'(\d{4})').astype(int)

    # Combine local authority and ward names for labels in the plots
    data['label'] = data['local_authority_name'] + ' - ' + data['ward_name']

    # Line styles for each local authority
    line_styles = {
        'Cherwell': 'solid',
        'Oxford': 'dash'
    }

    # Add a new column for line style based on local authority
    data['line_style'] = data['local_authority_name'].map(line_styles)

    # Line plot
    fig1 = px.line(
        data,
        x='year',
        y='median_price',
        color='label',
        line_dash='line_style',
        markers=True,
        title=f'House Price Trends ({start_year} - {end_year})',
        labels={'label': 'Local Authority - Ward', 'median_price': 'Median House Price (£)', 'year': 'Year'}
    )
    fig1.update_layout(
        xaxis_title='Year',
        yaxis_title='Median House Price (£)',
        legend_title='Local Authority - Ward'
    )
    for trace in fig1.data:
        label = trace.name.rsplit(',', 1)[0].strip()
        trace.name = label  # Clean up legend label
        trace_data = data[data['label'] == label].sort_values('year')
        trace.customdata = trace_data[['ward_name']].values
        trace.hovertemplate = (
            'Ward: %{customdata[0]}<br>'
            'Median House Price: £%{y:,.0f}<br>'
            'Year: %{x}<extra></extra>'
        )

    # Bar chart comparison
    first_year = data['year'].min()
    last_year = data['year'].max()
    bar_data = data[data['year'].isin([first_year, last_year])].copy()
    bar_data['year'] = bar_data['year'].astype(str)  # For better display

    fig2 = px.bar(
        bar_data,
        x='label',
        y='median_price',
        color='year',
        barmode='group',
        title=f'House Price Comparison by Ward ({first_year} vs {last_year})',
        labels={'label': 'Local Authority - Ward', 'median_price': 'Median House Price (£)', 'year': 'Year'}
    )
    fig2.update_layout(
        height=800,
        xaxis_title='Local Authority - Ward',
        yaxis_title='Median House Price (£)',
        legend_title='Year'
    )
    for trace in fig2.data:
        year_data = bar_data[bar_data['year'] == trace.name].set_index('label')
        year_data = year_data.loc[list(trace.x)].reset_index()
        trace.customdata = year_data[['ward_name', 'median_price', 'year']].values
        trace.hovertemplate = (
            'Ward: %{customdata[0]}<br>'
            'Median House Price: £%{customdata[1]:,.0f}<br>'
            'Year: %{customdata[2]}<extra></extra>'
        )
    fig2.update_xaxes(tickangle=45)

    return fig1, fig2