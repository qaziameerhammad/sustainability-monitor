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


# In[2]:


df_bg = pd.read_csv("D:/Personal/class/__Masters/6th semester/HIS Project/csv/bigrams_clean.csv")

df_bg.rename(columns={'variable': 'Bigram'}, inplace=True)

df_bg = df_bg.sort_values(by=["year"], ascending= False)

# df_bg = df_bg.sort_values(by=["company_name", "year"], ascending= [True, False])

# df1 = df1.sort_values(by=["Company Name", "year"], ascending=[True, False])

df_bg


# In[3]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# indicators = ['employees','fines_spending','employee_turnover', 'female_pct', 'female_mgmt_pct','employee_tenure','employee_parental_pct',
#              'employee_under30_pct','employee_over50_pct']




app.layout = html.Div([
    html.H1("Firm Textual Analysis", style={"textAlign":"center"}),
    html.Hr(),
    
    html.Div([
    html.Div('In this dashboard, you can visualize the most frequent bigrams (sequences of two words) for selected firms.',
             style={'color': 'black', 'fontSize': 18}),
        html.Div('Use the dropdown menus to select the year and firm you would like to visualize.',
             style={'color': 'black', 'fontSize': 18}),
    ], style={'marginBottom': 50, 'marginTop': 25,'marginLeft': 15}),
    
    html.P("Choose Year:"),
    html.Div(html.Div([
        dcc.Dropdown(id='year', clearable=True,
                     value="",
                     options=[{'label': x, 'value': x} for x in
                              df_bg["year"].unique()]),
    ],className="two columns"),className="row"),
    
    html.P("Select Firms"),
    html.Div(html.Div([
        dcc.Dropdown(id='company_name', clearable=False,
                     value="",
                     options=[{'label': x, 'value': x} for x in
                              df_bg["company_name"].unique()],style={'width': '100%'}),
    ],className="three columns"),className="row"),
    
    html.Div(id="output-div", children=[]),
    

    
    
])




# In[ ]:


@app.callback(Output(component_id="output-div", component_property="children"),
              
              Input(component_id="year", component_property="value"),
              Input(component_id="company_name", component_property="value"),
              #Input(component_id="indi_list", component_property="value")
              
               
)






def make_graphs(selected_year, selected_firms):
    
    
    
    #graph1
    df_year = df_bg[df_bg["year"]==selected_year]
    df_year1 =  df_year[df_year["company_name"]==selected_firms]
    
     # Bar chart
    
    bar_chart = px.bar(df_year1, x ="Bigram" , y ="word_freq", color= "Bigram",
                      )
    
    bar_chart.update_layout(
                            title=f"Top 5 Most Frequent Bigrams for {selected_firms} in {selected_year} ",
                            title_x = 0.5,
                            xaxis_title="Bigram Words",
                            yaxis_title="Word Frequencies",
#                             xaxis_visible=False,
                            font=dict(
                            family="Arial",
                            size=15,
                            color="RebeccaPurple",
                            )
    )
    
    

    
    
    
    return [
        
         
        html.Div([
            html.Div([dcc.Graph(figure=bar_chart)], className="ten columns"),
        ], className="row"),
        

       
        
    ]


    
    
    
    


if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




