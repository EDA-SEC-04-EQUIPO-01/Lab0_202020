"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *f
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista.
"""

import config as cf
import sys
import csv
from time import process_time 

def loadCSVFile (file, lst, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file 
            Archivo de texto del cual se cargaran los datos requeridos.
        lst :: []
            Lista a la cual quedaran cargados los elementos despues de la lectura del archivo.
        sep :: str
            Separador escodigo para diferenciar a los distintos elementos dentro del archivo.
    Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None   
    """
    del lst[:]
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lst.append(row)
    except:
        del lst[:]
        print("Se presento un error en la carga del archivo")
    
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Contar los elementos de la Lista")
    print("3- Contar elementos filtrados por palabra clave")
    print("4- Consultar elementos a partir de dos listas")
    print("0- Salir")

def countElementsFilteredByColumn(criteria, column, lst):               
    
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        for element in lst:
            if criteria.lower() in element[column].lower(): #filtrar por palabra clave 
                counter+=1
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return counter


def countElementsByCriteria3(criteria, lista, lista2):
    suma=0
    cont=0
    ident=[]
    for a in lista:
        if criteria==a["director_name"]:
            ident.append(a["id"])
    for b in lista2:
        if (b["\ufeffid"] in ident) and (float(b["vote_average"])>=6.0):
            suma+=float(b["vote_average"])
            cont+=1
    k= round(suma/cont,2)
    respuesta= str('Se han encontrado ') +str(cont) +str(' peliculas, las cuales tienen un promedio de ') +str(k)
    return respuesta

def countElementsByCriteria(criteria, casting, details):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    if len(casting)==0 or len(details)==0:
        print("Algunas de las listas están vacía")  
        return (0,0)
    else:
        ids = []
        for element in casting:
            if element["director_name"].lower() == criteria.lower():
                ids.append(element["id"])
        sumatoria = 0
        goodmovies = 0
        pos = 0
        for element in details:
            if len(ids) > pos:
                try:
                    if element["id"]==ids[pos] and float(element["vote_average"])>=6.0:
                        sumatoria += float(element["vote_average"])
                        goodmovies+=1
                        pos +=1
                except:
                    if element["\ufeffid"]==ids[pos] and float(element["vote_average"])>=6.0:
                        sumatoria += float(element["vote_average"])
                        goodmovies+=1
                        pos +=1
            else:
                break
        try:
            promedio = sumatoria/goodmovies
        except:
            promedio = 0
        return (goodmovies,promedio)


def countElementsByCriteria2(criteria, lst, lst2,dif):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    t1_start = process_time()
    column="director_name"
    counter = 0
    ids = []
    buenas = []
    suma = 0
    promedio = 0
    for fila in lst:
        if criteria.lower() in fila[column].lower():
            ids.append(fila["id"])
    for element in ids:
        i = 0
        seguir = True
        while seguir == True and i<len(lst2):
            if lst2[i][dif]==element and float(lst2[i]["vote_average"])>=6:
                counter +=1
                buenas.append(float(lst2[i]["vote_average"]))
                seguir = False
            else:
                i+=1

    for cal in buenas:
        suma+=cal

    if len(buenas) != 0:
        promedio = round(suma/len(buenas),2)

    t1_stop = process_time()
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    
    return (counter,promedio)
    


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """

    lista = [] #Casting
    lista2 = [] #Details

    casting = [] #instanciar una lista vacia
    details = []

    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                loadCSVFile("Data/AllMoviesCastingRaw.csv", casting) #llamar funcion cargar datos
                loadCSVFile("Data/AllMoviesDetailsCleaned.csv",details)
                print("Datos cargados, "+str(len(casting)+len(details))+" elementos cargados")
            elif int(inputs[0])==2: #opcion 2
                if len(casting)==0: #obtener la longitud de la lista
                    print("La lista esta vacía")    
                else: print("La lista tiene "+str(len(casting))+" elementos")
            elif int(inputs[0])==3: #opcion 3
                archivo = input("Ingresa 1 si quieres buscarlo en el archivo de Casting o 2 en el archivo de detalles\n")
                criteria =input('Ingrese el criterio de búsqueda\n')
                columna = input("Ingresa el nombre de la columna en la que quieres buscar\n")
                if archivo == "1":
                    counter=countElementsFilteredByColumn(criteria, columna, casting) #filtrar una columna por criterio  
                else:
                    counter=countElementsFilteredByColumn(criteria, columna, details)
                print("Coinciden ",counter," elementos con el crtierio: ", criteria  )
            elif int(inputs[0])==4: #opcion 4
                criteria =input('Ingrese el nombre del director que va a buscar\n')
                counter=countElementsByCriteria(criteria,casting,details)
                print("Hay ",counter[0]," buenas películas producidas por: ", criteria ," y en promedio esas buenas películas tuvieron ", counter[1], " vote average")            elif int(inputs[0])==0: #opcion 0, salir

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                

if __name__ == "__main__":
    main()
