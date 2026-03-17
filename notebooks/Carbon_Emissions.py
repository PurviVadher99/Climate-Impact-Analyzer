import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


data_carbon_scatter = pd.read_csv('historical_emissions.csv')

#barchart

data_carbon_bar = pd.read_csv('historical_emissions.csv')

# sort the data by CO2 emissions
data_carbon_bar_sorted = data_carbon_bar.sort_values(by='CO2 Emissions', ascending=False)

top5 = data_carbon_bar.groupby('Country')['CO2 Emissions'].sum().nlargest(5).reset_index()
top5_df = data_carbon_bar.loc[data_carbon_bar['Country'].isin(top5['Country'])]

bottom5 = data_carbon_bar.groupby('Country')['CO2 Emissions'].sum().nsmallest(5).reset_index()
bottom5_df = data_carbon_bar.loc[data_carbon_bar['Country'].isin(bottom5['Country'])]

# create the top 5 bar chart using plotly
fig_top_5 = px.bar(top5_df, x='Country', y='CO2 Emissions', color='CO2 Emissions', barmode='group',
                   labels={'Country': 'Country', 'CO2 Emissions': 'Carbon Emissions', 'Year': 'Year'},
                   title='Top 5 Carbon Emitting Countries', color_continuous_scale=px.colors.sequential.Viridis)

# increase the height of the figure
fig_top_5.update_layout(height=400)

# create the bottom 5 bar chart using plotly
fig_bottom_5 = px.bar(bottom5_df, x='Country', y='CO2 Emissions', color='CO2 Emissions', barmode='group',
                      labels={'Country': 'Country', 'CO2 Emissions': 'Carbon Emissions', 'Year': 'Year'},
                      title='Bottom 5 Carbon Emitting Countries', color_continuous_scale=px.colors.sequential.Viridis)

# increase the height of the figure
fig_bottom_5.update_layout(height=400)



#Line chart
data_carbon_line = pd.read_csv('historical_emissions.csv')

# filter the dataset to include only top 5 and bottom 5 countries based on CO2 emissions
top_5_countries = data_carbon_line.groupby('Country')['CO2 Emissions'].sum().nlargest(5).index
bottom_5_countries = data_carbon_line.groupby('Country')['CO2 Emissions'].sum().nsmallest(5).index
filtered_data_carbon_line = data_carbon_line[data_carbon_line['Country'].isin(top_5_countries) | data_carbon_line['Country'].isin(bottom_5_countries)]

# create the line chart for top 5 countries using plotly express
top_5_fig = px.line(filtered_data_carbon_line[filtered_data_carbon_line['Country'].isin(top_5_countries)], x="Year", y="CO2 Emissions", color="Country",
              title="Top 5 Carbon Emitting Countries")

# customize the layout of the top 5 line chart
top_5_fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Carbon Emissions",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    ))

top_5_fig.update_layout(height = 400)

# create the line chart for bottom 5 countries using plotly express
bottom_5_fig = px.line(filtered_data_carbon_line[filtered_data_carbon_line['Country'].isin(bottom_5_countries)], x="Year", y="CO2 Emissions", color="Country",
              title="Bottom 5 Carbon Emitting Countries")

# customize the layout of the bottom 5 line chart
bottom_5_fig.update_layout(
    xaxis_title="Year",
    yaxis_title="C02 Emissions",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    )
)
bottom_5_fig.update_layout(height = 400)



#HEAT MAP
data_heat_carbon = pd.read_csv('sorted_data_with_lat_lon.csv')

# Create heatmap using latitude and longitude values
fig_heat_carbon = px.density_mapbox(data_heat_carbon, 
                        lat='latitude', 
                        lon='longitude', 
                        z='CO2 Emissions',
                        hover_data=['Country', 'CO2 Emissions', 'Year'],
                         radius=20,
                         zoom=1,
                        mapbox_style="carto-positron",
                        animation_frame='Year',
                        opacity=0.9,
                        title='Average Temperature Heatmap by Country',
                        color_continuous_scale=px.colors.sequential.Plasma,)
fig_heat_carbon.update_layout(
    updatemenus=[dict(
        type='buttons',
      
        buttons=list([
            dict(
                label='Play',
                method='animate',
                args=[None, {'frame': {'duration': 500, 'redraw': True},
                             'fromcurrent': True, 'transition': {'duration': 0}}]
            ),
            dict(
                label='Pause',
                method='animate',
                args=[[None], {'frame': {'duration': 0, 'redraw': False},
                               'mode': 'immediate',
                               'transition': {'duration': 0}}]
            )
        ]),
        direction='left',
        pad={'r': 10, 't': 10},
        x=0.1,
        y=0,
        showactive=True,
        active=0
    )])



race = pd.read_csv('historical_emissions.csv')

# Filter data to years 1990 to 2018
race = race[race['Year'].between(1990, 2018)]

# Calculate total CO2 emissions for each country and year
df_total = race.groupby(['Country', 'Year'])['CO2 Emissions'].sum().reset_index()

# Get top 10 emitting countries for each year
top10_countries = df_total.groupby('Year').apply(lambda x: x.nlargest(10, 'CO2 Emissions')).reset_index(drop=True)

# Add a rank column for each year
top10_countries['Rank'] = top10_countries.groupby('Year')['CO2 Emissions'].rank(ascending=False)

# Add a color column based on the country
top10_countries['Color'] = pd.factorize(top10_countries['Country'])[0]

# Create animation frames
frames = []
for year in top10_countries['Year'].unique():
    df_year = top10_countries[top10_countries['Year'] == year]
    frame = go.Frame(data=[go.Bar(
        x=df_year['Country'],
        y=df_year['CO2 Emissions'],
        text=df_year['CO2 Emissions'].apply(lambda x: '{:.1f}'.format(x)),
        textposition='auto',
        marker_color=df_year['Color'],
        hovertemplate='%{y:.2f} MT CO2<extra></extra>',
    )])
    frames.append(frame)

# Set layout and add animation frames to the figure
# Set layout and add animation frames to the figure

fig_race = go.Figure(
    data=[go.Bar(        x=top10_countries[top10_countries['Rank'] == 1]['Country'],
        y=top10_countries[top10_countries['Rank'] == 1]['CO2 Emissions'],
        text=top10_countries[top10_countries['Rank'] == 1]['CO2 Emissions'].apply(lambda x: '{:.1f}'.format(x)),
        textposition='auto',
        marker_color=top10_countries[top10_countries['Rank'] == 1]['Color'],
        hovertemplate='%{y:.2f} MT CO2<extra></extra>',
    )],
    layout=go.Layout(
        title='Top 10 Carbon Emitting Countries in 1990',
        xaxis=dict(title='Country'),
        yaxis=dict(title='Carbon Emissions'),
        
        title_font=dict(color='black')
    ),
    frames=frames,
)

#bubble map
df_bb = pd.read_csv('historical_emissions.csv')

# Filter data to years 1990 to 2018
df_bb = df_bb[df_bb['Year'].between(1990, 2018)]

# Calculate total CO2 emissions for each country and year
df_total1 = df_bb.groupby(['Country', 'Year'])['CO2 Emissions'].sum().reset_index()

# Create a dictionary to map countries to regions
country_to_region = {
    'United States': 'North America',
    'China': 'Asia',
    'European Union (28)': 'Europe',
    'India': 'Asia',
    'Russia': 'Europe',
    'Japan': 'Asia',
    'Germany': 'Europe',
    'South Korea': 'Asia',
    'Iran': 'Middle East',
    'Canada': 'North America',
    'Saudi Arabia': 'Middle East',
    'Brazil': 'South America',
    'Indonesia':'Asia'
}

# Map countries to regions
df_total1['Region'] = df_total1['Country'].map(country_to_region)

# Create a figure using Gapminder API
fig_bb = px.scatter(df_total1, x='CO2 Emissions', y='Year', size='CO2 Emissions',
                 color='Region', log_x=True, range_x=[100, 15000],range_y=[1990,2018],
                 hover_name='Country', animation_frame='Year',
                 title='Country-Wise Carbon Emissions Over the Years')

# Update the layout
fig_bb.update_layout(
    xaxis_title='Aggregate CO2 Emissions (Metric Tons)',
    yaxis_title='Year',
    legend_title='Region',
    font=dict(size=12)
)

#choropleth map


data_carbon_choro = pd.read_csv("historical_emissions.csv")
# Sort the DataFrame by ascending year
data_carbon_choro = data_carbon_choro.sort_values(by="Year", ascending=True)

# Create a dropdown menu to select the year
year_options = [{"label": year, "value": year} for year in data_carbon_choro.columns[1:]]

# Create a choropleth map visualization
fig_carbon_choro = px.choropleth(
                    data_carbon_choro, 
                    locations="Country", 
                    locationmode="country names", 
                    color="CO2 Emissions", 
                    animation_frame="Year", 
                    range_color=[0, 1000],
                    title="Country-Wise Average Carbon Emissions",
                    color_continuous_scale=[
                        (0.0, "blue"),  # Low values
                        (0.5, "yellow"),  # Medium values
                        (1.0, "red")  # High values
                    ]
                   )

# Add the year selection dropdown to the map
fig_carbon_choro.update_layout(updatemenus=[{"type": "buttons",
                                "buttons": [{"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]},
                                            {"label": "Pause", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]}]}],
                  sliders=[{"active": 0, "steps": [{"label": str(year), "method": "animate", "args": [[year], {"frame": {"duration": 0, "redraw": True}, "transition": {"duration": 0}}]} for year in sorted(data_carbon_choro.columns[1:1],reverse = False)]}])








