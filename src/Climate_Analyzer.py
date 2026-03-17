import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import json
import importlib
import SeaLevel
importlib.reload(SeaLevel)
import Correlations
importlib.reload(Correlations)
import Carbon_Emissions
from Carbon_Emissions import data_carbon_scatter
import Temperature
importlib.reload(Temperature)
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import plotly.io as pio
import warnings
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import base64
from dash.dependencies import Input, Output

warnings.filterwarnings("ignore")


#------LAYOUT-------

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Layout
app.layout = html.Div([
html.H1(
    "Climate Change and Correlation Analyzer", 
    style={
        'background': 'linear-gradient(90deg, #4a5568, #2d3748)',  # Subtle modern gradient with dark tones
        'color': '#e2e8f0',  # Light gray text for contrast
        'text-align': 'center', 
        'font-family': 'Arial, sans-serif', 
        'font-weight': '900', 
        'padding': '20px', 
        'border-radius': '12px', 
        'box-shadow': '0 6px 10px rgba(0, 0, 0, 0.3)',
        'letter-spacing': '1.5px',
        'text-transform': 'uppercase'
    }
),

    # Tabs for different dashboards
    dcc.Tabs(
        id='tabs', 
        value='dashboard-1', 
        children=[
            dcc.Tab(
                label='Temperature Analysis', 
                value='dashboard-1', 
                style={
                    'font-family': 'Roboto, sans-serif', 
                    'font-size': '16px', 
                    'font-weight': 'bold', 
                    'color': '#2c3e50', 
                    'padding': '10px', 
                    'border': '1px solid #dcdcdc', 
                    'border-radius': '8px'
                },
                selected_style={
                    'background': 'linear-gradient(90deg, #e3e4e6, #ffffff)', 
                    'color': '#2c3e50', 
                    'font-weight': 'bold', 
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
                    'padding': '12px', 
                    'border-radius': '8px',
                    'border': '1px solid #a0a0a0'
                }
            ),
            dcc.Tab(
                label='Natural Disasters Analysis', 
                value='dashboard-2', 
                style={
                    'font-family': 'Roboto, sans-serif', 
                    'font-size': '16px', 
                    'font-weight': 'bold', 
                    'color': '#2c3e50', 
                    'padding': '10px', 
                    'border': '1px solid #dcdcdc', 
                    'border-radius': '8px'
                },
                selected_style={
                    'background': 'linear-gradient(90deg, #e3e4e6, #ffffff)', 
                    'color': '#2c3e50', 
                    'font-weight': 'bold', 
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
                    'padding': '12px', 
                    'border-radius': '8px',
                    'border': '1px solid #a0a0a0'
                }
            ),
            dcc.Tab(
                label='Carbon Emissions', 
                value='dashboard-3', 
                style={
                    'font-family': 'Roboto, sans-serif', 
                    'font-size': '16px', 
                    'font-weight': 'bold', 
                    'color': '#2c3e50', 
                    'padding': '10px', 
                    'border': '1px solid #dcdcdc', 
                    'border-radius': '8px'
                },
                selected_style={
                    'background': 'linear-gradient(90deg, #e3e4e6, #ffffff)', 
                    'color': '#2c3e50', 
                    'font-weight': 'bold', 
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
                    'padding': '12px', 
                    'border-radius': '8px',
                    'border': '1px solid #a0a0a0'
                }
            ),
            dcc.Tab(
                label='Sea Levels', 
                value='dashboard-4', 
                style={
                    'font-family': 'Roboto, sans-serif', 
                    'font-size': '16px', 
                    'font-weight': 'bold', 
                    'color': '#2c3e50', 
                    'padding': '10px', 
                    'border': '1px solid #dcdcdc', 
                    'border-radius': '8px'
                },
                selected_style={
                    'background': 'linear-gradient(90deg, #e3e4e6, #ffffff)', 
                    'color': '#2c3e50', 
                    'font-weight': 'bold', 
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
                    'padding': '12px', 
                    'border-radius': '8px',
                    'border': '1px solid #a0a0a0'
                }
            ),
            dcc.Tab(
                label='Correlations', 
                value='dashboard-5', 
                style={
                    'font-family': 'Roboto, sans-serif', 
                    'font-size': '16px', 
                    'font-weight': 'bold', 
                    'color': '#2c3e50', 
                    'padding': '10px', 
                    'border': '1px solid #dcdcdc', 
                    'border-radius': '8px'
                },
                selected_style={
                    'background': 'linear-gradient(90deg, #e3e4e6, #ffffff)', 
                    'color': '#2c3e50', 
                    'font-weight': 'bold', 
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
                    'padding': '12px', 
                    'border-radius': '8px',
                    'border': '1px solid #a0a0a0'
                }
            ),
        ],
        style={
            'background-color': '#f8f9fa', 
            'border-radius': '10px', 
            'padding': '10px', 
            'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
        }
    ),

    # Content will switch based on selected tab
    html.Div(
        id='tabs-content',
        style={
            'background-color': '#ffffff',
            'padding': '25px',
            'border-radius': '10px',
            'box-shadow': '0 6px 12px rgba(0, 0, 0, 0.15)',
            'font-family': 'Georgia, serif',
            'font-size': '14px',
            'line-height': '1.6',
            'color': '#2c3e50'
        }
    )
]),



# Callbacks
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    # Temp (Heatmap and Choropleth Map dashboard)
    if tab == 'dashboard-1': 
     return html.Div(
        children=[
            # Added Global Temperature Anomalies Graph
            html.Div(
                children=[
                    html.H1('Global Temperature Anomalies (1850-2024)', style={'textAlign': 'center'}),
                    dcc.Graph(
                        id='temperature-anomaly-graph',
                        style={'height': '70vh'}
                    )
                ]
            ),
            
            html.Div(
                children=[
                    html.H1(children='Average Temperature Heatmap by Cities',
                            style={'font-size': '36px', 'color': 'white'}),
                    html.P(children='This dashboard visualizes the temperature heatmap of major cities over time.',
                        style={'font-size': '20px', 'color': 'white', 'margin-top': '0px'})
                ],
                style={'text-align': 'center', 'padding-top': '50px', "display": 'block', "font-family": "PT Sans Narrow"}
            ),

            # Add the year range slider for the heatmap
            html.Div([
                html.Label("Select Year Range for Heatmap:"),
                dcc.RangeSlider(
                    id='year-slider-6',
                    min=1960,
                    max=2024,
                    step=1,
                    marks={i: str(i) for i in range(1960, 2025, 5)},
                    value=[1980, 2024]
                ),
            ], style={'margin-bottom': '20px'}),

            # Heatmap Graph with increased height
            dcc.Graph(
                id='heatmap', 
                figure=Temperature.fig_heat,
                style={'height': '700px'}  # Increased height of the heatmap
            ),

            # Timeline chart section
            html.Div([
                html.H2("Earth Temperature Timeline", style={'color': 'white'}),
                dcc.Graph(id='timeline-chart'),
                html.Div([
                    html.Label("Select Year Range for Timeline:"),
                    dcc.RangeSlider(
                        id='year-slider-timeline',
                        min=1960,
                        max=2024,
                        step=1,
                        marks={i: str(i) for i in range(1960, 2025, 5)},
                        value=[1980, 2024]
                    ),
                ], style={'margin-bottom': '20px'}),
            ], style={'background-color': '#4482C1', 'padding': '20px'}),  # Timeline chart section with background color

            # Choropleth Map Section
            html.Div([
                html.H2("Average Temperature Choropleth Map", style={'color': 'white'}),

                # Dropdown for selecting country
                html.Label("Select Country:"),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[
                        {'label': 'India', 'value': 'India'},
                        {'label': 'China', 'value': 'China'},
                        {'label': 'Canada', 'value': 'Canada'},
                        {'label': 'Brazil', 'value': 'Brazil'},
                        {'label': 'Russia', 'value': 'Russia'},
                        {'label': 'United States', 'value': 'US'},
                    ],
                    value='India',  # Default country
                    style={'width': '50%'}
                ),

                # Choropleth Map for selected country
                dcc.Graph(id='choropleth-map', style={'height': '700px'}),  # Map height adjustment
            ], style={'background-color': '#4482C1', 'padding': '20px'}),

            #Monthly Average Temperature (1995-2020)
            html.Div(children=[
                html.H1(
                    children='Monthly Average Temperature (1995-2020)',
                    style={'font-family': 'Helvetica', 'text-align': 'center', 'margin-top': '20px', 'font-weight': 'bold'}
                ),
                html.Div([
                    html.Div([
                        html.Label('Select a Country', style={'margin-right': '10px'}),
                        dcc.Dropdown(
                            id='country-dropdown-2',
                            options=[{'label': country, 'value': country} for country in sorted(Temperature.fig_CC['Country'].unique())],
                            value=Temperature.fig_CC['Country'].iloc[0],
                            style={'width': '200px'}
                        )
                    ], style={'margin-right': '20px'}),

                    html.Div([
                        html.Label('Select a City', style={'margin-right': '10px'}),
                        dcc.Dropdown(
                            id='city-dropdown-2',
                            options=[{'label': city, 'value': city} for city in sorted(Temperature.fig_CC['City'].unique())],
                            value=Temperature.fig_CC['City'].iloc[0],
                            style={'width': '200px'}
                        )
                    ], style={'margin-right': '20px'}),

                    html.Div([
                        html.Label('Select a Year', style={'margin-right': '10px'}),
                        dcc.Dropdown(
                            id='year-dropdown-2',
                            options=[{'label': year, 'value': year} for year in range(1995, 2021)],
                            value=Temperature.fig_CC['Year'].iloc[0],
                            style={'width': '200px'}
                        )
                    ])
                ], style={
                    'display': 'flex',
                    'flex-direction': 'row',
                    'align-items': 'center',
                    'background-color': '#2a3c5c',
                    'padding': '20px'
                }),
                dcc.Graph(
                    id='monthly-temperature',
                    style={"margin": "10px", 'border': '3px solid #2A547E', 'display': 'block', 'flex-wrap': 'wrap'}
                ),
            ]),

            # Appended content from dashboard-1
            html.Div([
                html.Div([
                    html.Label("Select Year Range:"),
                    dcc.RangeSlider(
                        id='year-slider-1',
                        min=1960,
                        max=2024,
                        step=1,
                        marks={i: str(i) for i in range(1960, 2025, 5)},
                        value=[1980, 2024]
                    ),
                ], style={'margin-bottom': '20px'}),
                dcc.Graph(id='temperature-world-map'),
                dcc.Graph(id='temperature-bar'),
                dcc.Graph(id='mean-temp-line'),
            ], style={'background-color': '#2a3c5c', 'padding': '20px'}),  # Appended section wrapped in a div
        ],
        style={'background-color': '#2a3c5c'}
    )

    elif tab == 'dashboard-2':
     return html.Div(
        children=[
            # Title for the dashboard
            html.H1(
                'Global Natural Disaster Analysis Dashboard',
                style={
                    'textAlign': 'center',
                    'color': '#e2e8f0',
                    'font-size': '28px',
                    'font-family': 'Roboto, sans-serif',
                    'margin-bottom': '20px'
                }
            ),

            # Section 1: Matplotlib graph for occurrences and temperature anomaly
            html.Div(
                children=[
                    html.H2(
                        'All Natural Disaster Occurrences and Temperature Anomaly (1980-2024)',
                        style={
                            'textAlign': 'center',
                            'color': '#cbd5e0',
                            'font-size': '22px',
                            'margin-bottom': '15px'
                        }
                    ),
                    html.Img(
                        id='matplotlib-graph',
                        style={
                            'width': '100%',
                            'height': 'auto',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    )
                ],
                style={
                    'padding': '20px',
                    'background-color': '#2d3748',
                    'border-radius': '12px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                    'margin-bottom': '20px'
                }
            ),

            # Section 2: Matplotlib graph for economic damage
            html.Div(
                children=[
                    html.H2(
                        'Economic Damage by Type of Natural Disaster (1980-2024)',
                        style={
                            'textAlign': 'center',
                            'color': '#cbd5e0',
                            'font-size': '22px',
                            'margin-bottom': '15px'
                        }
                    ),
                    html.Img(
                        id='econ-damage-graph',
                        style={
                            'width': '100%',
                            'height': 'auto',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    )
                ],
                style={
                    'padding': '20px',
                    'background-color': '#2d3748',
                    'border-radius': '12px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                    'margin-bottom': '20px'
                }
            ),

            # Section 3: Global Natural Disaster Occurrences
            html.Div(
                children=[
                    html.H1(
                        'Global Natural Disaster Occurrences (1980-2024)',
                        style={
                            'textAlign': 'center',
                            'color': '#e2e8f0',
                            'font-size': '28px',
                            'margin-bottom': '20px'
                        }
                    ),
                    dcc.Graph(
                        id='disaster-chart',
                        style={
                            'height': '70vh',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    )
                ],
                style={
                    'padding': '20px',
                    'background-color': '#1a202c',
                    'border-radius': '12px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            )
        ],
        style={
            'background-color': '#1a202c',
            'padding': '30px'
        }
    )


        
    #Carbon Emissions
    elif tab == 'dashboard-3':
     return html.Div(
        children=[
            # Dashboard Title
            html.Div(
                children=[
                    html.H1(
                        'Carbon Emissions',
                        style={
                            'font-size': '28px',
                            'color': '#e2e8f0',
                            'text-align': 'center',
                            'margin-bottom': '15px',
                            'font-family': 'Roboto, sans-serif'
                        }
                    ),

                   
                ],
                style={
                    'padding': '20px',
                    'background-color': '#2d3748',
                    'border-radius': '12px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            ),

            # Dropdown for country selection
            html.Div(
                children=[
                    html.Label(
                        'Select countries to display:',
                        style={
                            'color': '#e2e8f0',
                            'margin-bottom': '10px',
                            'font-size': '16px'
                        }
                    ),

                   

                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[
                            {"label": country, "value": country} 
                            for country in data_carbon_scatter["Country"].unique()
                        ],
                        value=["United States", "China"],
                        multi=True,
                        style={
                            'width': '700px',
                            'background-color': '#000000',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'color': '#e2e8f0'
                        },
                        
                    )
                ],
                style={
                    'margin-bottom': '20px',
                    'padding': '10px',
                    'background-color': '#000000',
                    'border-radius': '12px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            ),

            # Scatterplot Graph
            dcc.Graph(
                id="carbon-emissions-scatterplot",
                style={
                    'margin-bottom': '20px',
                    'background-color': '#2d3748',
                    'border': '1px solid #4a5568',
                    'border-radius': '8px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            ),

            # Top 10 Carbon Emitting Countries Bar Chart
            html.H2(
                'Top 10 Carbon Emitting Countries - Growth',
                style={
                    'font-size': '22px',
                    'color': '#e2e8f0',
                    'margin-bottom': '15px'
                }
            ),
            dcc.Graph(
                id='carbon-emissions-bar',
                figure=Carbon_Emissions.fig_race,
                style={
                    'margin-bottom': '20px',
                    'background-color': '#2d3748',
                    'border': '1px solid #4a5568',
                    'border-radius': '8px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            ),

            # Interval Component
            dcc.Interval(
                id='interval-component',
                interval=600,
                n_intervals=0
            ),

            # Top 5 and Bottom 5 Emissions Graphs
            html.Div(
                children=[
                    dcc.Graph(
                        id='carbon-emissions-top-5',
                        figure=Carbon_Emissions.fig_top_5,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    ),
                    dcc.Graph(
                        id='carbon-emissions-bottom-5',
                        figure=Carbon_Emissions.fig_bottom_5,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    )
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "justify-content": "space-between",
                    "width": "100%",
                    "gap": "10px"
                }
            ),

            # Additional Graphs
            dcc.Graph(
                id="carbon-bubble",
                figure=Carbon_Emissions.fig_bb,
                style={
                    'margin-bottom': '20px',
                    'background-color': '#2d3748',
                    'border': '1px solid #4a5568',
                    'border-radius': '8px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            ),
            dcc.Graph(
                id='top-5-chart',
                figure=Carbon_Emissions.top_5_fig,
                style={
                    'margin-bottom': '20px',
                    'background-color': '#2d3748',
                    'border': '1px solid #4a5568',
                    'border-radius': '8px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            ),
            dcc.Graph(
                id='bottom-5-chart',
                figure=Carbon_Emissions.bottom_5_fig,
                style={
                    'margin-bottom': '20px',
                    'background-color': '#2d3748',
                    'border': '1px solid #4a5568',
                    'border-radius': '8px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            ),

            # Choropleth and Heatmap
            dcc.Graph(
                id='choropleth-carbon-emissions',
                figure=Carbon_Emissions.fig_carbon_choro,
                style={
                    'margin-bottom': '20px',
                    'background-color': '#2d3748',
                    'border': '1px solid #4a5568',
                    'border-radius': '8px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                    'width': '100%',
                    'height': '850px'
                }
            ),
            dcc.Graph(
                id='heatmap-carbon-emissions',
                figure=Carbon_Emissions.fig_heat_carbon,
                style={
                    'margin-bottom': '20px',
                    'background-color': '#2d3748',
                    'border': '1px solid #4a5568',
                    'border-radius': '8px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                    'width': '100%',
                    'height': '850px'
                }
            )
        ],
        style={
            'background-color': '#1a202c',
            'padding': '30px'
        }
    )


#SeaLevel
    elif tab == 'dashboard-4':
      return html.Div(
        children=[
            # Dashboard Title
            html.Div(
                children=[
                    html.H1(
                        'Sea Level Change',
                        style={
                            'font-size': '28px',
                            'color': '#e2e8f0',
                            'text-align': 'center',
                            'margin-bottom': '15px',
                            'font-family': 'Roboto, sans-serif'
                        }
                    ),
                ],
                style={
                    'padding': '20px',
                    'background-color': '#2d3748',
                    'border-radius': '12px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            ),

            # Graphs Section
            html.Div(
                children=[
                    # Bar Graph
                    dcc.Graph(
                        id='sea-level-bar',
                        figure=SeaLevel.fig_bar,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    ),
                    
                    # Scatter Graph
                    dcc.Graph(
                        id='sea-level-scatter',
                        figure=SeaLevel.scatter_fig,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    ),

                    # Box and Area Graphs in Flexbox
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='sea-level-box',
                                figure=SeaLevel.fig_box,
                                style={
                                    'margin-bottom': '20px',
                                    'margin-right': '10px',
                                    'width': '50%',
                                    'background-color': '#2d3748',
                                    'border': '1px solid #4a5568',
                                    'border-radius': '8px',
                                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                                }
                            ),
                            dcc.Graph(
                                id='sea-level-area',
                                figure=SeaLevel.area_fig,
                                style={
                                    'margin-bottom': '20px',
                                    'margin-left': '10px',
                                    'width': '50%',
                                    'background-color': '#2d3748',
                                    'border': '1px solid #4a5568',
                                    'border-radius': '8px',
                                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                                }
                            )
                        ],
                        style={
                            "display": "flex",
                            "flex-direction": "row",
                            "justify-content": "space-between",
                            "width": "100%"
                        }
                    ),

                    # Line Chart
                    dcc.Graph(
                        id="line-chart",
                        figure=SeaLevel.fig_line,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    )
                ],
                style={
                    'padding': '20px',
                    'background-color': '#1a202c',
                    'border-radius': '12px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                },
                id='Sea-Levels'
            )
        ],
        style={
            'background-color': '#1a202c',
            'padding': '30px'
        }
    )

#Correlations
    elif tab == 'dashboard-5':
       return html.Div(
        children=[
            # Dashboard Title
            html.Div(
                children=[
                    html.H1(
                        'Correlation between Average Land & Ocean Temperature, Carbon Emissions and Sea Level (1990-2020)',
                        style={
                            'font-size': '28px',
                            'color': '#e2e8f0',
                            'text-align': 'center',
                            'margin-bottom': '15px',
                            'font-family': 'Roboto, sans-serif'
                        }
                    ),
                    html.P(
                        'This dashboard visualizes Average Land temperature, Average Carbon Emission, and Average Sea Level in a single plot.',
                        style={
                            'font-size': '18px',
                            'color': '#cbd5e0',
                            'text-align': 'center',
                            'margin-bottom': '20px'
                        }
                    )
                ],
                style={
                    'padding': '20px',
                    'background-color': '#2d3748',
                    'border-radius': '12px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                }
            ),

            # Graphs Section
            html.Div(
                children=[
                    # Correlation Line Chart for Temperature
                    dcc.Graph(
                        id='corr_line_temp',
                        figure=Correlations.fig_corr_temp,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    ),

                    # Correlation Line Chart
                    dcc.Graph(
                        id='corr_line',
                        figure=Correlations.fig_corr1,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    ),

                    # Correlation Bar Chart for Emissions
                    dcc.Graph(
                        id='corr_bar_em',
                        figure=Correlations.fig_emissions,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    ),

                    # Additional Correlation Line and Scatter Charts
                    dcc.Graph(
                        id='corr_line_1',
                        figure=Correlations.fig_corr3,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    ),
                    dcc.Graph(
                        id='corr_scatter',
                        figure=Correlations.fig_corr2,
                        style={
                            'margin-bottom': '20px',
                            'background-color': '#2d3748',
                            'border': '1px solid #4a5568',
                            'border-radius': '8px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        }
                    )
                ],
                style={
                    'padding': '20px',
                    'background-color': '#1a202c',
                    'border-radius': '12px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                    'margin-top': '20px'
                }
            )
        ],
        style={
            'background-color': '#1a202c',
            'padding': '30px'
        }
    )


    
@app.callback(
    Output('temperature-bar', 'figure'),
    [Input('year-slider-1', 'value')]
)
def update_temperature_bar(year_range):
    start_year, end_year = year_range
    filtered_df = Temperature.df_melt[(Temperature.df_melt['Year'] >= start_year) & (Temperature.df_melt['Year'] <= end_year)]
    top_countries = (
        filtered_df.groupby(['Year', 'Country'])['Temperature_Change']
        .mean()
        .reset_index()
        .groupby('Year')
        .apply(lambda x: x.nlargest(1, 'Temperature_Change'))
        .reset_index(drop=True)
    )
    fig = px.bar(
        top_countries.sort_values('Year', ascending=False),
        x='Year', y='Temperature_Change', color='Temperature_Change',
        title='Countries with Maximum Temperature Change',
        text='Country'
    )
    return fig

# @app.callback(
#     Output('global-temp-anomalies', 'figure'),
#     [Input('year-slider-1', 'value')]
# )
# def update_global_temp_anomalies(year_range):
#     start_year, end_year = year_range
#     filtered_df = df_global_temp[(df_global_temp['Year'] >= start_year) & (df_global_temp['Year'] <= end_year)]
#     fig = px.line(
#         filtered_df, x='Year', y='Temperature Anomaly',
#         title='Global Temperature Anomalies',
#         markers=True
#     )
#     return fig

@app.callback(
    Output('mean-temp-line', 'figure'),
    [Input('year-slider-1', 'value')]
)
def update_mean_temp_line(year_range):
    start_year, end_year = year_range
    filtered_df = Temperature.mean_temp_change_by_year[
        (Temperature.mean_temp_change_by_year['Year'] >= start_year) & (Temperature.mean_temp_change_by_year['Year'] <= end_year)
    ]
    fig = px.line(
        filtered_df, x='Year', y='Temperature_Change',
        title='Mean Temperature Change by Year',
        markers=True
    )
    return fig

@app.callback(
    Output('temperature-world-map', 'figure'),
    [Input('year-slider-1', 'value')]
)
def update_temperature_world_map(year_range):
    start_year, end_year = year_range
    filtered_df = Temperature.df_melt[
        (Temperature.df_melt['Year'] >= start_year) & (Temperature.df_melt['Year'] <= end_year)
    ]
    fig = px.choropleth(
        filtered_df, geojson=Temperature.world_json, featureidkey='properties.name',
        locations='Country', color='Temperature_Change',
        title='World Map of Temperature Change',
        color_continuous_scale='orrd', projection='orthographic'
    )
    return fig

@app.callback(
    Output('disaster-occurrences', 'figure'),
    [Input('year-slider-2', 'value')]
)
def update_disaster_occurrences(year_range):
    start_year, end_year = year_range
    filtered_df = Temperature.df_disasters.loc[start_year:end_year]
    fig = px.bar(
        filtered_df,
        x=filtered_df.index,
        y=filtered_df.sum(axis=1),
        title='Total Natural Disaster Occurrences'
    )
    return fig

@app.callback(
    Output('economic-damage', 'figure'),
    [Input('year-slider-2', 'value')]
)
def update_economic_damage(year_range):
    start_year, end_year = year_range
    filtered_df = Temperature.df_economic_damage.loc[start_year:end_year]
    fig = px.bar(
        filtered_df,
        x=filtered_df.index,
        y=filtered_df.sum(axis=1) / 1e9,
        title='Economic Damage by Natural Disasters (in Billion USD)'
    )
    return fig

@app.callback(
    Output('correlation-matrix', 'figure'),
    [Input('year-slider-2', 'value')]
)
def update_correlation_matrix(year_range):
    start_year, end_year = year_range
    filtered_df = Temperature.combined_df.loc[start_year:end_year]
    correlation_table = filtered_df.corr()
    fig = px.imshow(
        correlation_table,
        text_auto=True,
        color_continuous_scale='RdYlGn',
        title='Correlation Matrix'
    )
    return fig

#Heatmap Callback
@app.callback(
    Output('heatmap', 'figure'),
    [Input('year-slider-6', 'value')]  # Add any input components you want to bind
)
def update_heatmap(selected_year_range):
    # Apply filtering or data processing based on the selected_year_range
    filtered_data = Temperature.data_heatmap[Temperature.data_heatmap['dt'].between(selected_year_range[0], selected_year_range[1])]
    fig = px.density_mapbox(
        filtered_data, 
        lat='Latitude_Float', 
        lon='Longitude_Float', 
        z='AverageTemperature',
        hover_data=["City"],
        radius=8,
        zoom=1,
        mapbox_style="carto-positron",
        animation_frame='dt',
        opacity=0.5,
        title='Average Temperature Heatmap by Cities'
    )
    return fig

# Callback for the Timeline Chart
@app.callback(
    Output('timeline-chart', 'figure'),
    [Input('year-slider-timeline', 'value')]
)
def update_timeline(selected_year_range):
    filtered_data_timeline = Temperature.data_timeline[Temperature.data_timeline['Year'].between(selected_year_range[0], selected_year_range[1])]
    
    fig_timeline = px.line(
        filtered_data_timeline,
        x='Year',
        y='Average_Land_Temperature (celsius)',
        title='Earth Temperature Timeline'
    )
    fig_timeline.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Land Temperature (°C)',
        title='Earth Temperature Timeline'
    )

    return fig_timeline


# Callback for Choropleth Map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_choropleth_map(country):
    # Define a map of the figures for each country
    country_figures = {
        'India': Temperature.fig11,
        'China': Temperature.fig21,
        'Canada': Temperature.fig31,
        'Brazil': Temperature.fig41,
        'Russia': Temperature.fig51,
        'US': Temperature.fig61,
    }
    # Return the corresponding figure based on the selected country
    return country_figures.get(country, Temperature.fig61)  # Default to US if no match


#Monthly-Temperature

@app.callback(
    dash.dependencies.Output('city-dropdown', 'options'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_cities_options(selected_country):
    filtered_fig_df = Temperature.fig_CC[Temperature.fig_CC['Country'] == selected_country]
    cities = filtered_fig_df['City'].unique()
    options = [{'label': city, 'value': city} for city in cities]
    return options

@app.callback(
    dash.dependencies.Output('monthly-temperature', 'figure'),
    [dash.dependencies.Input('country-dropdown-2', 'value'),
     dash.dependencies.Input('city-dropdown-2', 'value'),
     dash.dependencies.Input('year-dropdown-2', 'value')])
def update_figure(country, city, year):
        df_country_city_year = Temperature.fig_CC[(Temperature.fig_CC["Country"] == country) & (Temperature.fig_CC["City"] == city) & (Temperature.fig_CC["Year"] == year)]
        df_country_city_year = df_country_city_year[df_country_city_year["AvgTemperature"] != -99]
        df_country_city_year["AvgTemperature"] = (df_country_city_year["AvgTemperature"] - 32) / 1.8
        df_country_city_year["datetime"] = pd.to_datetime(df_country_city_year[["Year", "Month", "Day"]])
        df_country_city_year.set_index("datetime", inplace=True)

        fig = go.Figure(data=go.Heatmap(
            z=df_country_city_year["AvgTemperature"],
            x=df_country_city_year.index.day,
            y=df_country_city_year.index.month,
            colorscale='Jet',
            colorbar=dict(title="Temperature (°C)"),
            zmin=df_country_city_year["AvgTemperature"].min(), 
            zmax=df_country_city_year["AvgTemperature"].max(),
            hovertemplate="Day: %{x}<br>Month: %{y}<br>Temperature: %{z:.2f}°C<extra></extra>",
        ))
        fig.update_layout(
            title=f"Monthly Average Temperature in {city}, {country} ({year})",
            xaxis=dict(title="Day"),
            yaxis=dict(title="Month"),
        )

        return fig

#Carbon Emissions call back
@app.callback(Output("carbon-emissions-scatterplot", "figure"),
              [Input("country-dropdown", "value")])
def update_scatterplot(countries):
    filtered_data_carbon_scatter = data_carbon_scatter[
    data_carbon_scatter["Country"].isin(countries)
]

    fig_carbon_scatter = px.scatter(filtered_data_carbon_scatter,title="Scatter Plot - Average Carbon Emissions by Country", x="Year", y="CO2 Emissions", color="Country", hover_data=["Country"])
    fig_carbon_scatter.update_layout(xaxis_title="Year",
                      yaxis_title="CO2 Emissions (MTCO2e) ",
                      font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False))
    return fig_carbon_scatter


# Define callback function to update figure with animation frames
@app.callback(Output('carbon-emissions-bar', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_carbon_emissions_bar(n):
    # Calculate next frame index
    frame_index = n % len(Carbon_Emissions.frames)
    current_year = Carbon_Emissions.top10_countries['Year'].unique()[frame_index]
    
    # Update the figure title with the current year
    Carbon_Emissions.fig_race.update_layout(title=f'Top 10 Carbon Emitting Countries - {current_year}'),
    # Return next frame
    return Carbon_Emissions.frames[frame_index]

#NaturalDisaster
@app.callback(
    Output('disaster-chart', 'figure'),
    Input('disaster-chart', 'id')
)
def update_chart(_):
    fig = px.bar(
        Temperature.melted_df,
        x='Year',
        y='Occurrences',
        color='Disaster Type',
        title='Global occurrences of natural disasters for 1980-2024',
        labels={'Occurrences': 'Number of Occurrences', 'Year': 'Year'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Occurrences",
        legend_title="Disaster Type"
    )
    return fig

#Temperature Anomaly
@app.callback(
    Output('temperature-anomaly-graph', 'figure'),
    Input('temperature-anomaly-graph', 'id')  # Static graph, no dynamic inputs
)
def update_temperature_anomaly_graph(_):
    # Create the figure
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=Temperature.global_temp_df.index,
            y=Temperature.global_temp_df['Temperature Anomaly'],
            mode='lines',
            line=dict(color='red'),
            name='Temperature Anomaly'
        )
    )
    
    # Update layout for the figure
    figure.update_layout(
        title='Global Temperature Anomalies (Annual) for 1850-2024',
        xaxis_title='Year',
        yaxis_title='Temperature Anomaly (°C)',
        font=dict(size=14),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return figure

#Natural Disaster Anomaly Graph
# Callback to generate and serve the Matplotlib graph
@app.callback(
    Output('matplotlib-graph', 'src'),
    Input('tabs', 'value')  # Trigger the callback when switching to dashboard-2
)
def render_matplotlib_graph(tab):
    if tab == 'dashboard-2':
        # Create Matplotlib figure
        fig, ax = plt.subplots(figsize=(14, 8))
        ax2 = ax.twinx()

        # Plot the data
        line1 = ax.plot(
            Temperature.nat_disaster_df.loc[:2024, 'All natural disasters (Occurrence)'],
            '-ro', markersize=4, label='All natural disasters (Occurrence)'
        )
        line2 = ax2.plot(
            Temperature.global_temp_df.loc[1900:, 'Temperature Anomaly'],
            'b-', label='Temperature Anomaly'
        )

        lines = line1 + line2
        labels = [l.get_label() for l in lines]

        # Add labels and titles
        plt.title('All natural disaster occurrences and temperature anomaly for 1980-2024', fontsize=19)
        ax.set_xlabel('Year', fontsize=15)
        ax.set_ylabel('Occurrence', fontsize=15, color='r')
        ax2.set_ylabel('Temperature anomaly (degree Celsius)', fontsize=15, color='r')
        ax.legend(lines, labels, loc=0, prop={'size': 12})

        # Save the plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        # Encode the image to base64
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        # Return the image data as a base64-encoded string
        return f'data:image/png;base64,{encoded_image}'

    return None
    

# Run app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)
