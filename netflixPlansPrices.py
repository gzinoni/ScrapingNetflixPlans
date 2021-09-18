from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

data_list = []

def Planes_Precios(tag):

    url = f'https://help.netflix.com/es/node/24926/{tag}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    #Por simple inspección, se observa que este tipo de paginas de Netflix poseen una unica tabla o ninguna, según el país.
    #En el caso de que la página posea una tabla, solo existen dos tipos de tablas. (Una de ellas tiene una fila y una columna extra)
    
    #Mediante esta variable, voy a chequear si la página en cuestión posee una tabla.
    tableCheck = soup.find_all("table", {"class":"c-table"})

    #Chequeo si la pagina posee una tabla
    if tableCheck:
      
      #Mediante esta variable chequearé que tipo de tabla contiene el link.
      columnCheck = soup.find_all('th')[3].text

      if 'Standar'in columnCheck:
         #Si es verdadero, quiere decir que la tabla es del tipo que contiene una fila y columna extra.
         #No recopilaré los datos extras ya que son datos que pertenecen a la minoría de los países.
         
         #Cargo los datos de las columnas.
         for i in range(0,3):
             
            #Dado que las celdas de la tabla no poseen un "id" o "class", decido acceder a ellas mediante indices. Para acceder a las celdas de la siguiente columna, simplemente me desplazo en UN valor (para ello utilizo el ciclo for)
            payload = {
            'Pais' : tag,
            'Plan' : soup.find_all('th')[2+i].text.strip(),
            'Precio' : soup.find_all('td')[2+i].text.strip(),
            'Disp_simul' : int(soup.find_all('td')[7+i].text.strip()),
            'Cant_disp_desc' : int(soup.find_all('td')[12+i].text.strip()),
            'Contenido_ilimitado' : soup.find_all('td')[17+i].text.strip(),
            'Laptop_tv_phone_tablet' : soup.find_all('td')[27+i].text.strip(),
            'HD' : soup.find_all('td')[32+i].text.strip(),
            'UHD' : soup.find_all('td')[37+i].text.strip(),
            }
            data_list.append(payload)

      else:
         #Si entro aquí quiere decir que la página posee el otro tipo de tabla.

         #Se realiza el mismo procedimiento, solo que las celdas de las columnas poseen distintos indices al ser una tabla distinta.
         #Cargo los datos de las columnas
         for i in range(0,3):

            payload = {
            'Pais' : tag,
            'Plan' : soup.find_all('th')[1+i].text.strip(),
            'Precio' : soup.find_all('td')[1+i].text.strip(),
            'Disp_simul' : int(soup.find_all('td')[5+i].text.strip()),
            'Cant_disp_desc' : int(soup.find_all('td')[9+i].text.strip()),
            'Contenido_ilimitado' : soup.find_all('td')[13+i].text.strip(),
            'Laptop_tv_phone_tablet' : soup.find_all('td')[17+i].text.strip(),
            'HD' : soup.find_all('td')[21+i].text.strip(),
            'UHD' : soup.find_all('td')[25+i].text.strip(),
            }
            data_list.append(payload)

    else:
         #Si no se encuentra ninguna tabla en la página, es porque en ese país no se presta el servicio de Netflix.
         payload = {
         'Pais' : tag,
         'Plan' : '-',
         'Precio' : '-',
         'Disp_simul' : '-',
         'Cant_disp_desc' : '-',
         'Contenido_ilimitado' : '-',
         'Laptop_tv_phone_tablet' : '-',
         'HD' : '-',
         'UHD' : '-',
         }
         data_list.append(payload)
       

#Si no desea probar el script con todos los países, seleccione solo algunos.
#allCountries = ["AF","AL","DE","AD","AO","AI","AQ","AG","SA","DZ","AR","AM","AW","AU","AT","AZ","BS","BD","BB","BH","BE","BZ","BJ","BM","BY","BO","BA","BW","BR","BN","BG","BF","BI","BT","CV","KH","CM","CA","BQ","QA","TD","CL","CN","CY","VA","CO","KM","KP","KR","CR","CI","HR","CU","CW","DK","DJ","DM","EC","EG","SV","AE","ER","SK","SI","ES","US","EE","ET","PH","FI","FJ","FR","GA","GM","GE","GH","GI","GD","GR","GL","GP","GU","GT","GF","GG","GN","GW","GQ","GY","HT","HN","HK","HU","IN","ID","IQ","IR","IE","BV","CX","IM","IS","NF","AX","KY","CC","CK","FO","GS","HM","FK","MP","MH","UM","PN","SB","TC","VG","VI","IL","IT","JM","JP","JE","KZ","KE","KG","KI","KW","LA","LS","LV","LB","LR","LY","LI","LT","LU","MO","MK","MG","MY","MW","MV","ML","MT","MA","MQ","MU","MR","YT","MX","FM","MD","MC","MN","ME","MS","MZ","MM","NA","NR","NP","NI","NE","NG","NU","NO","NC","NZ","OM","NL","PK","PW","PS","PA","PG","PY","PE","PF","PL","PT","PR","GB","CF","CZ","CG","CD","DO","RE","RW","RO","RU","EH","WS","AS","BL","KN","SM","MF","PM","SH","LC","ST","VC","SN","RS","SC","SL","SG","SX","SY","SO","LK","SZ","ZA","SD","SS","SE","CH","SR","SJ","TH","TW","TZ","TJ","IO","TF","TL","TG","TK","TO","TT","TN","TM","TR","TV","UA","UG","UY","UZ","VU","VE","VN","WF","YE","ZM","ZW"]
countries_list = ["AF","AL","DE","AD","AO","AI","AQ","AG","SA","DZ","AR","AM","AW","AU","AT","AZ","BS","BD","BB","BH","BE","BZ","BJ","BM","BY","BO","BA","BW","BR","BN","BG","BF","BI","BT","CV","KH","CM","CA","BQ","QA","TD","CL","CN","CY","VA","CO","KM","KP","KR","CR","CI","HR","CU","CW","DK","DJ","DM","EC","EG","SV","AE","ER","SK","SI","ES","US","EE","ET","PH","FI","FJ","FR","GA","GM","GE","GH","GI","GD","GR","GL","GP","GU","GT","GF","GG","GN","GW","GQ","GY","HT","HN","HK","HU","IN","ID","IQ","IR","IE","BV","CX","IM","IS","NF","AX","KY","CC","CK","FO","GS","HM","FK","MP","MH","UM","PN","SB","TC","VG","VI","IL","IT","JM","JP","JE","KZ","KE","KG","KI","KW","LA","LS","LV","LB","LR","LY","LI","LT","LU","MO","MK","MG","MY","MW","MV","ML","MT","MA","MQ","MU","MR","YT","MX","FM","MD","MC","MN","ME","MS","MZ","MM","NA","NR","NP","NI","NE","NG","NU","NO","NC","NZ","OM","NL","PK","PW","PS","PA","PG","PY","PE","PF","PL","PT","PR","GB","CF","CZ","CG","CD","DO","RE","RW","RO","RU","EH","WS","AS","BL","KN","SM","MF","PM","SH","LC","ST","VC","SN","RS","SC","SL","SG","SX","SY","SO","LK","SZ","ZA","SD","SS","SE","CH","SR","SJ","TH","TW","TZ","TJ","IO","TF","TL","TG","TK","TO","TT","TN","TM","TR","TV","UA","UG","UY","UZ","VU","VE","VN","WF","YE","ZM","ZW"]

#Llamada a la funcion con todos los países.
for i in countries_list:
    Planes_Precios(i)

df = pd.DataFrame(data_list)
df.to_excel('netflixPlansPricing.xlsx')
print('Fin.')