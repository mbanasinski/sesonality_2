import yfinance as yf
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date
#import pandas_datareader.data as web
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import json

#####################################################################
# PARAMETRY DO PROGRAMU
#####################################################################

dic_of_tickers = {"Gold":"GC=F","Silver":"SI=F", "Palladium":"PA=F", "Platinum":"PL=F", "Copper":"HG=F", "Aluminum":"ALI=F", "Crude Oil":"CL=F", "Heating Oil":"HO=F", "Natural Gas":"NG=F", "Gasoline":"RB=F", "Corn":"ZC=F", "Oat":"ZO=F", "Wheat":"KE=F", "Soybean":"ZS=F", "Soybean Oil":"ZL=F", "Cocoa":"CC=F", "Coffee":"KC=F", "Cotton":"CT=F", "Lumber":"LBS=F", "Sugar":"SB=F", "10-Year T-Note":"ZN=F", "S&P 500":"^GSPC", "Nikkei 225":"^N225", "Dow Jones":"^DJI", "Apple Inc":"AAPL", "Tesla":"TSLA", "Amazon":"AMZN", "American Airlines":"AAL", "Alphabet(Google)":"GOOGL", "Bitcoin USD":"BTC-USD", "EURUSD":"EURUSD=X", "USDJPY":"JPY=X", "GBPUSD":"GBPUSD=X", "AUDUSD":"AUDUSD=X", "NZDUSD":"NZDUSD=X", "EURJPY":"EURJPY=X", "GBPJPY":"GBPJPY=X", "EURGBP":"EURGBP=X", "EURCAD":"EURCAD=X", "EURSEK":"EURSEK=X", "EURCHF":"EURCHF=X", "EURHUF":"EURHUF=X", "EURJPY":"EURJPY=X", "USDHKD":"HKD=X", "USDSGD":"SGD=X", "USDINR":"INR=X", "USDRUB":"RUB=X", "EURCAD":"EURCAD=X", "CADCHF":"CADCHF=X", "CADJPY":"CADJPY=X", "CHFJPY":"CHFJPY=X", "GBPCAD":"GBPCAD=X", "GBPCHF":"GBPCHF=X", "AUDCAD":"AUDCAD=X", "AUDCHF":"AUDCHF=X", "AUDJPY":"AUDJPY=X", "AUDNZD":"AUDNZD=X", "CHFPLN":"CHFPLN=X", "EURNOK":"EURNOK=X", "EURNZD":"EURNZD=X", "EURPLN":"EURPLN=X", "EURSEK":"EURSEK=X", "GBPAUD":"GBPAUD=X", "GBPNZD":"GBPNZD=X", "GBPPLN":"GBPPLN=X", "NZDJPY":"NZDJPY=X", "USDNOK":"NOK=X", "USDPLN":"PLN=X"}

dni_w_pozycji = 60
ticker =  "GC=F"
start_date = "2003-01-01"

############################################################



def wykres_probability_Yahoo(ticker, start_date, days_in_position):
    today = str(date.today()).split("-", 1)[1].replace("-",".")
    actual_Year = int(str(date.today()).split("-", 1)[0])
    def Donwland_Data_Fron_Yahoo_probability(ticker, start_date):
        df_of_prices = yf.download(ticker, start=start_date)
        return df_of_prices

    btc_price = Donwland_Data_Fron_Yahoo_probability(ticker, start_date)
    print(btc_price)
    btc_price.to_csv('zloto_test_min.csv')

    def List_Of_returnes_probability(df_of_prices, days_in_position):
        List_Of_returnes = []
        i = 0
        for index, row in df_of_prices.iterrows():
            #print(index)
            zwrot = (btc_price['Close'][i + (days_in_position - 1)] - df_of_prices['Open'][i]) / df_of_prices['Open'][i]
            List_Of_returnes.append(zwrot)
            i = i +1
            if i == (len(df_of_prices.index) - days_in_position ):
                break
        return List_Of_returnes

    zwrory = List_Of_returnes_probability(btc_price, days_in_position)



    def min_max(df_of_prices):
        list_of_max_values = []
        lista_słowników_pozycji_60_skrocona = []
        i = 0
        koniec_pozycji = i + (days_in_position - 1)
        lista_słowników_pozycji_60 = []
        #print(df_of_prices.to_dict())

        for index, row in df_of_prices.iterrows():
            słownik_dnia = row.to_dict()
            słownik_dnia['data'] = str(index)
            lista_słowników_pozycji_60.append(słownik_dnia)

        for dict in lista_słowników_pozycji_60:
            #print(dict)
            zwrot = (lista_słowników_pozycji_60[i + (days_in_position - 1)]['Close']  -  lista_słowników_pozycji_60[i]['Open']) / lista_słowników_pozycji_60[i]['Open']
            wynik_pozyji = zwrot
            dict['wynik_pozyji'] = wynik_pozyji
            lista_słowników_trwana_pozucji = lista_słowników_pozycji_60[i:i + days_in_position]
            lista_low = []
            lista_High = []
            for dzien in lista_słowników_trwana_pozucji:
                #print(dzien)
                lista_low.append(dzien['Low'])
                lista_High.append(dzien['High'])


            cena_minimalna = min(lista_low)
            cena_maksymalna = max(lista_High)
            dict['cena_minimalna'] = cena_minimalna
            dict['cena_maksymalna'] = cena_maksymalna
            minimum_procentowe = ( dict['cena_minimalna'] - dict['Open'])/ dict['Open']
            maxsimum_procentowe = ( dict['cena_maksymalna'] - dict['Open'])/ dict['Open']
            #print('min_procentowe',minimum_procentowe)
            #print(cena_minimalna)
            #print('max_procentowe',maxsimum_procentowe)
            dict['minimum_procentowe'] = minimum_procentowe
            dict['maxsimum_procentowe'] = maxsimum_procentowe
            #print(dict)
            lista_słowników_pozycji_60_skrocona.append(dict)

            i = i +1
            if i == (len(lista_słowników_pozycji_60) - days_in_position ):
                break

        def lista_dni_w_roku(df_of_prices):
            dzien_roku = []
            lista_dni_w_roku = []
            for index, row in df_of_prices.iterrows():
                data = str(index)
                data.count('0')
                data = data.replace(' 00:00:00', '')
                data = data.split("-", 1)[1]
                data = float(data.replace('-', '.'))
                if data not in lista_dni_w_roku:
                    lista_dni_w_roku.append(data)
            return lista_dni_w_roku

        lista_dni_w_roku = lista_dni_w_roku(df_of_prices)

        slownik_histogramu_pozycji = {

        }

        lista_wszystkich_lat = []
        for dzien in lista_dni_w_roku:
            slownik_pozycji_dla_dnia = {}
            lista_lat = []
            lista_min = []
            lista_max = []
            lista_wyniku = []
            lista_słowników_pozycji = []
            for dict in lista_słowników_pozycji_60_skrocona:

                data = dict['data']
                #print(data)

                data.count('0')
                data = data.replace(' 00:00:00', '')
                rok = data.split("-", 1)[0]
                #print(rok)
                if rok not in lista_wszystkich_lat:
                    lista_wszystkich_lat.append(rok)
                data = data.split("-", 1)[1]
                data = float(data.replace('-', '.'))
########################################################################################
                # Tworzenie struktury danych pod histogram Pozycji
                if data == dzien:
                    #print(dzien,data)
                    lista_lat.append(rok)
                    lista_max.append(dict['maxsimum_procentowe'])
                    lista_min.append(dict['minimum_procentowe'])
                    lista_wyniku.append(dict['wynik_pozyji'])
                    pozycja_dict = {
                        'rok':rok,
                        'maxsimum_procentowe':dict['maxsimum_procentowe'],
                        'minimum_procentowe':dict['minimum_procentowe'],
                        'wynik_pozyji':dict['wynik_pozyji'],
                    }
                    lista_słowników_pozycji.append(pozycja_dict)

                slownik_pozycji_dla_dnia['lista_lat'] = lista_lat
                slownik_pozycji_dla_dnia['lista_min'] = lista_min
                slownik_pozycji_dla_dnia['lista_max'] = lista_max
                slownik_pozycji_dla_dnia['lista_wyniku'] = lista_wyniku
                slownik_pozycji_dla_dnia['lista_słowników_pozycji'] = lista_słowników_pozycji
                print(slownik_pozycji_dla_dnia)
                slownik_histogramu_pozycji[dzien] = slownik_pozycji_dla_dnia

                instrument = None

                for instrument_name in dic_of_tickers:
                    if dic_of_tickers[instrument_name] == ticker:
                        instrument = instrument_name

        slownik_histogramu_pozycji['lista_wszystkich_lat'] = lista_wszystkich_lat
        slownik_histogramu_pozycji['lista_dni_w_roku'] = lista_dni_w_roku

        with open(f"{instrument}_hisrofram_pozycji_{days_in_position}.json", "w") as outfile:
            json.dump(slownik_histogramu_pozycji, outfile)
    ############# Wklejka
        f = open(f"{instrument}_hisrofram_pozycji_{days_in_position}.json")
        data = json.load(f)



        lista_dni_w_roku = data['lista_dni_w_roku']
        lista_lat = data['lista_wszystkich_lat']
        l_prawdobodobienstwa = []
        lista_dni_w_roku.sort()
        slownik_dni_dobranych_pozycji = {}
        i = 0
        for dzien in lista_dni_w_roku:
            dobrany_słownik_dnia = {}
            #print('dzień',dzien)
            slownik_dnia = data[str(dzien)]

            #print(type(dzien))
            lista_słowników_pozycji = slownik_dnia['lista_słowników_pozycji']
            slowniik_slownikow_pozycji = {}
            lista_lat_na_ten_dzien = []
            dobrana_lista_slownikow_pozycji = []

            for dict in lista_słowników_pozycji:
                slowniik_slownikow_pozycji[dict['rok']] = dict
                lista_lat_na_ten_dzien.append(dict['rok'])
            for rok in lista_lat:
                if rok in lista_lat_na_ten_dzien:
                    #print(rok,slowniik_slownikow_pozycji[str(rok)])
                    dobrana_lista_slownikow_pozycji.append(slowniik_slownikow_pozycji[str(rok)])
                else:
                    #print(rok,'Wymyślam jak dobrać rok')
                    for d in lista_dni_w_roku[i+1:]:
                        #print(d)
                        mam_math = False
                        lista_slowikow_pozycji_d = data[str(d)]['lista_słowników_pozycji']
                        slownik_slownikow_pozycji_d = {}
                        lista_r_in_d = []
                        for r in lista_slowikow_pozycji_d:
                            lista_r_in_d.append(r['rok'])
                            slownik_slownikow_pozycji_d[r['rok']] = r
                        #print(lista_r_in_d)
                        if rok in lista_r_in_d:
                            #print('mam dobry dzień')
                            slownik_z_pozycja_dobieraną = slownik_slownikow_pozycji_d[rok]
                            slownik_z_pozycja_dobieraną['d'] = d

                            #print(slownik_z_pozycja_dobieraną)
                            dobrana_lista_slownikow_pozycji.append(slownik_z_pozycja_dobieraną)

                            break



            l_lat = []
            l_min = []
            l_max = []
            l_wynik = []
            prawdopodobienstwo = None
            up = 0
            down = 0
            ilosc_pozucji = len(dobrana_lista_slownikow_pozycji)
            for dict in dobrana_lista_slownikow_pozycji:
                print(dict)
                l_lat.append(dict['rok'])
                l_min.append(dict['minimum_procentowe'])
                l_max.append(dict['maxsimum_procentowe'])
                l_wynik.append(dict['wynik_pozyji'])
                wynik_pozyji = dict['wynik_pozyji']
                if wynik_pozyji > 0:
                    up = up + 1
                else:
                    down = down + 1

            prawdopodobienstwo = (up / ilosc_pozucji ) *100


            l_prawdobodobienstwa.append(prawdopodobienstwo)

            #print(l_lat)
            #print(l_min)
            #print(l_max)
            #print(l_wynik)
            dobrany_słownik_dnia['lista_lat'] = l_lat
            dobrany_słownik_dnia['lista_min'] = l_min
            dobrany_słownik_dnia['lista_max'] = l_max
            dobrany_słownik_dnia['lista_wyniku'] = l_wynik
            dobrany_słownik_dnia['lista_słowników_pozycji'] = dobrana_lista_slownikow_pozycji
            dobrany_słownik_dnia['prawdopodobienstwo'] = prawdopodobienstwo
            slownik_dni_dobranych_pozycji[dzien] = dobrany_słownik_dnia

            i = i + 1
        string_lista_dni_w_roku = []
        for d in lista_dni_w_roku:
            dzien = str(d)
            string_lista_dni_w_roku.append(dzien)
        slownik_dni_dobranych_pozycji['lista_prawdobodobienstwa'] = l_prawdobodobienstwa
        slownik_dni_dobranych_pozycji['lista_dni_w_roku'] = string_lista_dni_w_roku
        slownik_dni_dobranych_pozycji['lista_lat'] = lista_lat
        print('#####################################################################################################################3')
        print(string_lista_dni_w_roku)


        dict_do_df = {'day': string_lista_dni_w_roku, 'probability': l_prawdobodobienstwa}
        df = pd.DataFrame(dict_do_df)
        print(df)
        df.to_pickle(instrument+"_probability_dobierane_"+str(days_in_position) +".pkl")

        #fig = px.line(x=string_lista_dni_w_roku, y=l_prawdobodobienstwa, title='HISTORICAL PROBABILITY OF WINNING 20 TRADING DAYS POSITION '+' '+instrument)
        #fig.show()


        with open(f"{instrument}_hisrofram_pozycji_{days_in_position}_dobierany.json", "w") as outfile:
            json.dump(slownik_dni_dobranych_pozycji, outfile)







        return

    min_max(btc_price)


    def cut_df_to_shape_of_returnes_probability(df_of_prices, days_in_position):
        for i in range(days_in_position):
            df_of_prices =  df_of_prices.drop(df_of_prices.index[len(df_of_prices)-1])
        return df_of_prices

    btc_price = cut_df_to_shape_of_returnes_probability(btc_price, days_in_position)

    def Add_List_of_returnes_to_df_probability(df_of_prices, List_Of_returnes):
        df_of_prices['returnes'] = List_Of_returnes

    Add_List_of_returnes_to_df_probability(btc_price, zwrory)

    def list_of_days_probability(df_of_prices):
        dzien_roku = []
        lista_dni_w_roku_b = []
        for index, row in df_of_prices.iterrows():
            data = str(index)
            data.count('0')
            data = data.replace(' 00:00:00', '')
            data = data.split("-", 1)[1]
            data = float(data.replace('-', '.'))
            dzien_roku.append(data)
            lista_dni_w_roku_b.append(data)
        return dzien_roku

    dzien_roku = list_of_days_probability(btc_price)

    def list_of_days_in_year_probability(df_of_prices):
        lista_dni_w_roku_b = []
        for index, row in df_of_prices.iterrows():
            data = str(index)
            data.count('0')
            data = data.replace(' 00:00:00', '')
            data = data.split("-", 1)[1]
            data = float(data.replace('-', '.'))
            lista_dni_w_roku_b.append(data)
        lista_dni_w_roku = []
        for x in lista_dni_w_roku_b:
            if x not in lista_dni_w_roku:
                lista_dni_w_roku.append(x)
        lista_dni_w_roku.sort()
        return lista_dni_w_roku

    lista_dni_w_roku =  list_of_days_in_year_probability(btc_price)


    ####Utworzyłem plik z listy dni w roku
    '''
    ###################################################
    with open("listadniwroku.txt", 'w') as f:
        for s in lista_dni_w_roku:
            f.write(str(s) + '\n')
    #####################################################
    '''


    def addig_dates_of_days_to_df_probability(df_of_prices, list_of_days):
        df_of_prices['dzien_roku'] = list_of_days
        return df_of_prices

    btc_price = addig_dates_of_days_to_df_probability(btc_price, dzien_roku)

    def dictionary_of_dares_probability(lista_dni_w_roku):
        dict_list_dni = {}
        for d in lista_dni_w_roku:
            dl = []
            dict_list_dni.update({d: dl})
        return dict_list_dni

    dict_list_dni = dictionary_of_dares_probability(lista_dni_w_roku)

    def Tworzenie_wykresu_probability(dict_list_dni, btc_price, lista_dni_w_roku):
        małylicznik = 0
        for item in dict_list_dni:
            licznik = 0
            for index, row in btc_price.iterrows():
                #print(zwrory[licznik])
                if dzien_roku[licznik] == item:
                    dict_list_dni[item].append(zwrory[licznik])
                else:
                    pass
                licznik = licznik + 1





        dict_list_dni_binarnie = dict_list_dni
        lll = 0
        for lista in dict_list_dni_binarnie:
            lll = lll + 1
            licznik_listy = 0
            licznik_listy = int(licznik_listy)
            for el in dict_list_dni_binarnie[lista]:
                if el > 0.0:
                    dict_list_dni_binarnie[lista][licznik_listy] = 1
                else:
                    dict_list_dni_binarnie[lista][licznik_listy] = 0
                licznik_listy = licznik_listy + 1

        dict_list_dni_procentowo = dict_list_dni_binarnie

        for lista in dict_list_dni_procentowo:
            procent = round( (sum(dict_list_dni_procentowo[lista]) / len(dict_list_dni_procentowo[lista])) * 100, 2)
            dict_list_dni_procentowo[lista] = procent

        dict_list_dni_procentowo_string = {}

        for qqq in dict_list_dni_procentowo:
            a = str(qqq)
            ab = a.replace('.', '-')
            aaa = dict_list_dni_procentowo[qqq]
            dict_list_dni_procentowo_string.update({ab: aaa})

        dict_list_dni_procentowo_string2 = {}
        for i in lista_dni_w_roku:
            e = str(i)
            if len(str(i)) < 4:
                e = str(i) + '0'
            a = e.split('.')

            a = e.split('.')
            if len(a[1]) == 1:
                a[1] = a[1] + "0"
            a[0] = a[0].replace('12','Dec')
            a[0] = a[0].replace('11','Nov')
            a[0] = a[0].replace('10','Oct')
            a[0] = a[0].replace('9','Sep')
            a[0] = a[0].replace('8','Aug')
            a[0] = a[0].replace('7','Jul')
            a[0] = a[0].replace('6','Jun')
            a[0] = a[0].replace('5','May')
            a[0] = a[0].replace('4','Apr')
            a[0] = a[0].replace('3','Mar')
            a[0] = a[0].replace('2','Feb')
            a[0] = a[0].replace('1','Jan')
            ''' 
            a[0] = a[0].replace('12','Grudzień')
            a[0] = a[0].replace('11','Listopad')
            a[0] = a[0].replace('10','Pażdziernik')
            a[0] = a[0].replace('9','Wrzesień')
            a[0] = a[0].replace('8','Sierpień')
            a[0] = a[0].replace('7','Lipiec')
            a[0] = a[0].replace('6','Czerwiec')
            a[0] = a[0].replace('5','Maj')
            a[0] = a[0].replace('4','Kwiecień')
            a[0] = a[0].replace('3','Marzec')
            a[0] = a[0].replace('2','Luty')
            a[0] = a[0].replace('1','Styczeń')
            '''
            dict_list_dni_procentowo_string2.update({a[1]+'-'+a[0]:dict_list_dni_procentowo_string[str(i).replace('.','-')]})

        tabela_procentowa = pd.DataFrame(dict_list_dni_procentowo_string2.items(), columns=['Date', '%_PROBABILITY'])

        #fig = px.line(tabela_procentowa, x='Date', y='DateValue' ,title='SESONAL PATTERN PROBABILITY'+' '+ticker)
        return tabela_procentowa

    aaa = Tworzenie_wykresu_probability(dict_list_dni, btc_price, lista_dni_w_roku)
    return aaa

def wykres_probability_Stooq(ticker, start_date, days_in_position):
    today = str(date.today()).split("-", 1)[1].replace("-",".")
    actual_Year = int(str(date.today()).split("-", 1)[0])
    def Donwland_Data_Fron_Yahoo_probability(ticker, start_date):
        df_of_prices = web.DataReader(ticker, 'stooq', start=start_date)
        xs = [000] * len(df_of_prices)
        df_of_prices['xs'] = xs
        df_of_prices = df_of_prices.sort_values(by=['Date'])
        #df_of_prices = yf.download(ticker, start=start_date)
        return df_of_prices

    btc_price = Donwland_Data_Fron_Yahoo_probability(ticker, start_date)

    def List_Of_returnes_probability(df_of_prices, days_in_position):
        List_Of_returnes = []
        i = 0
        for index, row in df_of_prices.iterrows():
            #print(index)
            zwrot = (btc_price['Close'][i + (days_in_position - 1)] - df_of_prices['Open'][i]) / df_of_prices['Open'][i]
            List_Of_returnes.append(zwrot)
            i = i +1
            if i == (len(df_of_prices.index) - days_in_position ):
                break
        return List_Of_returnes

    zwrory = List_Of_returnes_probability(btc_price, days_in_position)

    def cut_df_to_shape_of_returnes_probability(df_of_prices, days_in_position):
        for i in range(days_in_position):
            df_of_prices =  df_of_prices.drop(df_of_prices.index[len(df_of_prices)-1])
        return df_of_prices

    btc_price = cut_df_to_shape_of_returnes_probability(btc_price, days_in_position)

    def Add_List_of_returnes_to_df_probability(df_of_prices, List_Of_returnes):
        df_of_prices['returnes'] = List_Of_returnes

    Add_List_of_returnes_to_df_probability(btc_price, zwrory)

    def list_of_days_probability(df_of_prices):
        dzien_roku = []
        lista_dni_w_roku_b = []
        for index, row in df_of_prices.iterrows():
            data = str(index)
            data.count('0')
            data = data.replace(' 00:00:00', '')
            data = data.split("-", 1)[1]
            data = float(data.replace('-', '.'))
            dzien_roku.append(data)
            lista_dni_w_roku_b.append(data)
        return dzien_roku

    dzien_roku = list_of_days_probability(btc_price)

    def list_of_days_in_year_probability(df_of_prices):
        lista_dni_w_roku_b = []
        for index, row in df_of_prices.iterrows():
            data = str(index)
            data.count('0')
            data = data.replace(' 00:00:00', '')
            data = data.split("-", 1)[1]
            data = float(data.replace('-', '.'))
            lista_dni_w_roku_b.append(data)
        lista_dni_w_roku = []
        for x in lista_dni_w_roku_b:
            if x not in lista_dni_w_roku:
                lista_dni_w_roku.append(x)
        lista_dni_w_roku.sort()
        return lista_dni_w_roku

    lista_dni_w_roku =  list_of_days_in_year_probability(btc_price)

    def addig_dates_of_days_to_df_probability(df_of_prices, list_of_days):
        df_of_prices['dzien_roku'] = list_of_days
        return df_of_prices

    btc_price = addig_dates_of_days_to_df_probability(btc_price, dzien_roku)

    def dictionary_of_dares_probability(lista_dni_w_roku):
        dict_list_dni = {}
        for d in lista_dni_w_roku:
            dl = []
            dict_list_dni.update({d: dl})
        return dict_list_dni

    dict_list_dni = dictionary_of_dares_probability(lista_dni_w_roku)

    def Tworzenie_wykresu_probability(dict_list_dni, btc_price, lista_dni_w_roku):
        małylicznik = 0
        for item in dict_list_dni:
            licznik = 0
            for index, row in btc_price.iterrows():
                #print(zwrory[licznik])
                if dzien_roku[licznik] == item:
                    dict_list_dni[item].append(zwrory[licznik])
                else:
                    pass
                licznik = licznik + 1





        dict_list_dni_binarnie = dict_list_dni
        lll = 0
        for lista in dict_list_dni_binarnie:
            lll = lll + 1
            licznik_listy = 0
            licznik_listy = int(licznik_listy)
            for el in dict_list_dni_binarnie[lista]:
                if el > 0.0:
                    dict_list_dni_binarnie[lista][licznik_listy] = 1
                else:
                    dict_list_dni_binarnie[lista][licznik_listy] = 0
                licznik_listy = licznik_listy + 1

        dict_list_dni_procentowo = dict_list_dni_binarnie

        for lista in dict_list_dni_procentowo:
            procent = round( (sum(dict_list_dni_procentowo[lista]) / len(dict_list_dni_procentowo[lista])) * 100, 2)
            dict_list_dni_procentowo[lista] = procent

        dict_list_dni_procentowo_string = {}

        for qqq in dict_list_dni_procentowo:
            a = str(qqq)
            ab = a.replace('.', '-')
            aaa = dict_list_dni_procentowo[qqq]
            dict_list_dni_procentowo_string.update({ab: aaa})

        dict_list_dni_procentowo_string2 = {}
        for i in lista_dni_w_roku:
            e = str(i)
            if len(str(i)) < 4 or len(str(i)) == 4 :
                e = str(i) + '0'
            a = e.split('.')
            a[0] = a[0].replace('12','Grudzień')
            a[0] = a[0].replace('11','Listopad')
            a[0] = a[0].replace('10','Pażdziernik')
            a[0] = a[0].replace('9','Wrzesień')
            a[0] = a[0].replace('8','Sierpień')
            a[0] = a[0].replace('7','Lipiec')
            a[0] = a[0].replace('6','Czerwiec')
            a[0] = a[0].replace('5','Maj')
            a[0] = a[0].replace('4','Kwiecień')
            a[0] = a[0].replace('3','Marzec')
            a[0] = a[0].replace('2','Luty')
            a[0] = a[0].replace('1','Styczeń')
            dict_list_dni_procentowo_string2.update({a[1]+'-'+a[0]:dict_list_dni_procentowo_string[str(i).replace('.','-')]})

        tabela_procentowa = pd.DataFrame(dict_list_dni_procentowo_string2.items(), columns=['Date', 'DateValue'])
        fig = px.line(tabela_procentowa, x='Date', y='DateValue' ,title='SESONAL PATTERN PROBABILITY'+' '+ticker)
        return fig

    aaa = Tworzenie_wykresu_probability(dict_list_dni, btc_price, lista_dni_w_roku)
    return aaa


#aaa = wykres_probability_Yahoo(ticker, start_date, dni_w_pozycji)
#print(aaa)


