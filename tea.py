import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import os # For path handling


DATA_FILE = r"pollution_wards.csv"


df = pd.read_csv(DATA_FILE, encoding='latin-1')


# --- Dash App Initialization ---
app = dash.Dash(__name__)

server = app.server # This line is crucial for Render deployment

# --- App Layout ---
app.layout = html.Div(
    style={'backgroundColor': '#f8f9fa', 'fontFamily': 'Inter, sans-serif', 'padding': '20px'},
    children=[
        html.H1(
            "Pollution Intensity (Heatmap)",
            style={'textAlign': 'center', 'color': '#343a40', 'marginBottom': '30px'}
        ),
        html.Div(
            style={
                'width': '90%',
                'maxWidth': '1200px',
                'margin': '0 auto',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'backgroundColor': 'white'
            },
            children=[
                dcc.Graph(
                    id='heatmap-graph',
                    # Create the heatmap using plotly.express
                    # `lat` and `lon` define the points
                    # `z` defines the intensity for the heatmap colors
                    # `radius` controls the size of the "heat" circles
                    figure=px.density_mapbox(
                        df,
                        lat="LATITUDE",
                        lon="LONGITUDE",
                        z="Tonnes", # The column used for heatmap intensity
                        radius=40,     # Adjust radius for how spread out the heat should be
                        center={"lat": df['LATITUDE'].mean(), "lon": df['LONGITUDE'].mean()},
                        zoom=10,       # Initial zoom level
                        mapbox_style="open-street-map",
                        title="Pollution Intensity Distribution by Ward",
                        color_continuous_scale=px.colors.sequential.Plasma, # Example color scale
                        range_color=[0, 20]
                    ),
                    style={'height': '70vh', 'width': '100%'}
                ),
                html.Div(
                    html.P("This heatmap visualizes the intensity of pollution based on ward-level latitude and longitude data. Higher intensity areas appear 'hotter'.",
                           style={'textAlign': 'center', 'marginTop': '20px', 'color': '#6c757d'})
                )
            ]
        )
    ]
)

# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True)
