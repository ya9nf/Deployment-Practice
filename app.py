# %% [markdown]
# # Assignment 5 Callbacks
# ## Yasmin Azizi

# %% [markdown]
# Objective: Practice adding callbacks to Dash apps.
# 
# Task:
# (1) Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. 
# 
# TASK 1 is the same as ASSIGNMENT 4. You are welcome to update your code. 
# 
# UI Components:
# A dropdown menu that allows the user to select `country`
# - The dropdown should allow the user to select multiple countries
# - The options should populate from the dataset (not be hard-coded)
# A slider that allows the user to select `year`
# - The slider should allow the user to select a range of years
# - The range should be from the minimum year in the dataset to the maximum year in the dataset
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# - The graph should display the gdpPercap for each country as a line
# - Each country should have a unique color
# - The graph should have a title and axis labels in reader friendly format
# 
# 
# 
# 
# (2) Write Callback functions for the slider and dropdown to interact with the graph
# 
# This means that when a user updates a widget the graph should update accordingly.
# The widgets should be independent of each other. 
# 
# 
# Layout:
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# 
# Submission:
# - Deploy your app on Render. 
# - In Canvas, submit the URL to your public Github Repo (made specifically for this assignment)
# - The readme in your GitHub repo should contain the URL to your Render page. 
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**
# ​
# 

# %%
#import dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, dash_table, dcc, html, Input, Output, State # update to import


# %%
# read data
df = pd.read_csv('gdp_pcap.csv')

# %%
# use the melt function to change data from wide to long
m_df = df.melt(id_vars=['country'], var_name='year', value_name='gdp')
print(m_df)

# %%
# create a function to remove the k in the gdp column, convert to float and multiply by 1000
# had to do alot of experimenting here, as I kept on getting erros
def convert_to_float(value):
    letter_to_remove = 'k' # create variable
    if (type(value) == str) and letter_to_remove in value:
        my_string = str(value)
        new_string = ''.join(char for char in my_string if char != letter_to_remove)
        new_float = float(new_string)  # convert to float
        new_int = int(new_float)
        new_int *= 1000  # multiply by 1000
        return new_int
    else:
        return value
    

# %%
# apply function and check
m_df['gdp'] = m_df['gdp'].apply(convert_to_float)
print(m_df)

# %%
# change gdp to int
m_df['gdp'] = m_df['gdp'].astype(int)

# %%
# change year to int
m_df['year'] = m_df['year'].astype(int)

# %%
# check
m_df.dtypes

# %%
# Create app
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # Load the CSS stylesheet

app = Dash(__name__, external_stylesheets=stylesheets)

# Layout
app.layout = html.Div([
    html.H1("GDP per Country over 1800-2100", style={'textAlign': 'center', 'color': 'black'}), # Create header
    
    html.P("The data used in this app is sourced from gapminder. It showcases the GDP per capita for all countries from 1800 - 2040. The data is sourced from the World Bank from 1990-2017, estimated pre 1990, and forecasted post 2017.", 
           style={'textAlign': 'center', 'color': 'black'}), # Description with white font
    
    # Create description
    html.Div([
        dcc.Dropdown( 
            id='country',
            multi=True,
            options=[{"label": x, "value": x} for x in sorted(m_df['country'].unique())],
            value=[m_df['country'].unique()[0]],
            className='six columns'
        ),  # Dropdown for countries
        
        dcc.RangeSlider(
            id='year-slider',
            min=m_df['year'].min(),
            max=m_df['year'].max(),
            value=[m_df['year'].min(), m_df['year'].max()],
            marks={str(year): str(year) if year % 50 == 0 else '' for year in m_df['year'].unique()},
            step=None,
            tooltip={'always_visible': True},
            className='six columns'
        )
    ], className='row', style={'padding': 10}),
    
    dcc.Graph(id='graph', figure=px.line(m_df, x='year', y='gdp', color='country', title='GDP x Year')), # Plotly Express graph
], style={'padding': 20})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# %%
# Create app
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # Load the CSS stylesheet

app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

# Layout
app.layout = html.Div([
    html.H1("GDP per Country over 1800-2100", style={'textAlign': 'center', 'color': 'black'}), # Create header
    
    html.P("The data used in this app is sourced from gapminder. It showcases the GDP per capita for all countries from 1800 - 2040. The data is sourced from the World Bank from 1990-2017, estimated pre 1990, and forecasted post 2017.", 
           style={'textAlign': 'center', 'color': 'black'}), # Description with white font
    
    # Create description
    html.Div([
        dcc.Dropdown( 
            id='country',
            multi=True,
            options=[{"label": x, "value": x} for x in sorted(m_df['country'].unique())],
            value=[m_df['country'].unique()[0]],
            className='six columns'
        ),  # Dropdown for countries
        
        dcc.RangeSlider(
            id='year-slider',
            min=m_df['year'].min(),
            max=m_df['year'].max(),
            value=[m_df['year'].min(), m_df['year'].max()],
            marks={str(year): str(year) if year % 50 == 0 else '' for year in m_df['year'].unique()},
            step=None,
            tooltip={'always_visible': True},
            className='six columns'
        )
    ], className='row', style={'padding': 10}),
    
    dcc.Graph(id='graph', figure=px.line(m_df, x='year', y='gdp', color='country', title='GDP x Year')), # Plotly Express graph
], style={'padding': 20})

# Callback to update the graph
@app.callback(
    Output('graph', 'figure'),
    [Input('country', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_country, selected_years):
    filtered_df = m_df[(m_df['country'].isin(selected_country)) & 
                       (m_df['year'] >= selected_years[0]) & 
                       (m_df['year'] <= selected_years[1])]
    
    fig = px.line(filtered_df, x='year', y='gdp', color='country', title='GDP x Year')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



