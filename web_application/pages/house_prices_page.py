from dash import dcc, html, Input, Output
from dash import dash_table
from web_application.query.house_prices_queries import get_house_prices_data
from web_application.query.connection import run_query

# Load dropdown options from the database
def load_local_authorities():
    df = run_query("SELECT DISTINCT local_authority_name FROM local_authority ORDER BY local_authority_name")
    return [{'label': name, 'value': name} for name in df['local_authority_name'].tolist()]

# Load wards with their corresponding local authorities for the dropdown
def load_wards():
    df = run_query(
        "SELECT w.ward_name, l.local_authority_name FROM ward w "
        "JOIN local_authority l ON w.local_authority_code = l.local_authority_code "
        "ORDER BY l.local_authority_name, w.ward_name"
    )
    return df

# Load distinct periods for the quarter/period dropdown
def load_periods():
    df = run_query("SELECT DISTINCT period FROM house_price ORDER BY period")
    return [row['period'] for _, row in df.iterrows()]

# Pre-load dropdown options
local_authority_options = load_local_authorities()
ward_df = load_wards()
period_options = load_periods()

# Define styles for the table and its cells
TABLE_STYLE = {
    'overflowX': 'auto',
    'minWidth': '100%',
}
TABLE_STYLE_CELL = {
    'textAlign': 'left',
    'padding': '12px',
    'whiteSpace': 'normal',
    'height': 'auto',
    'fontFamily': 'Segoe UI, Arial, sans-serif',
    'fontSize': '14px',
    'color': '#34495e',
    'border': '1px solid #e3e6ea',
}
TABLE_STYLE_HEADER = {
    'backgroundColor': '#f5f7fb',
    'fontWeight': '700',
    'border': '1px solid #e3e6ea',
    'borderBottom': '2px solid #e3e6ea',
    'fontFamily': 'Segoe UI, Arial, sans-serif',
    'fontSize': '14px',
    'color': '#1f2a44',
}

# Define the layout of the house prices page with filters and a table to display results
def get_layout():
    section_style = {
        'backgroundColor': '#ffffff',
        'border': '1px solid #e3e6ea',
        'borderRadius': '14px',
        'padding': '1.5rem',
        'boxShadow': '0 8px 20px rgba(0, 0, 0, 0.04)',
        'marginBottom': '1.5rem',
    }
    filter_row = {
        'display': 'flex',
        'flexWrap': 'wrap',
        'alignItems': 'flex-end',
        'gap': '1rem',
        'overflowX': 'auto',
        'paddingBottom': '0.5rem',
    }
    field_style = {
        'flex': '0 0 auto',
        'width': '240px',
        'minWidth': '180px',
        'maxWidth': '260px',
        'display': 'flex',
        'flexDirection': 'column',
    }

    return html.Div([
        html.Div([
            html.H4('Average Price and Percentage Change', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            html.Div([
                html.Div([
                    html.Label('Ward', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='house-ward',
                        options=[{'label': row['ward_name'], 'value': row['ward_name']} for _, row in ward_df.iterrows()],
                        value=ward_df['ward_name'].iloc[0] if not ward_df.empty else None,
                        clearable=False,
                        style={'width': '100%'},
                    ),
                ], style=field_style),
                html.Div([
                    html.Label('Start Year', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='house-start-year',
                        options=[{'label': str(year), 'value': str(year)} for year in range(2013, 2024)],
                        value='2013',
                        clearable=False,
                        style={'width': '100%'},
                    ),
                ], style=field_style),
                html.Div([
                    html.Label('End Year', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='house-end-year',
                        options=[{'label': str(year), 'value': str(year)} for year in range(2013, 2024)],
                        value='2023',
                        clearable=False,
                        style={'width': '100%'},
                    ),
                ], style=field_style),
            ], style=filter_row),
            dash_table.DataTable(
                id='house-price-table',
                page_size=10,
                style_table=TABLE_STYLE,
                style_cell=TABLE_STYLE_CELL,
                style_header=TABLE_STYLE_HEADER,
                style_as_list_view=False,
            ),
        ], style=section_style),
        html.Div([
            html.H4('Lowest House Price', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            html.Div([
                html.Div([
                    html.Label('Local Authority', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='house-local-authority',
                        options=local_authority_options,
                        value=local_authority_options[0]['value'] if local_authority_options else None,
                        clearable=False,
                        style={'minWidth': '0'},
                    ),
                ], style=field_style),
                html.Div([
                    html.Label('Quarter / Period', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='house-quarter',
                        options=[{'label': period, 'value': period} for period in period_options],
                        value=period_options[-1] if period_options else None,
                        clearable=False,
                        style={'width': '100%'},
                    ),
                ], style={**field_style, 'flex': '1 1 32%'}),
            ], style={**filter_row, 'marginBottom': '1rem', 'gap': '2%'}),
            html.P(id='house-lowest-price', style={'margin': '0', 'fontSize': '1rem', 'fontWeight': '600', 'color': '#34495e'}),
        ], style=section_style),
    ], style={'fontFamily': 'Arial, sans-serif', 'color': '#23374d'})

# Define callbacks to update the table and lowest price text based on user selections
def register_callbacks(app):
    @app.callback(
        Output('house-price-table', 'data'),
        Output('house-price-table', 'columns'),
        Output('house-lowest-price', 'children'),
        Input('house-local-authority', 'value'),
        Input('house-ward', 'value'),
        Input('house-start-year', 'value'),
        Input('house-end-year', 'value'),
        Input('house-quarter', 'value'),
    )
    def update_house_prices(local_authority, ward, start_year, end_year, quarter):
        # Fetch data based on user selections and format it for display in the table and lowest price text
        average_prices, price_changes, lowest_price = get_house_prices_data(
            local_authority, ward, start_year, end_year, quarter
        )

        # Format average prices and percentage changes to 2 decimal places for better readability in the table
        average_prices = average_prices.copy()  
        average_prices['average_price'] = average_prices['average_price'].astype(float).map('{:.2f}'.format)
        price_changes = price_changes.copy()
        price_changes['pct_change'] = price_changes['pct_change'].astype(float).map('{:.2f}'.format)

        # Merge average prices with percentage changes to create a combined dataset for the table
        merged = average_prices.merge(
            price_changes[['ward_name', 'pct_change']],
            on='ward_name',
            how='left'
        )

        # Convert the merged DataFrame to a list of dictionaries for the DataTable and define the columns to display
        merged_data = merged.to_dict('records')
        merged_columns = [
            {'name': 'Ward', 'id': 'ward_name'},
            {'name': 'Average Price (£)', 'id': 'average_price'},
            {'name': 'Percentage Change (%)', 'id': 'pct_change'},
        ]

        # Format the lowest price information to display
        lowest_price_text = 'No lowest price found.'
        if not lowest_price.empty:
            lowest_price_text = (
                f"Lowest price for {local_authority} on {quarter}: "
                f"{lowest_price.iloc[0]['ward_name']} (£{lowest_price.iloc[0]['median_price']:.2f})"
            )

        return merged_data, merged_columns, lowest_price_text
