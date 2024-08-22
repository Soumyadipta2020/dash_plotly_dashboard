import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Read data
df = pd.read_csv('./Cost_of_Living_Index_by_Country_2024.csv', header = 0)

# column names
column_names = df.columns.tolist()[2:]
# Unique values from Country
unique_country = df['Country'].unique()

app = Dash(__name__)

# Layout
app.layout = [
    html.H1(children='Cost of Living Index by Country 2024', style={'textAlign':'center'}),
    html.Content(children='Data Source - ', style = {'fontWeight': 'bold'}),
    html.A(children="Kaggle", href = "https://www.kaggle.com/datasets/myrios/cost-of-living-index-by-country-by-number-2024?resource=download"),
    html.Br(),
    html.Content(children='The cost of living indices are relative to New York City (NYC), with a baseline index of 100% for NYC. \
                 Here is a breakdown of each index and its meaning:'),
    html.Li(children="Cost of Living Index Excl. Rent: This index indicates the relative prices of consumer goods like groceries, restaurants, \
                 transportation, and utilities. It excludes accommodation expenses such as rent or mortgage. For instance, \
                 a city with a Cost of Living Index of 120 is estimated to be 20% more expensive than New York City \
                 excluding rent."),
    html.Li(children="Rent Index: This index estimates the prices of renting apartments in a city compared to New York City. If the Rent Index \
                 is 80, it suggests that the average rental prices in that city are approximately 20% lower than those \
                 in New York City."),
    html.Li(children="Cost of Living Plus Rent Index: This index estimates consumer goods prices, including rent, in comparison to New York City."),
    html.Li(children="Groceries Index: This index provides an estimation of grocery prices in a city relative to New York City. Numbeo uses item \
                 weights from the 'Markets' section to calculate this index for each city."),
    html.Li(children="Restaurants Index: This index compares the prices of meals and drinks in restaurants and bars to those in NYC."),
    html.Li(children="Local Purchasing Power: This index indicates the relative purchasing power in a given city based on the average net salary. \
            A domestic purchasing power of 40 means that residents with an average salary can afford, on average, \
                 60% less goods and services compared to residents of New York City with an average salary."),
    html.H1(children='Imported Data', style={'textAlign':'left'}),
    dash_table.DataTable(
        id = "data_imported", 
        data = df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={'height': '300px', 'overflowY': 'auto'}, # Table height & width
        fixed_rows={'headers': True}, # Fix header
        filter_action='native',  # Enable filtering
        style_cell={
            'textAlign': 'center',
            'padding': '5px',
            'whiteSpace': 'normal',  # Allow content to wrap
            'height': 'auto',
            'minWidth': '100px', 'width': 'auto', 'maxWidth': '300px',  # Auto column width settings
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold'
        }
    ), 
    html.H1(children="Visualize Index", style = {'textalign':'left'}),
    html.Div([
        html.Div([
            html.Label("Index Type",  style = {'fontWeight': 'bold'}),
            dcc.Dropdown(options=[{'label': col, 'value': col} for col in column_names],
                     value=column_names[0],
                     id='col-dropdown', multi=True, clearable=False, 
                     placeholder = 'Index Type')
        ], style={'width': '28%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Countries",  style = {'fontWeight': 'bold'}),
            dcc.Dropdown(options=[{'label': val, 'value': val} for val in unique_country],
                     value=list(unique_country)[0:5],
                     id='country-dropdown', multi=True, clearable=False, 
                     placeholder = 'Country')
        ], style={'width': '48%', 'display': 'inline-block', 'paddingLeft': '10px'}),
        html.Div([
            html.Label("Plot Type",  style = {'fontWeight': 'bold'}),
            dcc.Dropdown(options=['Line Plot', 'Violin Plot', 'Bar Plot'],
                     value='Line Plot',
                     id='plot-dropdown', multi=False, clearable=False, 
                     placeholder = 'Plot Type')
        ], style={'width': '20%', 'display': 'inline-block', 'paddingLeft': '10px'}),
        dcc.Graph(id='graph-output')
    ]),
]

# Graph plot
@app.callback(
    Output('graph-output', 'figure'),
    [Input('col-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('plot-dropdown', 'value')]
)

def update_graph(selected_column, selected_entries, selected_plot):
    if not selected_entries:
        raise dash.exceptions.PreventUpdate
    filtered_df = df[df['Country'].isin(selected_entries)]
    if selected_plot == 'Line Plot':
        fig = px.line(filtered_df, x = 'Country', y = selected_column, title = 'Country vs Index')
    elif selected_plot == 'Violin Plot':
        fig = px.violin(filtered_df, y = selected_column, box = True, title = 'Indices')
    elif selected_plot == 'Bar Plot':
        fig = px.bar(filtered_df, x = 'Country', y = selected_column, title = 'Country vs Index', barmode='group')
    return fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)