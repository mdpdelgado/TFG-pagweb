#!/usr/bin/python3

import os
import pandas as pd
import argparse

# parsear argumentos que van detras del comando
def argumentos():
    parser = argparse.ArgumentParser(add_help=True,
                                     description='Python to display groups tables',
                                     epilog='Each action is placed in different columns (prepared for 6 actions)')

    parser.add_argument('--sw', action='store',
                        dest='sw',
                        help='Allows you to choose the switch from which you want to extract the groups tables')
    parser.add_argument('--file', action='store',
                        dest='file',
                        help='It allows you to take the data from a file that you have on your computer with the same format as the response to the ovs-ofctl dump-groups command')
    parser.add_argument('--columns', action='store',
                        dest='columns',
                        help='Allows you to visualize certain columns, values separated by ,'
                             'values: groupId, type, bucketActions1, bucketActions2, bucketActions3, bucketActions4, bucketActions5, bucketActions6')

    results = parser.parse_args()

    if (results.sw == None and results.file == None and results.columns == None):
        parser.print_help()
    else:
        print('columns = {!r}'.format(results.columns))
        print('sw = {!r}'.format(results.sw))
        print('file = {!r}'.format(results.file))
    return results

# Descargar los grupos a un fichero txt segun el sw
def descargaSW(results):
    os.system("sudo ovs-ofctl dump-groups " + results.sw + " --protocols=OpenFlow13 > g.txt")

#Copiar los datos de un fichero txt de entrada a otro con el que trabajar luego
def copiarFile(results):
    os.system("cp " + results.file + " g.txt")

#Crear un DataFrame
def crearDataFrame():
    data = pd.DataFrame(columns=('groupId', 'type', 'bucketActions1','bucketActions2','bucketActions3','bucketActions4','bucketActions5','bucketActions6'))
    # DataFrame preparado para 6 bucketActions
    return data

#grupo inicial funciones
results= argumentos()
if (results.sw == None and results.file == None and results.columns == None):
    print()
else:
    if results.sw != None and results.file == None:
        descargaSW(results)
    if results.sw == None and results.file != None:
        copiarFile(results)
    data = crearDataFrame()

    # Problema con vars dentro de una funcion
    # Crear un diccionario de cada linea y rellenar el DataFrame
    with open("g.txt", "r") as f:
        it = (linea for i, linea in enumerate(f) if i > 0)
        for l in it:
            string = l


            # Encontrar actions y poner delante una coma
            a = string.find("bucket")
            #print(a)

            if a != -1:
                b = string[0:a-1]
                actions = string[a+15:len(string) - 1]
                #print(b)
                #print(actions)
            else:
                b = l
                actions = "-"

            newDict = dict(map(lambda z: z.split("=", 1), b.split(",")))
            #print(newDict)

            arg1 = newDict[' group_id']
            arg2 = newDict['type']

            arg3="-"
            arg4="-"
            arg5="-"
            arg6="-"
            arg7="-"
            arg8="-"
            listActions = actions.split(sep=',')

            aux=3
            for e in listActions:
                m = e.find("bucket")
                if m!=-1:
                    n = e[m + 15:len(string) - 1]
                else:
                    n=e
                #Al meterlo en una función esta linea no funciona
                vars()["arg%s" %aux] = n
                aux=aux+1

            #Rellenar el DataFrame
            data.loc[len(data)] = [arg1, arg2, arg3,arg4,arg5,arg6,arg7,arg8]
    f.close()
    #print(data)


# Funcionalidad del argumento columns con una lista de elementos separados por coma
def elegirColumns(results,data):
    newList = results.columns.split(sep=',')
    #print(newList)
    lista_aux = ['groupId', 'type', 'bucketActions1','bucketActions2','bucketActions3','bucketActions4','bucketActions5','bucketActions6']
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

#Segundo grupo de funciones
if (results.sw == None and results.file == None and results.columns == None):
    print()
else:
    if results.columns != None:
        data = elegirColumns(results,data)

    print(data)
    covertirCsv(data)