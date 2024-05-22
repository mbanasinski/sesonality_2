import json
import plotly.express as px
import plotly.graph_objects as go
instrument = 'Gold'
dzien = 1.03



def histogram_60(instrument,dzien):
    dzien = str(dzien)
    print(dzien)


    f = open(f"{instrument}_hisrofram_pozycji_60_dobierany.json")
    slownik_danch_histogrmau = json.load(f)
    slownik_dnia = slownik_danch_histogrmau[dzien]
    lista_lat    = slownik_dnia['lista_lat']
    lista_min    = slownik_dnia['lista_min']
    lista_max    = slownik_dnia['lista_max']
    lista_wyniku = slownik_dnia['lista_wyniku']

    print(lista_lat)
    print(lista_min)
    print(lista_max)
    print(lista_wyniku)

    tit = f'Returnes of 60 day positions {instrument} | date={dzien}'
    fig = go.Figure(
        data=[
            go.Bar(name='Wynik pozycji', x=lista_lat, y=lista_wyniku),
            go.Bar(name='Minimum', x=lista_lat, y=lista_min),
            go.Bar(name='max', x=lista_lat, y=lista_max)
        ],
        layout=go.Layout(title=tit)

    )

    #fig = px.bar(y=lista_wyniku, x=lista_lat)
    fig.show()
    return fig

def histogram_20(instrument,dzien):
    dzien = str(dzien)
    print(dzien)


    f = open(f"{instrument}_hisrofram_pozycji_20_dobierany.json")
    slownik_danch_histogrmau = json.load(f)
    slownik_dnia = slownik_danch_histogrmau[dzien]
    lista_lat    = slownik_dnia['lista_lat']
    lista_min    = slownik_dnia['lista_min']
    lista_max    = slownik_dnia['lista_max']
    lista_wyniku = slownik_dnia['lista_wyniku']

    print(lista_lat)
    print(lista_min)
    print(lista_max)
    print(lista_wyniku)

    tit = f'Returnes of 20 day positions {instrument} | date={dzien}'
    fig = go.Figure(
        data=[
            go.Bar(name='Wynik pozycji', x=lista_lat, y=lista_wyniku),
            go.Bar(name='Minimum', x=lista_lat, y=lista_min),
            go.Bar(name='max', x=lista_lat, y=lista_max),
        ],
        layout=go.Layout(title=tit)


    )

    #fig = px.bar(y=lista_wyniku, x=lista_lat)
    #fig.show()
    return fig




histogram_20(instrument,'12.2')
