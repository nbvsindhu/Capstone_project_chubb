import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import pyodbc

# Database connection (example using pyodbc)
def fetch_data():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=LAPTOP-977U4L1T\\SQLEXPRESS;"
        "Database=master;"
        "Trusted_Connection=yes;"
    )
    query = """
        SELECT year_desc, age_desc, ethnic_desc, 
               sex_desc, area_desc, count
        FROM capstone_project_target_v1
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Census Data Analysis"

# Fetch data
data = fetch_data()

# Generate unique dropdown options
def generate_dropdown_options(column):
    return [{'label': str(val), 'value': val} for val in sorted(data[column].dropna().unique())]

# Function to generate a bar or pie chart with data labels
def generate_graph(data, group_field, title, chart_type):
    grouped_data = data.groupby(['year_desc', group_field])['count'].sum().reset_index()
    
    if chart_type == 'Bar':
        traces = []
        for category in grouped_data[group_field].unique():
            filtered = grouped_data[grouped_data[group_field] == category]
            traces.append({
                'x': filtered['year_desc'],
                'y': filtered['count'],
                'type': 'bar',
                'name': category,
                'text': filtered['count'],  # Add count to text for data labels
                'textposition': 'outside',  # Position the labels outside the bars
                'hoverinfo': 'x+y+name'  # Show x, y, and name in hover info
            })
        return {
            'data': traces,
            'layout': {
                'title': title,
                'xaxis': {'title': 'Year', 'type': 'category'},
                'yaxis': {'title': 'Count'},
                'barmode': 'stack',
                'template': 'plotly_white',
                'margin': {'t': 100},  # Increased top margin for space above the bars
            }
        }
    
    elif chart_type == 'Pie':
        grouped_data = data.groupby(group_field)['count'].sum().reset_index()
        return {
            'data': [{
                'values': grouped_data['count'],
                'labels': grouped_data[group_field],
                'type': 'pie',
                'hole': 0.4,  # Donut-style pie chart
                'textinfo': 'label+percent+value',  # Display label, percent, and value on the chart
                'insidetextorientation': 'radial',  # Radial text orientation inside pie chart
            }],
            'layout': {
                'title': title,
                'template': 'plotly_white',
                'height': 500,  # Reduced height
                'width': 500    # Reduced width
            }
        }

# Layout
app.layout = html.Div([
    html.H1("Census Data Analysis", style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Dropdown to switch between bar and pie charts for static graphs
    html.Div([
        html.Label("Chart Type:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='static-chart-type',
            options=[
                {'label': 'Bar Chart', 'value': 'Bar'},
                {'label': 'Pie Chart', 'value': 'Pie'}
            ],
            value='Bar',
            clearable=False,
            style={'width': '200px', 'marginBottom': '20px'}
        )
    ], style={'textAlign': 'center'}),

    # Static Graphs Section
    html.Div([
        dcc.Graph(id='static-graph-1', style={'height': '500px'}),  # Increased height
        dcc.Graph(id='static-graph-2', style={'height': '500px'}),  # Increased height
        dcc.Graph(id='static-graph-3', style={'height': '500px'}),  # Increased height
        dcc.Graph(id='static-graph-4', style={'height': '500px'})   # Increased height
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '20px', 'marginBottom': '40px'}),

    # Interactive Graphs Section
    html.Div([
        # Dropdowns (vertical layout)
        html.Div([
            html.Label("Chart Type:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='interactive-chart-type',
                options=[
                    {'label': 'Bar Chart', 'value': 'Bar'},
                    {'label': 'Pie Chart', 'value': 'Pie'}
                ],
                value='Bar',
                clearable=False,
                style={'width': '200px', 'marginBottom': '10px'}
            ),

            html.Label("Select Field:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown-field',
                options=[
                    {'label': 'Year Description', 'value': 'year_desc'},
                    {'label': 'Age Description', 'value': 'age_desc'},
                    {'label': 'Ethnic Description', 'value': 'ethnic_desc'},
                    {'label': 'Sex Description', 'value': 'sex_desc'},
                    {'label': 'Area Description', 'value': 'area_desc'}
                ],
                value='age_desc',
                clearable=False,
                style={'width': '200px', 'marginBottom': '10px'}
            ),

            html.Label("Filter by Year:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown-year',
                options=generate_dropdown_options('year_desc'),
                placeholder="Select Year",
                clearable=True,
                style={'width': '200px', 'marginBottom': '10px'}
            ),

            html.Label("Filter by Sex:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown-sex',
                options=generate_dropdown_options('sex_desc'),
                placeholder="Select Sex",
                clearable=True,
                style={'width': '200px', 'marginBottom': '10px'}
            ),

            html.Label("Filter by Age Description:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown-age',
                options=generate_dropdown_options('age_desc'),
                placeholder="Select Age",
                clearable=True,
                style={'width': '200px', 'marginBottom': '10px'}
            ),

            html.Label("Filter by Ethnic Description:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown-ethnic',
                options=generate_dropdown_options('ethnic_desc'),
                placeholder="Select Ethnic",
                clearable=True,
                style={'width': '200px', 'marginBottom': '10px'}
            ),

            html.Label("Filter by Area Description:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown-area',
                options=generate_dropdown_options('area_desc'),
                placeholder="Select Area",
                clearable=True,
                style={'width': '200px', 'marginBottom': '10px'}
            ),
        ], style={'padding': '20px', 'borderRight': '1px solid #ddd', 'width': '20%'}),
        
        # Bar chart
        html.Div([
            dcc.Graph(id='interactive-graph', style={'height': '600px'})
        ], style={'width': '75%', 'padding': '20px'})
    ], style={'display': 'flex', 'alignItems': 'flex-start'})
])

# Callbacks for static graphs
@app.callback(
    [
        Output('static-graph-1', 'figure'),
        Output('static-graph-2', 'figure'),
        Output('static-graph-3', 'figure'),
        Output('static-graph-4', 'figure'),
    ],
    [Input('static-chart-type', 'value')]
)
def update_static_graphs(chart_type):
    return (
        generate_graph(data, 'sex_desc', 'Count vs Year (Sex)', chart_type),
        generate_graph(data, 'age_desc', 'Count vs Year (Age)', chart_type),
        generate_graph(data, 'area_desc', 'Count vs Year (Area)', chart_type),
        generate_graph(data, 'ethnic_desc', 'Count vs Year (Ethnic)', chart_type),
    )

# Callback for interactive graph
@app.callback(
    Output('interactive-graph', 'figure'),
    [
        Input('interactive-chart-type', 'value'),
        Input('dropdown-field', 'value'),
        Input('dropdown-year', 'value'),
        Input('dropdown-sex', 'value'),
        Input('dropdown-age', 'value'),
        Input('dropdown-ethnic', 'value'),
        Input('dropdown-area', 'value')
    ]
)
def update_interactive_graph(chart_type, selected_field, selected_year, selected_sex, selected_age, selected_ethnic, selected_area):
    filtered_data = data.copy()

    if selected_year:
        filtered_data = filtered_data[filtered_data['year_desc'] == selected_year]
    if selected_sex:
        filtered_data = filtered_data[filtered_data['sex_desc'] == selected_sex]
    if selected_age:
        filtered_data = filtered_data[filtered_data['age_desc'] == selected_age]
    if selected_ethnic:
        filtered_data = filtered_data[filtered_data['ethnic_desc'] == selected_ethnic]
    if selected_area:
        filtered_data = filtered_data[filtered_data['area_desc'] == selected_area]

    return generate_graph(filtered_data, selected_field, f"Count by {selected_field.replace('_', ' ').title()}", chart_type)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
