import dash
from dash import dcc
from dash import html
from matplotlib import pyplot as plt
import plotly.express as px
import pandas as pd
import pathlib
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()



df = pd.read_csv(DATA_PATH.joinpath("data2.csv"))
# df2 = df.copy()

female=df.loc[df['sex']=='Female']
female_values=female.target.value_counts()
male=df.loc[df['sex']=='Male']
male_values=male.target.value_counts()
target=['No Disease','Disease']

y=df.target.value_counts()
x=['Disease','No Disease']

labels = ['YES','NO']
value = df['target'].value_counts().values

def create_dash_application(flask_app):


    
    # card 1
    fig = px.histogram(df, x='age',color_discrete_sequence=['coral'])
    fig.update_xaxes(title_text='Age')
    fig.update_yaxes(title_text='Number of Individuals')
    fig.update_layout(title_text='Distribution of Age')

    # card 2
    fig1 = go.Figure(data=[
    go.Bar(name='female', x=female_values.index, y=female_values, text=female_values, textposition='auto'),
    go.Bar(name='male', x=male_values.index, y=male_values, text=male_values, textposition='auto'),
])
    fig1.update_xaxes(title_text='Heart Disease')
    fig1.update_yaxes(title_text='Number of Individuals')
    fig1.update_layout(title_text='Gender Distribution')
    fig1.update_layout(barmode='group')


    # card 4
    fig3 = px.line(df['cp'].value_counts(),labels={
                     "variable": "Chest Pain",
                 }, color_discrete_sequence=['coral'])

    fig3.update_xaxes(title_text='Chest Pain Types')
    fig3.update_yaxes(title_text='Number of Individuals')
    fig3.update_layout(title_text='Distribution of Chest Pain Types')

    # card 3
    fig4 = go.Figure(data=[go.Pie(labels=x, values=y,  hole=.3)],
    layout=go.Layout(title=go.layout.Title(text='Heart Disease')))

    # card 5
    fig5 = px.histogram(df, x='thalach',color_discrete_sequence=['coral'])
    fig5.update_xaxes(title_text='Cholesterol Levels')
    fig5.update_yaxes(title_text='Number of Individuals')
    fig5.update_layout(title_text='Distribution of Cholesterol Levels')


    

    dash_app = dash.Dash(server=flask_app, external_stylesheets=[dbc.themes.BOOTSTRAP], name="Dashboard", url_base_pathname="/dash/")
    navbar = dbc.NavbarSimple(
    brand="HEART DISEASE DATA VISUALIZATIONS",
    brand_href="/dash",
    color="danger",
    dark=True,
)

    dash_app.layout = html.Div([dcc.Location(id="url"), navbar,
    dbc.Card(
        dbc.CardBody([
 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='example-graph1',figure=fig)
                ], width=5),
                dbc.Col([
                    dcc.Graph(id='example-graph2',figure=fig1)
                ], width=3),
                dbc.Col([
                    dcc.Graph(id='example-graph3',figure=fig4)
                ], width=4),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='example-graph4',figure=fig3)
                ], width=7),
                dbc.Col([
                    dcc.Graph(id='example-graph5',figure=fig5)
                ], width=4),
            ], align='center'),      
        ]), color = 'light'
    )
])

    return dash_app
    







# dbc.CardGroup(
#     [
#     html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(dbc.Card(dcc.Graph(id='example-graph',figure=fig))),
#                 dbc.Col(dbc.Card(dcc.Graph(id='example-graph1',figure=fig1))),
#                 dbc.Col(dbc.Card(dcc.Graph(id='example-graph2',figure=fig4))),
#             ],
#             className="align-self-center",
#         ),
#         dbc.Row(
#             [
#                 dbc.Col(dbc.Card(dcc.Graph(id='example-graph3',figure=fig3))),
#                 dbc.Col(dbc.Card(dcc.Graph(id='example-graph4',figure=fig2))),
#                 dbc.Col(dbc.Card(dcc.Graph(id='example-graph5',figure=fig5))),
#             ],
#             className="mb-4",

#         ),

#     ]
# )
#    ]
# )



































#dash_app.layout = html.Div([
#     html.H1('General Product Sales', style={"textAlign": "center"}),

#     html.Div([
#         html.Div([
#             html.Pre(children="Payment type", style={"fontSize":"150%"}),
#             dcc.Dropdown(
#                 id='pymnt-dropdown', value='DEBIT', clearable=False,
#                 persistence=True, persistence_type='session',
#                 options=[{'label': x, 'value': x} for x in sorted(dfg["Type"].unique())]
#             )
#         ], className='six columns'),

#         html.Div([
#             html.Pre(children="Country of destination", style={"fontSize": "150%"}),
#             dcc.Dropdown(
#                 id='country-dropdown', value='India', clearable=False,
#                 persistence=True, persistence_type='local',
#                 options=[{'label': x, 'value': x} for x in sorted(dfg["Order Country"].unique())]
#             )
#             ], className='six columns'),
#     ], className='row'),

#     dcc.Graph(id='my-map', figure={}),
# ])


# @app.callback(
#     Output(component_id='my-map', component_property='figure'),
#     [Input(component_id='pymnt-dropdown', component_property='value'),
#      Input(component_id='country-dropdown', component_property='value')]
# )
# def display_value(pymnt_chosen, country_chosen):
#     dfg_fltrd = dfg[(dfg['Order Country'] == country_chosen) &
#                     (dfg["Type"] == pymnt_chosen)]
#     dfg_fltrd = dfg_fltrd.groupby(["Customer State"])[['Sales']].sum()
#     dfg_fltrd.reset_index(inplace=True)
#     fig = px.choropleth(dfg_fltrd, locations="Customer State",
#                         locationmode="USA-states", color="Sales",
#                         scope="usa")
#     return fig