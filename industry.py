# import pandas as pd
import dash
import plotly.express as px


#import dash_html_components as html
from dash import html, dcc, callback, Input, Output
import plotly.express as px     # pip install plotly==5.2.2

import pandas as pd

import requests
import io


df1 = pd.read_csv("Group2Data.csv")

df1.rename(columns={'scope_3': 'Scope 3(Emissions in Tons)','scope_2': 'Scope 2(Emissions in Tons)','scope_1':
                    'Scope 1(Emissions in Tons)','year': 'Years','energy_cons': 'Energy Consumption(GJ)','employees':
                    'Total Number of Employees','waste': 'Waste',
                    'waste_recycled': 'Waste Recycled',
                   'water_cons': 'Water Consumption(cubic meter)','waste_water':'Water Wastage(M^3)','renewable_energy_pct':
                   'Renewable Energy','fuel_fleet':'Fuel Fleet(PJ)','contrib_political':'Political Contribution(in €)',
                   'waste_recycled_pct':'Waste Recycled Percentage',' legal_spending':
                   'Legal Spending(in €)','fines_spending':'Fine Spending(in €)','employee_turnover':'Employee Turnover',
                   'female_pct' :'Total Share of Female Employees','female_mgmt_pct':'Share of Female Employees in Management',
                   'employee_parental_pct':'Employee Parental Percentage','employee_tenure':'Employee Tenure',
                   'employee_under30_pct':'Share of Employees Under 30 Years Old',
                   'employee_over50_pct':'Share of Employees Over 50 Years Old',
                   'training_spending':'Training spending(in €)'}, inplace=True)


indicators = ['Total Number of Employees', 'Employee Turnover', 'Total Share of Female Employees',
              'Share of Female Employees in Management',
              'Share of Employees Under 30 Years Old', 'Share of Employees Over 50 Years Old',
              'Water Consumption(cubic meter)', 'Waste', 'Scope 1(Emissions in Tons)', 'Scope 2(Emissions in Tons)',
              'Scope 3(Emissions in Tons)']


layout = html.Div([
    html.H1("Industry Indicators Analysis",
            style={"textAlign": "center"}),
    html.Hr(),
    html.Div([
        html.Div('In this dashboard, you can visualize ESG indicators for selected industries.',
             style={'color': 'black', 'fontSize': 18}),
        html.Div('Use the dropdown menus to select industries and indicators you would like to visualize.',
                 style={'color': 'black', 'fontSize': 18}),
        html.Div('On the right-hand side of the graphs, click on the industry (firm) names to hide or unhide industries (firms) from the analysis and compare the results.',
                 style={'color': 'black', 'fontSize': 18}),
    ], style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 15}),

    html.H3("Analysis per Industry and Firms", style={"textAlign": "center"}),
    html.P("Select Industry"),
    html.Div(html.Div([
        dcc.Dropdown(id='indus_list', clearable=False,
                     value=["Health care"],
                     options=[{'label': x, 'value': x} for x in
                              df1["Industry"].unique()]
                     )
    ], className="three columns"), className="row"),

    html.P("Select Indicator"),
    html.Div(html.Div([
        dcc.Dropdown(id='indi_list', clearable=False,
                     value=["Total Number of Employees"],
                     options=[{'label': x, 'value': x} for x in
                              indicators]),
    ], className="three columns"), className="row"),

    html.Div(id="output-div-industry", children=[]),


    html.H3("Averages per Industry", style={"textAlign": "center"}),
    html.P("Select Industries"),
    html.Div(html.Div([
        dcc.Dropdown(id='indus_list2', clearable=False,
                     value=["Industrials"],
                     options=[{'label': x, 'value': x} for x in
                              df1["Industry"].unique()], multi=True),
    ], className="three columns"), className="row"),
    html.P("Select Indicator"),
    html.Div(html.Div([
        dcc.Dropdown(id='indi_list2', clearable=False,
                     value=["Total Number of Employees"],
                     options=[{'label': x, 'value': x} for x in
                              indicators]),
    ], className="three columns"), className="row"),
    html.Div(id="output-div-industry2", children=[])

])


@callback(Output(component_id="output-div-industry", component_property="children"),

              Input(component_id="indus_list", component_property="value"),
              Input(component_id="indi_list", component_property="value")
              )
def make_graphs(indus_list, ind_chosen):

    if indus_list and ind_chosen:
        #graph1
        df_ind = df1[df1["Industry"] == indus_list]

        # LINE CHART
        df_line = df_ind.sort_values(by=[ind_chosen], ascending=True)
        df_line = df_line.groupby(
            ["Years", "name", ind_chosen]).size().reset_index(name="count")
        #print(df_line.head())
        fig = px.line(df_line, x="Years", y=ind_chosen, color='name', markers=True)
        fig.update_xaxes(nticks=4)
        #fig.update_layout(xaxis_type='date')
        #fig.update_layout(autotypenumbers="strict")

        return [

            html.Div([
                html.Div([dcc.Graph(figure=fig)]),
            ], className="row"),

        ]



@callback(Output(component_id="output-div-industry2", component_property="children"),

              Input(component_id="indus_list2", component_property="value"),
              Input(component_id="indi_list2", component_property="value")
              )
def avg_graph(indus_list2, ind_chosen2):
    if indus_list2 and ind_chosen2:

        df_ind1 = df1[df1["Industry"].isin(indus_list2)]

        # LINE CHART
        meandf = df_ind1.groupby(['Industry', 'Years']).mean().reset_index()
        #print(df_line.head())
        fig2 = px.line(meandf, x="Years", y=ind_chosen2,
                    color='Industry', markers=True)
        fig2.update_xaxes(nticks=4)
        meandf1 = df1.groupby(['Industry']).mean().reset_index()
        fig2_1 = px.bar(meandf1, x="Industry", y=ind_chosen2,
                        color="Industry")

        return [

            html.Div([
                html.Div([dcc.Graph(figure=fig2)]),
            ], className="row"),
            html.Div([
                html.Div([dcc.Graph(figure=fig2_1)]),
            ], className="row"),

        ]
