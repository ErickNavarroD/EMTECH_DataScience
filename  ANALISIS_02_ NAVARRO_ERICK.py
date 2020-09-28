#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:53:29 2020

@author: ericknavarro
"""
#Cargar datos y calcular datos básicos necesarios
import csv
"""Calcular rutas más demandadas por año
Forma de resolver: graficar la proporcion relativa anual de transacciones y valor 
de cada ruta y graficarlo para ver cuales se mantienen arriba constantemente a lo largo
de los años"""
    
#Calcular numero de transacciones anuales
with open("synergy_logistics_database.csv", "r", encoding='utf-8-sig') as database:
    database_r = csv.DictReader(database, delimiter = ",")
    transacciones_anuales = {}
    for transaccion in database_r:
        if transaccion["year"] not in transacciones_anuales.keys():
            transacciones_anuales[transaccion["year"]] = 1
        elif transaccion["year"] in transacciones_anuales.keys():
            transacciones_anuales[transaccion["year"]] += 1
    
#Calcular ganancias anuales
with open("synergy_logistics_database.csv", "r", encoding='utf-8-sig') as database:
    database_r = csv.DictReader(database, delimiter = ",")
    ganancias_anuales = {}
    for transaccion in database_r:
        if transaccion["year"] not in ganancias_anuales.keys():
            ganancias_anuales[transaccion["year"]] = int(transaccion["total_value"])
        elif transaccion["year"] in ganancias_anuales.keys():
            ganancias_anuales[transaccion["year"]] = ganancias_anuales[transaccion["year"]] + int(transaccion["total_value"])
#%%Crear lista con ventas por ruta
#Objetivo: generar lista con la proporción promedio anual de valor y cantidad de transacciones
            #por cada ruta, tomando las rutas con dirección (i.e. (japon->mexico) != (mexico->japon))
with open("synergy_logistics_database.csv", "r", encoding='utf-8-sig') as database:
    database_r = csv.DictReader(database, delimiter = ",")
    rutas = {}
    #Crear diccionario ordenado por años cuyo valor sea un diccionario que almacene las rutas del año y la informacion condensada de ella
    for transaccion in database_r:
        #Crear nombre de la ruta
        prefijo_ruta = transaccion["origin"] + "->" + transaccion["destination"]
        #Si no esta el año en el diccionario de rutas
        if transaccion["year"] not in rutas.keys():
            rutas[transaccion["year"]] = {prefijo_ruta: [transaccion["year"], prefijo_ruta, 1,int(transaccion["total_value"]) ]}
        #Si el año ya existe en el diccionario de rutas
        elif transaccion["year"] in rutas.keys():
            #Si la ruta no está en ese año
            if prefijo_ruta not in rutas[transaccion["year"]].keys():
                rutas[transaccion["year"]][prefijo_ruta] = [transaccion["year"], prefijo_ruta, 1,int(transaccion["total_value"])]
            #Si la ruta ya existe en el diccionario
            elif prefijo_ruta in rutas[transaccion["year"]].keys():
                rutas[transaccion["year"]][prefijo_ruta][2] += 1 #Añadir uno a la frecuencia
                rutas[transaccion["year"]][prefijo_ruta][3] += int(transaccion["total_value"]) #Sumar el valor de la transaccion al total anual

#Calcular la proporción relativa anual de cada ruta en ingresos y frecuencia y añadirla en cada ruta
for año in rutas.keys():
    #para cada ruta en cada año
    for ruta in rutas[año]: 
        #añadir la proporcion de transacciones de esa ruta en ese año
        rutas[año][ruta].append(rutas[año][ruta][2]/transacciones_anuales[año])
        #Añadir la proporcion de ganancias de esa ruta en ese año
        rutas[año][ruta].append(rutas[año][ruta][3]/ganancias_anuales[año])
"""
estructura: 
    rutas = {año:{ruta:[año,ruta,frecuenciaAnual,ValorAnual, FrecuenciaRelativaAnual, ValorRelativoAnual]}}
Objeto util para graficar proporciones relativas de valor y frecuencia de cada ruta a lo largo de los años
y para obtener el resultado final de proporcion relativa promedio a lo largo de los años.
"""
#Crear lista con frecuencia y valor anual relativo promedio
prop_frec = {}
prop_value = {}
#calcular proporcion acumulada
for año in rutas.keys():
    for ruta in rutas[año]:
        if ruta not in prop_frec.keys():
            prop_frec[ruta] = rutas[año][ruta][4]
            prop_value[ruta] = rutas[año][ruta][5]
        elif ruta in prop_frec.keys():
            prop_frec[ruta] += rutas[año][ruta][4]
            prop_value[ruta] += rutas[año][ruta][5]
#Calcular proporcion promedio
for ruta in prop_frec.keys():
    prop_frec[ruta] = round(prop_frec[ruta]/len(rutas), 3)
    prop_value[ruta] = round(prop_value[ruta]/len(rutas), 3)

#Juntar ambos diccionarios
proporciones = {}
for ruta in prop_frec.keys():
    proporciones[ruta] = [prop_frec[ruta], prop_value[ruta]]

#Convertir diccionario a lista de tuplas para poder ordenarla
proporciones = [(a, b, c) for a, [b, c] in proporciones.items()] 
#Ordenar de mayor a menor frecuencia relativa (rutas mas a menos demandadas al año)
proporciones.sort(key=lambda tup: tup[1], reverse = True)  

"""Estructura final:
proporciones = (Ruta, ProporcionPromedioAnual, ValorPromedioAnual)"""    
#Guardar el archivo final en csv para graficar con otro programa


with open("info_rutas.csv","w") as info_rutas:
    escritor = csv.writer(info_rutas)
    escritor.writerows(proporciones)


#%%
##Obtener medios de transporte más utilizados. 
#Crear lista con ventas por transporte
#Objetivo: Generar una lista con el transporte y su proporción promedio de ventas y transacciones anuales
with open("synergy_logistics_database.csv", "r", encoding='utf-8-sig') as database:
    database_r = csv.DictReader(database, delimiter = ",")
    transportes = {}
    #Crear diccionario ordenado por años cuyo valor sea un diccionario que almacene los transportes y la informacion de sus movimientos
    for transaccion in database_r:
        #Si no esta el año en el diccionario de transportes
        if transaccion["year"] not in transportes.keys():
            transportes[transaccion["year"]] = {transaccion["transport_mode"]: [transaccion["year"], transaccion["transport_mode"], 1,int(transaccion["total_value"]) ]}
        #Si el año ya existe en el diccionario de rutas
        elif transaccion["year"] in transportes.keys():
            #Si la ruta no está en ese año
            if transaccion["transport_mode"] not in transportes[transaccion["year"]].keys():
                transportes[transaccion["year"]][transaccion["transport_mode"]] = [transaccion["year"], transaccion["transport_mode"], 1,int(transaccion["total_value"])]
            #Si la ruta ya existe en el diccionario
            elif transaccion["transport_mode"] in transportes[transaccion["year"]].keys():
                transportes[transaccion["year"]][transaccion["transport_mode"]][2] += 1 #Añadir uno a la frecuencia
                transportes[transaccion["year"]][transaccion["transport_mode"]][3] += int(transaccion["total_value"]) #Sumar el valor de la transaccion al total anual

#Calcular la proporción relativa anual de cada transporte en ingresos y frecuencia y añadirla en cada ruta
for año in transportes.keys():
    #para cada transporte en cada año
    for transporte in transportes[año]: 
        #añadir la proporcion de transacciones de ese transporte en ese año
        transportes[año][transporte].append(transportes[año][transporte][2]/transacciones_anuales[año])
        #Añadir la proporcion de ganancias de ese transporte en ese año
        transportes[año][transporte].append(transportes[año][transporte][3]/ganancias_anuales[año])
"""
estructura: 
    transportes = {año:{transporte:[año,transporte,frecuenciaAnual,ValorAnual, FrecuenciaRelativaAnual, ValorRelativoAnual]}}
Objeto util para graficar proporciones relativas de valor y frecuencia de cada transporte a lo largo de los años
y para obtener el resultado final de proporcion relativa promedio a lo largo de los años.
"""
#Crear lista con frecuencia y valor anual relativo promedio de cada transporte
prop_frec_trans = {}
prop_value_trans = {}
#calcular proporcion acumulada
for año in transportes.keys():
    for transporte in transportes[año]:
        if transporte not in prop_frec_trans.keys():
            prop_frec_trans[transporte] = transportes[año][transporte][4]
            prop_value_trans[transporte] = transportes[año][transporte][5]
        elif transporte in prop_frec_trans.keys():
            prop_frec_trans[transporte] += transportes[año][transporte][4]
            prop_value_trans[transporte] += transportes[año][transporte][5]
#Calcular proporcion promedio
for transporte in prop_frec_trans.keys():
    prop_frec_trans[transporte] = round(prop_frec_trans[transporte]/len(transportes), 3)
    prop_value_trans[transporte] = round(prop_value_trans[transporte]/len(transportes), 3)

#Juntar ambos diccionarios
proporciones_trans = {}
for transporte in prop_frec_trans.keys():
    proporciones_trans[transporte] = [prop_frec_trans[transporte], prop_value_trans[transporte]]

#Convertir diccionario a lista de tuplas para poder ordenarla
proporciones_trans = [(a, b, c) for a, [b, c] in proporciones_trans.items()] 
#Ordenar de mayor a menor frecuencia relativa (transportes mas a menos importantes al año con respecto al total value)
proporciones_trans.sort(key=lambda tup: tup[2], reverse = True)  

#Guardar proporciones_trans para graficar con otro programa
"""Estructura final:
proporciones_trans = (Transporte, ProporcionPromedioAnual, ValorPromedioAnual)"""   
with open("info_transportes.csv","w") as info_transportes:
    escritor = csv.writer(info_transportes)
    escritor.writerows(proporciones_trans)

with open("info_trans_total.csv","w") as info_trans_total:
    escritor = csv.writer(info_trans_total)
    info_total = []
    for año in transportes.keys():
        for transporte in transportes[año]:
            info_total.append(transportes[año][transporte])
    escritor.writerows(info_total)

#%%Calcular paises que contribuyen al 80% de las ganancias
#Objetivo: obtener una lista para graficar que tenga año, pais y valor
#El pais al que se le asignará el valor de la transaccion será el origin en caso de exportacion y destination en caso de importación
with open("synergy_logistics_database.csv", "r", encoding='utf-8-sig') as database:
    database_r = csv.DictReader(database, delimiter = ",")
    paises_ganancias = []
    
    for transaccion in database_r:
        if transaccion["direction"] == "Exports":
            paises_ganancias.append([transaccion["year"], transaccion["origin"], transaccion["total_value"]])
        elif transaccion["direction"] == "Imports":
            paises_ganancias.append([transaccion["year"], transaccion["destination"], transaccion["total_value"]])
    """Estructura final: 
    paises_ganancias = [año, pais, total_value]"""

def proporciones_paises(paises_ganancias):
    prop_ganancias = {}
    paises = []
    #Sacar la suma de ganancia anuales de cada pais por año
    for transaccion in paises_ganancias:
        if transaccion[1] not in paises:
            paises.append(transaccion[1])
        #Si el año no esta en prop_ganancias añadir el elemento nuevo
        if transaccion[0] not in prop_ganancias.keys():
            prop_ganancias[transaccion[0]]= {transaccion[1]:int(transaccion[2])}
        #Si el año si esta en prop ganancias buscarlo y añadir el pais o sumarlo cuando ya esté
        elif transaccion[0] in prop_ganancias.keys():
            if transaccion[1] not in prop_ganancias[transaccion[0]].keys():
                prop_ganancias[transaccion[0]][transaccion[1]] = int(transaccion[2])
            elif transaccion[1] in prop_ganancias[transaccion[0]].keys():
                prop_ganancias[transaccion[0]][transaccion[1]] += int(transaccion[2])
    #Convertir la ganancia total por pais a ganancia relativa anual
    for año in prop_ganancias.keys():
        for pais in prop_ganancias[año].keys():
            prop_ganancias[año][pais] = prop_ganancias[año][pais]/ganancias_anuales[año]
    #Obtener la ganancia relativa anual promedio(grap)
    grap = []
    for pais in paises:
        suma = 0
        for año in prop_ganancias:
            if pais in prop_ganancias[año].keys():
                suma += prop_ganancias[año][pais]
        grap.append(([pais, round(suma/len(ganancias_anuales),4)]))
    #Ordenar la lista de mayor a menor contribuidor a las ganancias relativas 
    grap.sort(key = lambda x:x[1] ,reverse = True)
    #Regresar el objeto grap
    return grap

prop_paises_ganancias = proporciones_paises(paises_ganancias)
    
#Obtener paises que contribuyen al 80%
x = 0
index = 0
while x <= 0.80:
    print(prop_paises_ganancias[index])
    x += prop_paises_ganancias[index][1]
    print("La suma de porcentaje es" + str(x))
    index += 1
    
   
#Guardar la lista en csv de la informacion de los paises para graficar
with open("info_paises_value.csv","w") as info_paises:
    escritor = csv.writer(info_paises)
    escritor.writerows(paises_ganancias)
#Guardar lista ordenada de paises y su GRAP
with open("info_paises_grap_ordenado.csv","w") as grap_info:
    escritor = csv.writer(grap_info)
    escritor.writerows(prop_paises_ganancias)
