import pandas
import Probability_sesonal_pattern as probanility
import Cumulative_Sesonal_pattern as cumulative
import dash
from dash import dcc
from dash import html
from  dash import Input
from dash import Output
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import data_managment_functions as data_managment
import searhbestopportunity
import Wykresy_histogramy
from datetime import date
from slownik_dni import s_dni
from slownik_dni import marks_d


#dcc.Slider

'''
dcc.Slider(0, 10,
    step=None,
    marks={
        0: '0°F',
        3: '3°F',
        5: '5°F',
        7.65: '7.65°F',
        10: '10°F'
    },
    value=5
)
'''
''' 
df = pd.read_pickle("dafr.pkl")
fig = px.line(df, x='Data', y='Close' ,title='Stock chart')
plotly.offline.plot(fig, filename='fig.html')
'''
def dzis():
    today = date.today()
    print(today)
    Tlist = str(today).split('-')
    a = Tlist[1]+'.' +Tlist[2]
    print(a)
    d = float(a)
    dzis = str(d)

    return dzis

dzis = dzis()
instrument = 'Gold'
app = dash.Dash(__name__)
server = app.server
Years = [10 , 30]
df = pandas.DataFrame(Years, columns=['Years'])
app.layout = html.Div([
    html.H1(children="MARKET SESONALITY.", id='header'),
    html.P(children='sell may and go away...', id='motto'),
    html.Label("Select an instrument"),
    html.Div(
        dcc.Dropdown(
            options= data_managment.list_of_instruments,
            id='Instrument_Dropdown'
        )
    )    ,
    html.Div(
            children=html.Div([
            html.Div(dcc.Graph(figure=data_managment.open_kolejne_lata_posortowane_json(instrument) )),
            html.Div(dcc.Graph(figure=data_managment.fig_cumulative_30(instrument) )),
            html.Div(dcc.Graph(figure=data_managment.fig_cumulative_10(instrument)), id='aaa' ),
            html.Div(dcc.Graph(figure=data_managment.fig_probability_20(instrument))),
            dcc.Slider(0,len(s_dni),
                step=1,
                marks= marks_d,
                value=5,
                id='20_d_histogram'
                       ),
            html.Div(dcc.Graph(figure=Wykresy_histogramy.histogram_20(instrument,dzis))),
            html.Div(dcc.Graph(figure=data_managment.fig_probability_60(instrument))),
            dcc.Slider(0,len(s_dni),
                step=1,
                marks= marks_d,
                value=5,
                id='60_d_histogram'
                       ),
            html.Div(dcc.Graph(figure=Wykresy_histogramy.histogram_60(instrument,dzis),id='histogram60'),)

       ])
    , id='charts'),
    html.Br(),
    html.Div(
        [
        html.P('Copyright 2022 by Michał Banasiński.' , id="stopka"),
        html.P(
            html.A("Author's GitHub Prifile",href="https://github.com/mbanasinski"  , id='hh')
         ,id='linkstopki'
        )]


    )
])




@app.callback(
    Output(component_id='charts', component_property='children'),
    Input(component_id='Instrument_Dropdown', component_property='value'),
    )

def update_charts( value ):

    children =html.Div([
            html.Div(dcc.Graph(figure=data_managment.open_kolejne_lata_posortowane_json(str(value)))),
            html.Div(dcc.Graph(figure=data_managment.fig_cumulative_30(str(value)))),
            html.Div(dcc.Graph(figure=data_managment.fig_cumulative_10(str(value)))),
            html.Div(dcc.Graph(figure=data_managment.fig_probability_20(str(value)))),
            html.Div(dcc.Graph(figure=data_managment.fig_probability_60(str(value)))),
       ])
    return children
#app.css.append_css({
#    "exsternal_url":
#})
if __name__=="__main__":
    app.run_server()




