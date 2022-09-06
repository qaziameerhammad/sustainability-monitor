import dash
import plotly.express as px
import pandas as pd
import requests
import io

from dash import html, dcc, callback, Input, Output
import plotly.express as px 

dash.register_page(__name__, path='/environment')
url = "Final_indicators.csv"
s = requests.get(url).content
df1 = pd.read_csv(io.StringIO(s.decode('utf-8')))


df1.rename(columns={'name': 'Firm Name','year': 'Years','scope_3': 'Scope 3 (Emissions in Tons)','scope_2': 'Scope 2 (Emissions in Tons)','scope_1':
                    'Scope 1 (Emissions in Tons)','energy_cons': 'Energy Consumption (GJ)','employees': 'Total Number of Employees','waste':
                    'Waste Produced(XXX)',
                    'waste_recycled': 'Waste Recycled',
                   'water_cons': 'Water Consumption (cubic meter)','waste_water':'Waste Water(M^3)','renewable_energy_pct':
                   'Renewable Energy','fuel_fleet':'Fuel Fleet(PJ)','contrib_political':'Political Contribution(in €)',
                   'waste_recycled_pct':'Waste Recycled Percentage',' legal_spending':
                   'Legal Spending(in €)','fines_spending':'Fine Spending(in €)','employee_turnover':'Employee Turnover(%)',
                   'female_pct' :'Total share of Female Employees','female_mgmt_pct':'Share of Female Employees in Management',
                   'employee_parental_pct':'Employee Parental Percentage','employee_tenure':'Employee Tenure',
                   'employee_under30_pct':'Share of Employees Under 30 Years Old',
                   'employee_over50_pct':'Share of Employees Over 50 Years Old',
                   'training_spending':'Training spending(in €)'}, inplace=True)

indicators = ['Water Consumption (cubic meter)','Energy Consumption (GJ)']
indicators_scope = ['Scope 1 (Emissions in Tons)','Scope 2 (Emissions in Tons)','Scope 3 (Emissions in Tons)']

layout = html.Div([
    html.H1("Firm Environmental Analysis", style={"textAlign": "center"}),
    html.Hr(),
    html.Div([
    html.Div('In this dashboard, you can visualize environmental indicators for selected firms.',
             style={'color': 'black', 'fontSize': 18}),
        html.Div('Use the dropdown menus to select the firms and indicators you would like to visualize.',
             style={'color': 'black', 'fontSize': 18}),
        html.Div('On the right-hand side of the graphs, click on the firm names to hide or unhide firms from the analysis and compare the results.',
             style={'color': 'black', 'fontSize': 18}),
    ], style={'marginBottom': 50, 'marginTop': 25,'marginLeft': 15}),
    html.H3("Analysis of Emissions per Firm", style={"textAlign": "center"}),
    html.P("Select Firms"),
    html.Div(html.Div([
        dcc.Dropdown(id='firm_list_environme', clearable=False,
                     value=["Fresenius"],
                     options=[{'label': x, 'value': x} for x in
                              df1["Firm Name"].unique()],multi=True),
                    
    ], className="three columns"), className="row"),
    
    html.P("Select Indicator"),
    html.Div(html.Div([
        dcc.Dropdown(id='indi_list_environment', clearable=False,
                 
                     options=[{'label': x, 'value': x} for x in
                              indicators_scope]),
    ],className="three columns"),className="row"),
    
    
    
    html.Div(id="output-div-environment", children=[]),
    
    html.Hr(),
   
    html.H3("Analysis of Other Environmental Indicators per Firm",
            style={"textAlign": "center"}),
    html.P("Select Firms"),
    
     html.Div(html.Div([
        dcc.Dropdown(id='firm_list_environme1', clearable=False,
                     value=["Fresenius"],
                     options=[{'label': x, 'value': x} for x in
                              df1["Firm Name"].unique()],multi=True),
         
                    
    ], className="three columns"), className="row"),
    html.P("Select Indicator"),
    html.Div(html.Div([
        dcc.Dropdown(id='indi_list_environment1', clearable=False,
                     value="employees",
                     options=[{'label': x, 'value': x} for x in
                              indicators]),
    ],className="three columns"),className="row"),
    
    
    
    html.Div(id="output-div2", children=[])
])


@callback(Output(component_id="output-div-environment", component_property="children"),
              
              Input(component_id="firm_list_environme", component_property="value"),
              Input(component_id="indi_list_environment", component_property="value")
                            
)


def make_graphs(firm_list_environme,ind_chosen):
    
    if firm_list_environme and ind_chosen:
        
       
        df_ind = df1[df1["Firm Name"].isin(firm_list_environme)]
        df_line = df_ind.sort_values(by=[ind_chosen], ascending=True)
        df_line = df_line.groupby(
            ["Years","Firm Name", ind_chosen]).size().reset_index(name="count")
        fig = px.line(df_line, x="Years", y=ind_chosen,color='Firm Name',markers=True)
        fig.update_xaxes(nticks=4)

        
        
        return [
            
            html.Div([
            html.Div([dcc.Graph(figure=fig)]),
            ], className="row"),
            
            ]
    
@callback(Output(component_id="output-div2", component_property="children"),
              
              Input(component_id="firm_list_environme1", component_property="value"),
              Input(component_id="indi_list_environment1", component_property="value")
               
)


def make_graphs(firm_list_environme1,ind_chosen1):
    if firm_list_environme1 and ind_chosen1:

        df_ind = df1[df1["Firm Name"].isin(firm_list_environme1)]
        df_line = df_ind.sort_values(by=[ind_chosen1], ascending=True)
        df_line = df_line.groupby(
            ["Years","Firm Name", ind_chosen1]).size().reset_index(name="count")
        fig1 = px.line(df_line, x="Years", y=ind_chosen1,color='Firm Name',markers=True)
        fig1.update_xaxes(nticks=4)

        
        return [
            
            html.Div([
            html.Div([dcc.Graph(figure=fig1)]),
            ], className="row"),
            
            ]
    
