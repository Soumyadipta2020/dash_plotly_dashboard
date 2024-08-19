from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# source - https://www.kaggle.com/datasets/myrios/cost-of-living-index-by-country-by-number-2024?resource=download
df = pd.read_csv('./Cost_of_Living_Index_by_Country_2024.csv', header = 0)

app = Dash(__name__)

app.layout = [
    html.H1(children='Cost of Living Index by Country 2024', style={'textAlign':'center'})
]


# Run app
if __name__ == '__main__':
    app.run(debug=True)