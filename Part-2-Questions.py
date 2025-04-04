#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"
app.title="Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value':'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Statistics Dashboard"),

    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value=None,
            placeholder='Select a report type'
        )
    ]),

    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': str(i)} for i in year_list],
            value=None,
            placeholder='Select a year',
            disabled=True
        )
    ])
])
html.Div([
    html.Div(
        id='output-container',
        className='chart-grid',
        style={'display': 'flex'}
    )
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output('select-year', 'disabled'), 
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
       recession_data = data[data['Recession'] == 1]

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
        
#TASK 2.5: Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
       yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
       R_chart1 = dcc.Graph(figure=pxline(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        
        # use groupby to create relevant data for plotting
        #Hint:Use Vehicle_Type and Automobile_Sales columns
       average_sales = recession_data.groupby('Vehicle_Type') ['Automobile_Sales'].mean().reset_index()      
       R_chart2  = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Vehicle Sales for Each Vehicle Category"))
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # grouping data for plotting
	# Hint:Use Vehicle_Type and Advertising_Expenditure columns
       exp_rec= recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
       R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values="Advertising_Expenditure", names="Vehicle_Type",title="Total Advertising Expenditure Share of Vehicle Type During Recession"
))

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        #grouping data for plotting
	# Hint:Use unemployment_rate,Vehicle_Type and Automobile_Sales columns
       unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type', 'Automobile_Sales']).mean().reset_index()
       R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'}, title='Effect of Unemployment Rate on Vehicle Type and Sales'))


       return [
             html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart3)],style={'display': 'flex'})
            ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots
    # Check for Yearly Statistics.                             
    elif (input_year and selected_statistics == 'Yearly Statistics'):
       yearly_data = data[data['Year'] == input_year]
                              
#plot 1 Yearly Automobile sales using line chart for the whole period.
        # grouping data for plotting.
        # Hint:Use the columns Year and Automobile_Sales.
       yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
       Y_chart1 = dcc.Graph(figure=px.line(yas,x='Year', y='Automobile_Sales', title="Yearly Average Automobile Sales"))
            
# Plot 2 Total Monthly Automobile sales using line chart.
        # grouping data for plotting.
	# Hint:Use the columns Month and Automobile_Sales.
       mas=yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
       Y_chart2 = dcc.Graph(figure=px.line(yearly_data, x='Month',y='Automobile_Sales', title=f" Monthly Automobile Sales for the year {input_year}"))

  # Plot bar chart for average number of vehicles sold during the given year
         # grouping data for plotting.
         # Hint:Use the columns Year and Automobile_Sales
       avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
       Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type' ,y='Automobile_Sales', title=f'Average Vehicles Sold by Vehicle Type in the year{input_year}'))

    # Total Advertisement Expenditure for each vehicle using pie chart
         # grouping data for plotting.
         # Hint:Use the columns Vehicle_Type and Advertising_Expenditure
       exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
       Y_chart4 = dcc.Graph(figure=px.pie(exp_data,values='Advertising_Expenditure', names='Vehicle_Type', title=f'Total Advertising Expenditure for Vehicle Type in the year {input_year}'))

#TASK 2.6: Returning the graphs for displaying Yearly data
       return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display':'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
        ]
        
    return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=8060)


