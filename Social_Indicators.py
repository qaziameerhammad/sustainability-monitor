#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash                     # pip install dash
from dash.dependencies import Input, Output, State
from dash import dcc
import plotly

import numpy as np

import plotly.graph_objs as go
import plotly.express as px

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#import cufflinks as cf

#import dash_html_components as html
from dash import html
import plotly.express as px     # pip install plotly==5.2.2

import pandas as pd
import matplotlib.pyplot as plt

import plotly.graph_objects as go


# In[2]:


df1 = pd.read_csv("D:/Personal/class/__Masters/6th semester/HIS Project/csv/Final_indicators.csv")

df1.rename(columns={'name': 'Firm Name','energy_cons': 'Energy Consumption(GJ)','employees': 'Total Number of Employees','waste': 'Waste Produced(XXX)',
                    'waste_recycled': 'Waste Recycled',
                   'water_cons': 'Water Consumption(cubic meter)','waste_water':'Water Wastage(M^3)','renewable_energy_pct':
                   'Renewable Energy','fuel_fleet':'Fuel Fleet(PJ)','contrib_political':'Political Contribution(in €)',
                   'waste_recycled_pct':'Waste Recycled Percentage',' legal_spending':
                   'Legal Spending(in €)','fines_spending':'Fine Spending(in €)','employee_turnover':'Employee Turnover(%)',
                   'female_pct' :'Total share of Female Employees','female_mgmt_pct':'Share of Female Employees in Management',
                   'employee_parental_pct':'Employee Parental Percentage','employee_tenure':'Employee Tenure',
                   'employee_under30_pct':'Share of Employees Under 30 Years Old',
                   'employee_over50_pct':'Share of Employees Over 50 Years Old',
                   'training_spending':'Training spending(in €)'}, inplace=True)

# df1.rename(columns={'employees': 'Total Number of Employees', 'employee_parental_pct':'Employee Parental Percentage',
#                     'employee_tenure':'Employee Tenure',
#                    'employee_under30_pct':'Share of Employees Under 30 Years Old ',
#                    'employee_over50_pct':'Share of Employees Over 50 Years Old'}, inplace=True)

# df1 = df1.sort_values(by=["Company Name", "year"], ascending=[True, False])

df1 = df1.sort_values(by=["year"], ascending= False)

df1
# type(df1["name"])

# df1 = df1.groupby('name')

# print(df1.dtypes)


# In[3]:


# name_list = df1["name"].unique()
# name_list


# In[4]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# indicators = ['employees','fines_spending','employee_turnover', 'female_pct', 'female_mgmt_pct','employee_tenure','employee_parental_pct',
#              'employee_under30_pct','employee_over50_pct']




app.layout = html.Div([
    html.H1("Firm Social Analysis", style={"textAlign":"center"}),
    html.Hr(),
    
    html.Div([
    html.Div('In this dashboard, you can visualize social indicators for selected firms.',
             style={'color': 'black', 'fontSize': 18}),
        html.Div('Use the dropdown menus to select the year and the firms you would like to visualize.',
             style={'color': 'black', 'fontSize': 18}),
    ], style={'marginBottom': 50, 'marginTop': 25,'marginLeft': 15}),
    
    html.P("Choose Year:"),
    html.Div(html.Div([
        dcc.Dropdown(id='year-value', clearable=True,
                     value="",
                     options=[{'label': x, 'value': x} for x in
                              df1["year"].unique()]),
    ],className="two columns"),className="row"),
    
    html.P("Select Firms"),
    html.Div(html.Div([
        dcc.Dropdown(id='firm_name', clearable=False,
                     value="",
                     options=[{'label': x, 'value': x} for x in
                              df1["Firm Name"].unique()],multi=True,style={'width': '100%'}),
    ],className="four columns"),className="row"),
    
    html.Div(id="output-div", children=[]),
    

    
    
])


# In[ ]:


@app.callback(Output(component_id="output-div", component_property="children"),
              
              Input(component_id="year-value", component_property="value"),
              Input(component_id="firm_name", component_property="value"),
              #Input(component_id="indi_list", component_property="value")
              
               
)



def make_graphs(selected_year, selected_firms):
    
    
    
    #graph1
    df_year = df1[df1["year"]==selected_year]
    df_year2 =  df_year[df_year["Firm Name"].isin(selected_firms)]

    
    print(df_year2)
    
     # Bar chart 1
    
    bar_chart1 = px.bar(df_year2, x =selected_firms , y ='Total Number of Employees'
                        
                        )
    bar_chart1.update_layout(
                            title = "Total Employees by Firm",
                            title_x = 0.25,
                            xaxis_title="Firm Name",
#                             xaxis_visible=False,
                            font=dict(
                            family="Arial",
                            size=15,
                            color="RebeccaPurple",
                            )
    
    )
#     go.FigureWidget(bar_chart1.update_layout)
    

    # Bar chart 2
    
    bar_chart2 = px.bar(df_year2, x =selected_firms, y ='Total share of Female Employees'
                        
                        )
    
    bar_chart2.update_layout(
                            title = "Female Employees (percentage)",
                            title_x = 0.25,
                            xaxis_title="Firm Name",
#                             xaxis_visible=False,
                            font=dict(
                            family="Arial",
                            size=15,
                            color="RebeccaPurple",
                            )
    
    )



    # Bar chart 3
    
    bar_chart3 = px.bar(df_year2, x = selected_firms, y ='Share of Female Employees in Management'
                       
                        )
    
    bar_chart3.update_layout(
                            title = 'Female Employees in Management (percentage)',
                            title_x = 0.25,
                            xaxis_title="Firm Name",
#                             xaxis_visible=False,
                            font=dict(
                            family="Arial",
                            size=15,
                            color="RebeccaPurple",
                            )
    
    )
    
    
    # Bar chart 4
    
    bar_chart4 = px.bar(df_year2, x =selected_firms, y ='Share of Employees Under 30 Years Old'
                        
                        )
    
    bar_chart4.update_layout(
                            title = "Employees Under 30 Years Old (percentage)",
                            title_x = 0.25,
                            xaxis_title="Firm Name",
#                             xaxis_visible=False,
                            font=dict(
                            family="Arial",
                            size=15,
                            color="RebeccaPurple",
                            )
    
    )
    
    # Bar chart 5
    
    bar_chart5 = px.bar(df_year2, x =selected_firms, y ='Share of Employees Over 50 Years Old'
                        
                        )
    
    
    
    
    bar_chart5.update_layout(
                            title = "Employees Over 50 Years Old (percentage)",
                            title_x = 0.25,
                            xaxis_title="Firm Name",
#                             xaxis_visible=False,
                            font=dict(
                            family="Arial",
                            size=15,
                            color="RebeccaPurple",
                            )
    
    )
    
    
    
   
    

    
    
    
    return [
        
         
        html.Div([
            html.Div([dcc.Graph(figure=bar_chart1)], className="six columns"),
            html.Div([dcc.Graph(figure=bar_chart2)], className="six columns"),
        ], className="row"),
        
        
        html.Div([
            html.Div([dcc.Graph(figure=bar_chart3)], className="six columns"),
            html.Div([dcc.Graph(figure=bar_chart4)], className="six columns"),
        ], className="row"),
        
        
        html.Div([
            html.Div([dcc.Graph(figure=bar_chart5)], className="six columns"),
        ], className="row")
        

        

       
        
    ]
    
    
    
    


if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




