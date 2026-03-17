#SeaLevel
# Create the bar chart
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
#1.Load DataSet
data = pd.read_csv('Global_sea_level_rise.csv')

# Create the bar chart
fig_bar = go.Figure(
    data=[go.Bar(x=data['Year'], y=data['Sea Level'],)],
    layout=go.Layout(
        title=go.layout.Title(text="Sea Level Variations Over Time", font=dict(size=24)),
        xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Year")),
        yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text="Sea Level-mm")),
    )
)


area_fig = px.area(data, x='Year', y='Sea Level', title='Area Chart',
              labels={'Year': 'Year', 'Sea Level': 'Sea Level-mm'},
              color_discrete_sequence=['#3D9970'])

# Add a gradient fill
area_fig.update_traces(mode='lines', fillcolor="red")

# Add a line color and shape
area_fig.update_traces(line_color='black', line_shape='spline', line_smoothing=1.3, line_width=3)

# Adjust the opacity
area_fig.update_traces(opacity=0.2)

# Customize the layout
area_fig.update_layout(
    font_family='Arial',
    title_font_size=24,
    title_font_color='#404040',
    xaxis=dict(
        title_font_size=24,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1,
        tickfont=dict(size=10)
    ),
    yaxis=dict(
        tickmode='linear',
        dtick=25,
        zeroline=True,
        zerolinecolor='lightgray',
        zerolinewidth=0.1,
        title_font_size=18,
        tickfont_size=14,
        showgrid=False,
        gridcolor='lightgray',
        gridwidth=0.01,
        tickfont=dict(size=10)
    ),
    legend=dict(
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
    ),
    dragmode='zoom',
    clickmode='event+select'
)

area_fig.update_traces(fillcolor='#ADD8E6')  # Light Blue

# Create a box and whiskers plot with Plotly
fig_box = go.Figure()

fig_box.add_trace(go.Box(
    y=data['Sea Level'],
    name='Sea Level',
    boxmean=True, # set boxmean to True to color the box
    fillcolor='#d9b3ff', # set fillcolor to change the color of the box
    marker=dict(
        color='blue'
    ),
    line=dict(
        color='#00004d'
    )
))

# Create a scatter plot with Plotly
scatter_fig = px.scatter(data, x='Year', y='Sea Level', title='Scatter Plot- Sea Level Changes Over Time',
                 labels={'Year': 'Year', 'Sea Level': 'Sea Level-mm'}, color_discrete_sequence=['#FF5733'])

# Customize the layout
scatter_fig.update_layout(
    font_family='Arial',
    title_font_size=24,
    title_font_color='#404040',
    xaxis=dict(
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1,
        tickfont=dict(size=10)
    ),
    yaxis=dict(
        zeroline=True,
        zerolinecolor='lightgray',
        zerolinewidth=0.1,
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.01,
        tickfont=dict(size=10)
    ),
    legend=dict(
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

# Customize the box plot layout
fig_box.update_layout(
    font_family='Arial',
    title="Box and Whiskers Plot",
    title_font_size=24,
    title_font_color='#404040',
    xaxis=dict(
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.1,
        tickfont=dict(size=10)
    ),
    yaxis=dict(
        tickmode='linear',
        dtick=25,
        zeroline=True,
        zerolinecolor='lightgray',
        zerolinewidth=0.1,
        title_font_size=18,
        tickfont_size=14,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=0.01,
        tickfont=dict(size=10)
    ),
    legend=dict(
        title_font_size=18,
        font_size=14,
        bgcolor='rgba(0,0,0,0)',
        yanchor='bottom',
        y=0.01,
        xanchor='left',
        x=0.01
    ),
    plot_bgcolor='#f7f7f7', # change plot background color
    hoverlabel=dict(
        font_size=16,
        font_family='Arial',
        bgcolor='white',
        bordercolor='black'
    ),

)
trace_markers = go.Scatter(x=data["Year"], y=data["Sea Level"], mode="markers", name="")
trace_lines = go.Scatter(x=data["Year"], y=data["Sea Level"], mode="lines",name="Lines", line=dict(width=3, color="blue"))
fig_line = go.Figure(data=[trace_markers, trace_lines])
fig_line.update_xaxes(range=[1950, max(data["Year"])],  zeroline=False,showgrid=False )
fig_line.update_yaxes( zeroline=False)
fig_line.update_layout(xaxis_title="Year", yaxis_title="Sea Level-mm", template="plotly_dark",title="Line Chart", title_font=dict(size=24))


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]