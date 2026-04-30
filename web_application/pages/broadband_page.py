from dash import dcc, html, Input, Output, dash_table
from web_application.query.broadband_queries import get_broadband_data
from web_application.query.connection import run_query

# Load dropdown options from the database
def load_local_authorities():
    df = run_query("SELECT DISTINCT local_authority_name FROM local_authority ORDER BY local_authority_name")
    return [{'label': name, 'value': name} for name in df['local_authority_name'].tolist()]

# Load broadband areas with their corresponding local authority names
def load_broadband_areas():
    df = run_query(
        "SELECT ba.area_name, l.local_authority_name FROM broadband_area ba "
        "JOIN local_authority l ON ba.local_authority_code = l.local_authority_code "
        "ORDER BY l.local_authority_name, ba.area_name"
    )
    return df

# Pre-load dropdown options and data for the page
local_authority_options = load_local_authorities()
broadband_area_df = load_broadband_areas()

# Define styles for the tables and page layout
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
}
TABLE_STYLE_HEADER = {
    'backgroundColor': '#f5f7fb',
    'fontWeight': '700',
    'borderBottom': '2px solid #e3e6ea',
    'fontFamily': 'Segoe UI, Arial, sans-serif',
    'fontSize': '14px',
    'color': '#1f2a44',
}

# Define the layout of the broadband page with filters and tables
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
        'flexWrap': 'nowrap',
        'alignItems': 'flex-end',
        'gap': '1%',
        'overflowX': 'auto',
        'paddingBottom': '0.5rem',
    }
    field_style = {
        'flex': '0 0 auto',
        'width': '280px',
        'minWidth': '200px',
        'maxWidth': '320px',
        'display': 'flex',
        'flexDirection': 'column',
    }

    return html.Div([
        html.Div([
            html.H4('Broadband Stats', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            html.Div([
                html.Div([
                    html.Label('Area Name', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='broadband-area',
                        options=[{'label': row['area_name'], 'value': row['area_name']} for _, row in broadband_area_df.iterrows()],
                        value=broadband_area_df['area_name'].iloc[0] if not broadband_area_df.empty else None,
                        clearable=False,
                        style={'width': '100%'},
                    ),
                ], style=field_style),
            ], style={**filter_row, 'marginBottom': '1rem'}),
            dash_table.DataTable(
                id='broadband-stats-table',
                page_size=10,
                style_table=TABLE_STYLE,
                style_cell=TABLE_STYLE_CELL,
                style_header=TABLE_STYLE_HEADER,
                style_as_list_view=True,
            ),
        ], style=section_style),
        html.Div([
            html.H4('Fastest Areas by Local Authority', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            html.Div([
                html.Div([
                    html.Label('Local Authority', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='broadband-local-authority',
                        options=local_authority_options,
                        value=local_authority_options[0]['value'] if local_authority_options else None,
                        clearable=False,
                        style={'width': '100%'},
                    ),
                ], style=field_style),
            ], style={**filter_row, 'marginBottom': '1rem'}),
            dash_table.DataTable(
                id='broadband-fastest-table',
                page_size=10,
                style_table=TABLE_STYLE,
                style_cell=TABLE_STYLE_CELL,
                style_header=TABLE_STYLE_HEADER,
            ),
        ], style=section_style),
    ], style={'fontFamily': 'Arial, sans-serif', 'color': '#23374d'})

# Define callbacks to update the tables based on the selected filters
def register_callbacks(app):
    @app.callback(
        Output('broadband-stats-table', 'data'),
        Output('broadband-stats-table', 'columns'),
        Output('broadband-fastest-table', 'data'),
        Output('broadband-fastest-table', 'columns'),
        Input('broadband-local-authority', 'value'),
        Input('broadband-area', 'value'),
    )
    def update_broadband(local_authority, area_name):
        # Fetch broadband stats and fastest areas based on the selected local authority and area name
        broadband_stats, broadband_fastest = get_broadband_data(local_authority, area_name)
        broadband_stats = broadband_stats.copy()
        broadband_stats['avg_download_speed_mbps'] = broadband_stats['avg_download_speed_mbps'].astype(float).map('{:.2f}'.format)
        stats_data = broadband_stats.to_dict('records')
        # Define columns for the broadband stats table
        stats_columns = [
            {'name': 'Area Name', 'id': 'area_name'},
            {'name': 'Average Speed (Mbps)', 'id': 'avg_download_speed_mbps'},
            {'name': 'Superfast Availability (%)', 'id': 'superfast_pct'},
        ]
        # Format the fastest areas data and define columns for the table
        broadband_fastest = broadband_fastest.copy()
        broadband_fastest['average_speed_mbps'] = broadband_fastest['average_speed_mbps'].astype(float).map('{:.2f}'.format)
        fastest_data = broadband_fastest.to_dict('records')
        fastest_columns = [
            {'name': 'Area Name', 'id': 'area_name'},
            {'name': 'Average Speed (Mbps)', 'id': 'average_speed_mbps'},
            {'name': 'Superfast Availability (%)', 'id': 'Superfast_Pct'},
            {'name': 'Gigabit Availability (%)', 'id': 'Gigabit_Pct'},
        ]

        return stats_data, stats_columns, fastest_data, fastest_columns
