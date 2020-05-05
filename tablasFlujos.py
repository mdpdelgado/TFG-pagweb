#!/usr/bin/python3

import os
import pandas as pd
import argparse

# parsear argumentos que van detrás del comando
def argumentos():
    parser = argparse.ArgumentParser(add_help=True,
                                     description='Python to display flow tables',
                                     epilog='The sw and file arguments cannot be used at the same time. '
                                            'The profile and columns arguments cannot be used at the same time')

    parser.add_argument('--sw', action='store',
                        dest='sw',
                        help='Allows you to choose the switch from which you want to extract the flow tables')
    parser.add_argument('--file', action='store',
                        dest='file',
                        help='It allows you to take the data from a file that you have on your computer with the same format as the response to the ovs-ofctl dump-flows command')
    parser.add_argument('--info', action='store_true',
                        default = False,
                        dest='info',
                        help='Allows you to see the information of the tables in use and how many entries they have')
    parser.add_argument('--table', action='store',
                        dest='table',
                        help='Allows you to choose the table or tables you want to view, values separated by , ')
    parser.add_argument('--profile', action='store',
                        dest='profile',
                        help='Choose a user profile that shows certain columns. Values: simple, expert or emptyout.'
                             'emptyout: alow to remove all empty columns')
    parser.add_argument('--columns', action='store',
                        dest='columns',
                        help='Allows you to visualize certain columns, values separated by ,  '
                             'values: table, cookie, duration, nPackets, nBytes, idleAge, sendFlowRem, priority, '
                             'type, inPort, dlSrc, dlDst, dlType, nwSrc, nwDst, tpSrc, tpDst, vlanTci, dlVlan, mplsLabel, mplsBos, actions')

    results = parser.parse_args()

    if (results.sw == None and results.file == None and results.info == False and results.table == None and results.profile == None and results.columns == None):
        parser.print_help()
    elif(results.info == True):
        print()
    else:
        print('sw = {!r}'.format(results.sw))
        print('file = {!r}'.format(results.file))
        print('info = {!r}'.format(results.info))
        print('table = {!r}'.format(results.table))
        print('profile = {!r}'.format(results.profile))
        print('columns = {!r}'.format(results.columns))
    return results


# Descargar los flujos a un fichero txt segun el sw
def descargaSW(results):
    os.system("sudo ovs-ofctl dump-flows " + results.sw + " --protocols=OpenFlow13 > datos.txt")

#Copiar los datos de un fichero txt de entrada a otro con el que trabajar luego
def copiarFile(results):
    os.system("cp " + results.file + " datos.txt")

#Crear un DataFrame
def crearDataFrame():
    data = pd.DataFrame(columns=('table', 'cookie', 'duration', 'nPackets', 'nBytes', 'idleAge', 'sendFlowRem', 'priority', 'type', 'inPort', 'dlSrc', 'dlDst', 'dlType',
                                 'nwSrc', 'nwDst', 'tpSrc', 'tpDst', 'vlanTci', 'dlVlan', 'mplsLabel', 'mplsBos', 'actions'))
    return data

#Set de tablas activas
def crearTableSet():
    tableset = {"0"}
    return tableset

def arregloClaveSinValor(tipo, frase):
    v = frase.find(tipo)
    if v != -1:
        v += len(tipo)
        w = frase[0:v]
        w += '=' + tipo
        w += frase[v:len(frase)]
    else:
        w = frase
    return w


# Crear un diccionario de cada linea y rellenar el DataFrame
def llenarDataFrame(data, tableset):
    with open("datos.txt", "r") as f:
        it = (linea for i, linea in enumerate(f) if i > 0)
        for l in it:
            string = l

            # Encontrar actions y poner delante una coma
            a = string.find("actions")
            #print(a)

            b = string[0:a]
            actions = string[a+8:len(string) - 1]
            #print(b)
            #print(actions)

            # Encontrar send_flow_rem y poner detrás una coma
            c = b.find("send_flow_rem")
            if c != -1:
                c = c + 13
                #print(c)
                d = b[0:c]
                d += '=1,'
                d += b[c:len(b) - 1]
            else:
                d=b
            #print(d)

            # Arreglo de las claves que no tienen valor
            o = arregloClaveSinValor("arp", d)
            #print('o es'+o)
            h = arregloClaveSinValor("ip", o)
            #print('h es' + h)
            i = arregloClaveSinValor("icmp", h)
            #print('i es' + i)
            j = arregloClaveSinValor("tcp", i)
            #print('j es' + j)
            #k = arregloClaveSinValor("ipv6", j)
            #print('k es' + k)
            l = arregloClaveSinValor("mpls", j)
            #print('l es' + l)

            try:
                newDict = dict(map(lambda z: z.split("=", 1), l.split(",")))
                #print(newDict)
            except:
                print("Error al crear diccionario de linea: "+l)
                newDict = dict()

            if  ' table' in newDict:
                arg1 = newDict[' table']
                # Anadir tablas activas al set
                tableset.add(arg1)
            else:
                arg1 = '-'

            if ' cookie' in newDict:
                arg2a = newDict[' cookie']
                arg2 = arg2a[2:len(arg2a)]
            else:
                arg2 = '-'
            if ' duration' in newDict:
                arg3 = newDict[' duration']
            else:
                arg3 = '-'
            if ' n_packets' in newDict:
                arg4 = newDict[' n_packets']
            else:
                arg4 = '-'
            if ' n_bytes' in newDict:
                arg5 = newDict[' n_bytes']
            else:
                arg5 = '-'


            if ' idle_age' in newDict:
                arg6 = newDict[' idle_age']
            else:
                arg6 = '-'

            if ' send_flow_rem' in newDict:
                arg7 = 'si'
            else:
                arg7 = '-'

            if ' priority' in newDict:
                arg8 = newDict[' priority']
            else:
                arg8 = '-'

            if 'arp' in newDict:
                arg9 = newDict['arp']
            elif 'ip' in newDict:
                arg9 = newDict['ip']
            elif 'icmp' in newDict:
                arg9 = newDict['icmp']
            elif 'tcp' in newDict:
                arg9 = newDict['tcp']
            elif ' ip' in newDict:
                arg9 = newDict[' ip']
            elif 'mpls' in newDict:
                arg9 = newDict['mpls']
            elif ' mpls' in newDict:
                arg9 = newDict[' mpls']
            else:
                arg9 = '-'

            if 'in_port' in newDict:
                arg10 = newDict['in_port']
            else:
                arg10 = '-'

            if 'dl_src' in newDict:
                arg11 = newDict['dl_src']
            else:
                arg11 = '-'

            if 'dl_dst' in newDict:
                arg12 = newDict['dl_dst']
            else:
                arg12 = '-'

            if 'dl_type' in newDict:
                arg13 = newDict['dl_type']
            else:
                arg13 = '-'
            if 'nw_src' in newDict:
                arg14 = newDict['nw_src']
            else:
                arg14 = '-'
            if 'nw_dst' in newDict:
                arg15 = newDict['nw_dst']
            else:
                arg15 = '-'
            if 'tp_src' in newDict:
                arg16 = newDict['tp_src']
            else:
                arg16 = '-'
            if 'tp_dst' in newDict:
                arg17 = newDict['tp_dst']
            else:
                arg17 = '-'

            if 'vlan_tci' in newDict:
                arg18 = newDict['vlan_tci']
            else:
                arg18 = '-'
            if 'dl_vlan' in newDict:
                arg19 = newDict['dl_vlan']
            else:
                arg19 = '-'
            if 'mpls_label' in newDict:
                arg20 = newDict['mpls_label']
            else:
                arg20 = '-'
            if 'mpls_bos' in newDict:
                arg21 = newDict['mpls_bos']
            else:
                arg21 = '-'


            arg22 = actions

            #Rellenar el DataFrame
            data.loc[len(data)] = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19, arg20, arg21, arg22]
    f.close()
    return data,tableset

#Funcionalidad de informacion
def info(data,tableset):
    tableset2 = sorted(tableset)
    str1 = "La lista de tablas en uso es "
    for t in tableset2:
        str1 += t + ", "
    print(str1)

    dicaux = {}
    for e in tableset2:
        dataaux = data[data.table == e]
        num = len(dataaux.index)
        dicaux[e] = num

    for k,v in dicaux.items():
        if (v == 1):
            print ("En la tabla %s hay %s entrada" %(k,v))
        else:
            print("En la tabla %s hay %s entradas" % (k, v))

    numtotal = len(data.index)
    print("El numero total de entradas es " + str(numtotal))

#Funcionalidad de elegir tabla
def elegirTable(results,data,tableset,tab):
    try:
        tablesList = results.table.split(sep=',')
    except:
        tablesList = results.table
    #print(tablesList)
    data2 = pd.DataFrame(columns=('table', 'cookie', 'duration', 'nPackets', 'nBytes', 'idleAge', 'sendFlowRem', 'priority', 'type', 'inPort', 'dlSrc', 'dlDst', 'dlType',
                             'nwSrc', 'nwDst', 'tpSrc', 'tpDst', 'vlanTci', 'dlVlan', 'mplsLabel', 'mplsBos', 'actions'))
    for e in tablesList:
        dataAux = data
        #print(dataAux)
        if e in tableset:
            #eliminar tablas que no sean e
            dataAux = dataAux.loc[dataAux['table'] == e]
        else:
            dataAux = dataAux.loc[dataAux['table'] == e]
            print("La tabla " + e +" no tiene flujos activos")
        data2 = pd.concat([data2,dataAux])
    data = data2
    if data.empty:
        tab = False
    return data,tab
    #print(tab)
    #print(data)


# Funcionalidad del argumento profile
def elegirProfile(results,data,tab):
    
    if results.profile == 'todoData' and tab:
        data = data

    if results.profile == 'simple' and tab:
        collection_auxs = ['cookie', 'duration', 'nPackets', 'nBytes', 'idleAge', 'sendFlowRem', 'priority']
        for a in collection_auxs:
            data = data.drop([a], axis=1)

    if results.profile == 'expert' and tab:
        collection_auxe = ['cookie', 'sendFlowRem', 'idleAge']
        for a in collection_auxe:
            data = data.drop([a], axis=1)

    if results.profile == 'emptyout' and tab:
        lista_aux = ['table', 'cookie', 'duration', 'nPackets', 'nBytes', 'idleAge', 'sendFlowRem', 'priority', 'type', 'inPort', 'dlSrc', 'dlDst', 'dlType',
                     'nwSrc', 'nwDst', 'tpSrc', 'tpDst', 'vlanTci', 'dlVlan', 'mplsLabel', 'mplsBos', 'actions']
        numtotal = len(data.index)
        for col in lista_aux:
            dataaux = data[data[col] == '-']
            num = len(dataaux.index)
            if num == numtotal:
                data = data.drop([col], axis=1)
    return data

# Funcionalidad del argumento columns con una lista de elementos separados por coma
def elegirColumns(results,data,tab):
    newList = results.columns.split(sep=',')
    #print(newList)
    lista_aux = ['table', 'cookie', 'duration', 'nPackets', 'nBytes', 'idleAge', 'sendFlowRem', 'priority', 'type', 'inPort', 'dlSrc', 'dlDst', 'dlType',
                             'nwSrc', 'nwDst', 'tpSrc', 'tpDst', 'vlanTci', 'dlVlan', 'mplsLabel', 'mplsBos', 'actions']
    #print(lista_aux)

    for li in newList:
        for m in lista_aux:
            if m == li:
                lista_aux.remove(m)

    #print(newList)
    #print(lista_aux)

    for n in lista_aux:
        data = data.drop([n], axis=1)
    return data

#Convertir el DataFrame a csv
def covertirCsv(data):
    data.to_csv("pandasCSV.csv")

#ejecutar todas las funciones
results= argumentos()
if(results.sw == None and results.file == None and results.info == False and results.table == None and results.profile == None and results.columns == None):
    print()
else:
    if results.sw != None and results.file == None:
        descargaSW(results)
    if results.sw == None and results.file != None:
        copiarFile(results)
    data = crearDataFrame()
    tableset = crearTableSet()
    data,tableset = llenarDataFrame(data,tableset)

    #print(data)
    #print(tableset)

    if (results.info == True):
        info(data,tableset)
    else:
        tab = True

        if results.table != None:
            data,tab = elegirTable(results,data,tableset,tab)

        data = elegirProfile(results,data,tab)

        if results.columns != None and results.profile == None and tab:
            data = elegirColumns(results,data,tab)

        print(data)
        covertirCsv(data)
