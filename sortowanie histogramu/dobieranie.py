import json

f = open('Gold_hisrofram_pozycji_60.json')
data = json.load(f)



lista_dni_w_roku = data['lista_dni_w_roku']
lista_lat = data['lista_wszystkich_lat']

lista_dni_w_roku.sort()
slownik_dni_dobranych_pozycji = {}
i = 0
for dzien in lista_dni_w_roku:
    dobrany_słownik_dnia = {}
    print('dzień',dzien)
    slownik_dnia = data[str(dzien)]
    print(type(dzien))
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
            print(rok,'Wymyślam jak dobrać rok')
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
                    print('mam dobry dzień')
                    slownik_z_pozycja_dobieraną = slownik_slownikow_pozycji_d[rok]
                    slownik_z_pozycja_dobieraną['d'] = d

                    print(slownik_z_pozycja_dobieraną)
                    dobrana_lista_slownikow_pozycji.append(slownik_z_pozycja_dobieraną)

                    break



    l_lat = []
    l_min = []
    l_max = []
    l_wynik = []
    for dict in dobrana_lista_slownikow_pozycji:
        print(dict)
        l_lat.append(dict['rok'])
        l_min.append(dict['maxsimum_procentowe'])
        l_max.append(dict['minimum_procentowe'])
        l_wynik.append(dict['wynik_pozyji'])

    print(l_lat)
    print(l_min)
    print(l_max)
    print(l_wynik)
    dobrany_słownik_dnia['lista_lat'] = l_lat
    dobrany_słownik_dnia['lista_min'] = l_min
    dobrany_słownik_dnia['lista_max'] = l_max
    dobrany_słownik_dnia['lista_wyniku'] = l_wynik
    dobrany_słownik_dnia['lista_słowników_pozycji'] = dobrana_lista_slownikow_pozycji
    slownik_dni_dobranych_pozycji[dzien] = dobrany_słownik_dnia

    i = i + 1


with open(f"dobrany_histogram.json", "w") as outfile:
    json.dump(slownik_dni_dobranych_pozycji, outfile)
