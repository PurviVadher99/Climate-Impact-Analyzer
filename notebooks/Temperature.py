#TempFigures
# Import and Setup
import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend


# Setting default renderer for Plotly
pio.renderers.default = 'notebook'

#Loading JSON File
india_states = json.load(open("states_india.geojson", "r"))
us_states = json.load(open("us-states.json", "r"))
can_states = json.load(open("canada.geojson", "r"))
china_states = json.load(open("China_geo.json", "r", encoding="utf-8"))
rus_states = json.load(open("Russia_geo.json", "r"))
brz_states = json.load(open("brazil_geo.json", "r"))

#Mapping States to IDs
# Creating mappings for states to IDs

state_id_map1 = {}
state_id_map2 = {}
state_id_map3 = {}
state_id_map4 = {}
state_id_map5 = {}
state_id_map6 = {}

for feature in brz_states["features"]:
    feature["id"] = feature["id"]
    state_id_map1[feature["properties"]["name"]] = feature["id"]
for feature in rus_states["features"]:
    feature["id"] = feature["properties"]["ID_1"]
    state_id_map2[feature["properties"]["NAME_1"]] = feature["id"]
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map3[feature["properties"]["st_nm"]] = feature["id"]
for feature in china_states["features"]:
    feature["id"] = feature["properties"]["HASC_1"]
    state_id_map4[feature["properties"]["NAME_1"]] = feature["id"]
for feature in can_states["features"]:
    feature["id"] = feature["properties"]["cartodb_id"]
    state_id_map5[feature["properties"]["name"]] = feature["id"]
for feature in us_states["features"]:
    feature["id"] = feature["id"]
    state_id_map6[feature["properties"]["name"]] = feature["id"]

# Reading temperature data
df1 = pd.read_csv("India_temperatures.csv")
df1["id"] = df1["State"].apply(lambda x: state_id_map3[x])
df2 = pd.read_csv("China_temperatures.csv")
df2["id"] = df2["State"].apply(lambda x: state_id_map4[x])
df3 = pd.read_csv("Canada_temperatures.csv")
df3["id"] = df3["State"].apply(lambda x: state_id_map5[x])
df4 = pd.read_csv("Brazil_temperatures.csv")
df4["id"] = df4["State"].apply(lambda x: state_id_map1[x])
df5 = pd.read_csv("Updated_Russia_temperatures.csv")
df5["id"] = df5["State"].apply(lambda x: state_id_map2[x])
df6 = pd.read_csv("US_temperatures.csv")
df6["id"] = df6["State"].apply(lambda x: state_id_map6[x])

# Temperature maps
fig11 = px.choropleth_mapbox(
    df1,
    locations="id",
    geojson=india_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature INDIA",
    mapbox_style="carto-positron",
    center={"lat": 24, "lon": 78},
    zoom=3.7,
    opacity=0.3,
    width=1400,
    height=800,
)

fig21 = px.choropleth_mapbox(
    df2,
    locations="id",
    geojson=china_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature CHINA",
    mapbox_style="carto-positron",
    center={"lat": 37, "lon": 104},
    zoom=3,
    opacity=0.5,
    width=1400,
    height=800,
)

fig31 = px.choropleth_mapbox(
    df3,
    locations="id",
    geojson=can_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature CANADA",
    mapbox_style="carto-positron",
    center={"lat": 72, "lon": -99},
    zoom=1.9,
    opacity=0.5,
    width=1400,
    height=800,
)

fig41 = px.choropleth_mapbox(
    df4,
    locations="id",
    geojson=brz_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature BRAZIL",
    mapbox_style="carto-positron",
    center={"lat": -12, "lon": -56},
    zoom=3,
    opacity=0.5,
    width=1400,
    height=800,
)

fig51 = px.choropleth_mapbox(
    df5,
    locations="id",
    geojson=rus_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature RUSSIA",
    mapbox_style="carto-positron",
    center={"lat": 68, "lon": 101},
    zoom=2.1,
    opacity=0.5,
    width=1400,
    height=800,
)

fig61 = px.choropleth_mapbox(
    df6,
    locations="id",
    geojson=us_states,
    color="AverageTemperature",
    color_continuous_scale='Turbo',
    hover_name="State",
    hover_data=["AverageTemperature"],
    title="Average Temperature USA",
    mapbox_style="carto-positron",
    center={"lat": 53, "lon": -113},
    zoom=2.3,
    opacity=0.5,
    width=1400,
    height=800,
)

# Create Heatmap
data_heatmap = pd.read_csv('UpdatedMajorCity_Temperatures.csv')
fig_heat = px.density_mapbox(
    data_heatmap, 
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
fig_heat.update_layout(
    updatemenus=[dict(
        type='buttons',
        buttons=list([
            dict(
                label='Play',
                method='animate',
                args=[None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 0}}]
            ),
            dict(
                label='Pause',
                method='animate',
                args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]
            )
        ]),
        direction='left',
        pad={'r': 10, 't': 10},
        x=0.1,
        y=0,
        showactive=True,
        active=0
    )]
)

# Timeline Chart for Earth Temperature
data_timeline = pd.read_csv('avg_dataset.csv')
fig_timeline = px.line(data_timeline, x='Year', y='Average_Land_Temperature (celsius)', title='Earth Temperature Timeline')
fig_timeline.update_layout(
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
        title='Average Temperature (°C)',
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1
    ),
    legend=dict(
        title='Country',
        title_font_size=18,
        font_size=14,
        bgcolor='rgba(0,0,0,0)',
        yanchor='bottom',
        y=0.01,
        xanchor='left',
        x=0.01
    ),
    plot_bgcolor='white',
    hoverlabel=dict(
        font_size=16,
        font_family='Arial',
        bgcolor='white',
        bordercolor='black'
    )
)


# Natural disasters and temp
# Load datasets
df_temp = pd.read_csv('Climate_Change_Indicators.csv')
df_global_temp = pd.read_csv('Global Surface Temperature.csv')
df_disasters = pd.read_csv('Climate_related_Disasters_Frequency.csv')
df_economic_damage = pd.read_csv('Econ_Damage-from-Disasters.csv')
# Load another dataset for further analysis
fig_CC = pd.read_csv("city_temp.csv")

with open('countries.geo.json') as f:
    world_json = json.load(f)

# Climate Change Indicators
year_list = [f"F{i}" for i in range(1963, 2023)]
df_melt = pd.melt(df_temp, id_vars=["Country"], value_vars=year_list)
df_melt.rename(columns={"variable": "Year", "value": "Temperature_Change"}, inplace=True)
df_melt['Year'] = df_melt['Year'].str.replace('F', '').astype(int)

df_disasters = df_disasters.pivot(index='Year', columns='Entity', values='Number of reported natural disasters (reported disasters)').fillna(0)
df_economic_damage = df_economic_damage.pivot(index='Year', columns='Entity', values='Total economic damage from natural disasters (US$)').fillna(0)
mean_temp_change_by_year = df_melt.groupby("Year").agg({"Temperature_Change": "mean"}).reset_index()
combined_df = df_global_temp.set_index('Year').join([df_disasters, df_economic_damage], how='inner')


#----------1.NaturalDisaster------------

# Load the data (use your data loading code here)
orig_disaster_data = pd.read_csv('Climate_related_Disasters_Frequency.csv')
nat_disaster_df = orig_disaster_data.copy()

nat_disaster_df.drop(['Code'], axis=1, inplace=True)

nat_disaster_df = nat_disaster_df.pivot(
    index='Year', 
    columns='Entity', 
    values='Number of reported natural disasters (reported disasters)'
)

nat_disaster_df.drop(['Impact'], axis=1, inplace=True)
nat_disaster_df.fillna(value=0, inplace=True)
nat_disaster_df = nat_disaster_df.add_suffix(' (Occurrence)')

# Filter data for the chart (1980 onwards)
filtered_df = nat_disaster_df.loc[1980:].drop(['All natural disasters (Occurrence)'], axis=1)

# Convert DataFrame to Plotly format
filtered_df.reset_index(inplace=True)
melted_df = filtered_df.melt(id_vars=['Year'], var_name='Disaster Type', value_name='Occurrences')


#----------Temperature Anomalies------------

# Load and process the global temperature dataset
orig_temp_data = pd.read_csv('Global Surface Temperature.csv')

# Preprocess the data
global_temp_df = orig_temp_data[['Date', 'OceanAverageTemperature']].copy()
global_temp_df['Date'] = pd.to_datetime(global_temp_df['Date'], format='%m/%d/%Y', errors='coerce')
global_temp_df.set_index('Date', inplace=True)
global_temp_df.sort_index(axis=0, inplace=True)

# Resample by year to calculate the annual average temperature
global_temp_df = global_temp_df.resample('A').mean()
global_temp_df.rename(columns={'OceanAverageTemperature': 'AnnualAverageTemp'}, inplace=True)
global_temp_df.index.rename('Year', inplace=True)
global_temp_df.index = global_temp_df.index.year

# Drop rows with missing values
global_temp_df.dropna(inplace=True)

# Calculate the global baseline temperature
global_ref_temp = global_temp_df.loc[1951:2024].mean()['AnnualAverageTemp']

# Create a temperature anomaly column
global_temp_df['Temperature Anomaly'] = global_temp_df['AnnualAverageTemp'] - global_ref_temp
global_temp_df.drop(['AnnualAverageTemp'], axis=1, inplace=True)