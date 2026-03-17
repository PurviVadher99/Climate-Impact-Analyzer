#Correlation
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
# Load data from a CSV file
data_temp = pd.read_csv('avg_dataset.csv')

# Extract the relevant columns
years = data_temp['Year']
temp = data_temp['Average_Land_Temperature (celsius)']
temp1 = data_temp['Average_LandOcean_Temperature (celsius)']
emissions = data_temp['Average_Emissions (MtCO₂e)']
sea=data_temp['Average_Sealevel (mm)']

# Create figure
fig_corr1 = go.Figure()

# Add trace for temperature
fig_corr1.add_trace(go.Scatter(x=years, y=temp,
                         mode='lines+markers',
                         name='Land Temperature',
                         line=dict(color='lime', width=2),
                         marker=dict(color='lime', size=8)))

# Add trace for emissions
fig_corr1.add_trace(go.Scatter(x=years, y=emissions,
                         mode='lines+markers',
                         name='Carbon Emissions',
                         line=dict(color='aqua', width=2),
                         marker=dict(color='aqua', size=8),
                         yaxis='y2')) # assign the second y-axis to the emissions trace
# Add trace for emissions
fig_corr1.add_trace(go.Scatter(x=years, y=sea,
                         mode='lines+markers',
                         name='Sea level',
                         line=dict(color='red', width=2),
                         marker=dict(color='red', size=8),
                         yaxis='y3'))

# Update layout with custom styling
fig_corr1.update_layout(
#     plot_bgcolor='#FFFFFF', # set plot area background color
#     paper_bgcolor='#88B0D7', # remove background
    font=dict(family='Arial', size=12, color='black'), # set font and color
    title=dict(text='Relationship Between Average Land Temperature, Carbon Emissions, and Sea Level (1990-2020)', # set title
               xanchor='center', yanchor='top', x=0.5, y=0.95),
    xaxis=dict(title='Year', tickmode='linear', tick0=1990, dtick=5), # set x-axis title and tick values
    yaxis=dict(title='Temperature (°C Above Pre-Industrial Baseline)', range=[8.6, 10],color='red',title_font=dict(size=16)), # set y-axis title and range for temperature
    yaxis2=dict(title='Carbon Emissions-metric tons per capita', range=[22500, 37000], overlaying='y', side='right',color='blue',title_font=dict(size=16)), 
    yaxis3=dict(title='Sea level-mm', range=[-25, 69], overlaying='y', side='right',position=.94,color='green',title_font=dict(size=16)), # set y-axis title and range for emissions

    legend=dict(orientation='h', yanchor='bottom', y=-0.2), # move legend to bottom
)


# Create figure
fig_corr3 = go.Figure()

# Add trace for temperature
fig_corr3.add_trace(go.Scatter(x=years, y=temp1,
                         mode='lines+markers',
                         name='Land and Ocean Temperature',
                         line=dict(color='lime', width=2,shape='spline'),
                         marker=dict(color='lime', size=8)))

# Add trace for emissions
fig_corr3.add_trace(go.Scatter(x=years, y=emissions,
                         mode='lines+markers',
                         name='Carbon Emissions',
                         line=dict(color='aqua', width=2,shape='spline'),
                         marker=dict(color='aqua', size=8),
                         yaxis='y2')) # assign the second y-axis to the emissions trace
# Add trace for emissions
fig_corr3.add_trace(go.Scatter(x=years, y=sea,
                         mode='lines+markers',
                         name='Sea level',
                         line=dict(color='red', width=2,shape='spline'),
                         marker=dict(color='red', size=8),
                         yaxis='y3'))

# Update layout with custom styling
fig_corr3.update_layout(
#     plot_bgcolor='#FFFFFF', # set plot area background color
#     paper_bgcolor='#88B0D7', # remove background
    font=dict(family='Arial', size=12, color='black'), # set font and color
    title=dict(text='Correlation between Average Land and Ocean Temperature, Carbon Emissions and Sea level (1990-2020)', # set title
               xanchor='center', yanchor='top', x=0.5, y=0.95),
    xaxis=dict(title='Year', tickmode='linear', tick0=1990, dtick=5), # set x-axis title and tick values
    yaxis=dict(title='Temperature (°C above pre-industrial levels)', range=[14, 18],color='lime',title_font=dict(size=16)), # set y-axis title and range for temperature
    yaxis2=dict(title='Carbon Emissions (metric tons per capita)', range=[22500, 37000], overlaying='y', side='right',color='aqua',title_font=dict(size=16)), 
    yaxis3=dict(title='Sea level(mm)', range=[-25, 69], overlaying='y', side='right',position=.94,color='red',title_font=dict(size=16)), # set y-axis title and range for emissions

    legend=dict(orientation='h', yanchor='bottom', y=-0.2), # move legend to bottom
)


data_temp_subset = data_temp[['Year','Average_Land_Temperature (celsius)','Average_Emissions (MtCO₂e)','Average_Sealevel (mm)']]
fig_corr2=px.scatter(data_temp_subset, x='Average_Emissions (MtCO₂e)', y='Average_Land_Temperature (celsius)', color='Year',
                           size='Average_Emissions (MtCO₂e)', hover_data=['Year', 'Average_Land_Temperature (celsius)', 'Average_Emissions (MtCO₂e)', 'Average_Sealevel (mm)']).update_layout(title=dict(text='Correlation between Average Land Temperature, Carbon Emissions and Sea level (1990-2020)', # set title
               xanchor='center', yanchor='top', x=0.5, y=0.95),xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False))
# fig_corr2.update_layout(
#     plot_bgcolor='#FFFFFF', # set plot area background color
#     paper_bgcolor='#88B0D7')

df_corr = pd.read_csv('avg_dataset.csv')

fig_corr_temp={
            'data': [
                {'x': df_corr['Year'], 'y': df_corr['Average_Land_Temperature (celsius)'], 'type': 'bar', 'name': 'Average Land Temperature', 'marker': {'color': 'green'}, "width": 0.5, },
                {'x': df_corr['Year'], 'y': df_corr['Average_LandOcean_Temperature (celsius)'], 'type': 'bar', 'name': 'Average Land and Ocean Temperature', 'marker': {'color': 'pink'}, "width": 0.5},
            ],
            'layout': {
                'title': 'Average Temperatures by Year',
                'xaxis': {'title': 'Year'},
                'yaxis': {'title': 'Temperature', 'range': [8, 17]},
                'bargroupgap': 2,
                'bargap': 2,
            }
        }

data_emissions = pd.read_csv('avg_dataset.csv')

# Create a stacked bar chart with Plotly
fig_emissions = px.bar(data_emissions, x='Year', y=['Average_Emissions (MtCO₂e)', 'Average_Land_Temperature (celsius)', 'Average_LandOcean_Temperature (celsius)'],
                      title='Greenhouse Emissions vs Temperature')

# Customize the layout
fig_emissions.update_layout(
    font_family='Arial',
    title_font_size=24,
    title_font_color='#404040',
    xaxis=dict(
        title='Year',
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1
    ),
    yaxis=dict(
        title='Carbon Emissions(MTCO2e)',
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1
    ),
    legend=dict(
        title='Variable',
        title_font_size=14,
        font_size=12,
        bgcolor='rgba(0,0,0,0)',
        yanchor='bottom',
        y=0.01,
        xanchor='right',
        x=1.4
    ),
    barmode='stack',
    plot_bgcolor='white',
    hoverlabel=dict(
        font_size=14,
        font_family='Arial',
        bgcolor='white',
        bordercolor='black'
    )
)

fig_emissions.update_traces(marker=dict(color='light green'))