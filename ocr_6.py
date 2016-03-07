#-----------------------------------------------------------------------#
#                                                                       #
#               PROGRAMA PARA REALIZAR EL RECONOCIMIENTO                #
#                       DE IMAGENES MEDIANTE OCR                        #
#                                                                       #
#                   ELABORADO POR: MARCOS, ROBERTO                      #
#                                                                       #
#-----------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------#
#                                                                                                   #
#           DESCRIPCION DE LOS ATRIBUTOS DE LAS INSTANCIAS                                          #
#                                                                                                   #
#  atributo 0 = numero consecutivo                                                                  #
#  atributo 1 = numero de columnas / numero de filas                                                #
#  atributo 2 = numero de 1's / tamanio de la imagen(filas * columnas)                              #
#  atributo 3 = numero de 1's que hay en la columna de enmedio/tamanio de la imagen                 #
#  atributo 4 = numero de 1's que hay en la columna a un cuarto/tamanio de la imagen                #
#  atributo 5 = numero de 1's que hay en la columna entre 4 * 3/tamanio de la imagen                #
#  atributo 6 = numero de 1's que hay en la fila de enmedio/tamanio de la imagen                    #
#  atributo 7 = numero de 1's que hay en la fila a un cuarto/tamanio de la imagen                   #
#  atributo 8 = numero de 1's que hay en la fila entre 4 * 3/tamanio de la imagen                   #
#  atributo 9 = numero de cortes que hay en la columna de enmedio/tamanio de la imagen              #
#  atributo 10 = numero de cortes que hay en la columna a un cuarto/tamanio de la imagen            #
#  atributo 11 = numero de cortes que hay en la columna entre 4 * 3/tamanio de la imagen            #
#  atributo 12 = numero de cortes que hay en la fila de enmedio/tamanio de la imagen                #
#  atributo 13 = numero de cortes que hay en la fila a un cuarto/tamanio de la imagen               #
#  atributo 14 = numero de cortes que hay en la fila entre 4 * 3/tamanio de la imagen               #
#  atributo 15 = clase a la que pertenecen                                                          #
#                                                                                                   #
#---------------------------------------------------------------------------------------------------#
#-->Librerias ocupadas en este programa
import os#para poder recorrer las carpetas
import matplotlib.image as im#abrir la imagen como matriz
from PIL import Image as IM#abrir la imagen y obtener sus filas y columnas
import csv,math#para generar el archivo csv y hacer la raiz cuadrada
from time import time#para obtener el tiempo del sistema
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : Funcion main                                                             #
# DESCRIPCION : es la primera en ejecutarse y llama a la funcion proceso            #
# PARAMETROS : ninguno                                                              #
# RETORNO : ninguno                                                                 #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def menu():
    mensaje = """
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#       PROGRAMA PARA REALIZAR EL METODO OCR DE IMAGENES
#
#               ELABORADO POR: ROBERTO, MARCOS
#                         8 B
#                    MINERIA DE DATOS
#                          2016
#
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
    print(mensaje)#impresion del mensaje
    repetir = 1#variable que controla el while
    while(repetir == 1):#condicion del while
        print("\nMenu de opciones\n1 --> Generar el archivo .csv\n2 --> Aplicar el OCR mediante KNN")#impresion de opciones
        opcion = int(input('------>  '))#se lee la opcion ingresada por el usuario
        if(opcion == 1):#evaluamos la opcion
            path = input('Ingresa la ruta de la carpeta padre\n')
            load(path)#llamamos al metodo load pasando como parametro la ruta del directorio
        elif(opcion == 2):#evaluamos la opcion en caso que el usuario seleccione knn
            knn()#se llama a la funcion knn
        else:#sino
            print("Ha ingresado una opcion incorrecta")
            menu()#se ejecuta de nuevo la funcion menu en caso de que no haya ingresado 1 o 2 como opciones
        print("Desea ejecutar de nuevo el programa??\n1 --> Si\n2 --> No")
        repetir = int(input('---->  '))#se lee la entrada del del usuario
    print("Programa finalizado, elaborado por: Roberto, Marcos\n\t\t8 B")
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : funcion load                                                             #
# DESCRIPCION : leer las carpetas y los archivos dentro de la carpeta padre         #
# PARAMETROS : string padre, es la ruta del directorio padre                        #
# RETORNO : ninguno                                                                 #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def load(padre):
    #lista donde se almacenaran cada una de las rutas del directorio padre
    rutas = []
    #recorrermos todos los archivos que hay dentro de la carpeta padre
    for (path, carpetas, archivos) in os.walk(padre):
        #recorremos las carpetas existentes en el directorio y accedemos a sus archivos
        for name in archivos:
            #concatenamos la el nombre de la carpeta con el nombre de la imagen
            ruta = path+"/"+name#
            rutas.append(ruta)#agreamos la ruta a la lista de rutas
    leer(sorted(rutas))#llamamos al metodo leer pasando como parametros las rutas ordenadas
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : funcion leer                                                             #
# DESCRIPCION : abre todas las imagenes con las rutas obtenidas anteriormente       #
# PARAMETROS : list de todas las rutas de las imagenes                              #
# RETORNO : ninguno                                                                 #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def leer(rutas):
    #para saber el tiempo en que inicio el proceso
    inicio = time()
    archivo = input('Escribe el nombre del archivo para guardar los datos\n')#entrada del nombre del archivo
    n_archivo = archivo + ".csv"#concatenamos el nombre del archivo con la extension que es csv
    abrir = open(n_archivo,'w')#abrimos el archivo para escribir
    csvsalida = open(n_archivo, 'w', newline='')#para escribir el el archivo csv
    escribir = csv.writer(csvsalida)
    print("Escribiendo las caracteristicas en el archivo csv")
    print("Sea paciente, este proceso puede llevar unos minutos")
    t = 0#variable total de instancias escritas
    carpeta = -1#para indicar el proceso total, el contador lo declaramos con -1
    for i in range(len(rutas)): #recorremos todas las imagenes para sacar sus atributos    
        instancias = []#lista para los atributos por cada instancia
        img=im.imread(rutas[i])#abrir la imagen con este metodo para tener acceso a la matriz
        img1 = IM.open(rutas[i])#abrir la imagen con este metodo para tener acceso al metodo para calcular filas y columnas
        col, filas = img1.size#obtenemos el tamanio de cada imagen
        instancias.extend([(i+1),float(filas)/float(col),atr2(img,filas,col)])#agregamos los 3 primeros atributos a la lista
        r_col = atributos(img, filas, col,True)#lista con los resultados de los atributos de las columnas
        r_filas = atributos(img, filas, col,False) #lista con los resultados de los atributos de las filas
        #agregamos los demas atributos a nuestra lista de instancias
        instancias.extend([r_col[0],r_col[1],r_col[2],r_filas[0],r_filas[1],r_filas[2],r_col[3],r_col[4],r_col[5],r_filas[3],r_filas[4],r_filas[5]])
        #del numbre de la ruta, tomamos el nombre de la carpeta que este caso esta en la posicion 6 y este es la clase a la que pertenece
        instancias.append(int(rutas[i][6]))#atributo 15
        #guardamos en una lista nueva los renglones a escribir en el archivo
        data = [(instancias[0],instancias[1],instancias[2],instancias[3],instancias[4],instancias[5],instancias[6],instancias[7],instancias[8],instancias[9],instancias[10],instancias[11],instancias[12],instancias[13],instancias[14],instancias[15])]
        escribir.writerows(data)#escribimos en el archivo el renglon con los datos obtenidos de la imagen
        t = i+1#aumentamos el contador de instancias totales en 1
        if(carpeta != int(rutas[i][6])):#mostramos el proceso actual de la operacion
            carpeta +=1#aumentamos el contador de la carpeta en 1
            print("\nProgreso actual = escribiendo datos de la carpeta ---> "+str(rutas[i][6]))
            print("Progreso total global ---> "+str(carpeta)+str("0%"))#mostramos un mensaje formateado al usuario
        #fin del for total
    csvsalida.close()#cerramos el archivo csv al terminar de escribir todas las instancias
    fin = time()#tomamos el tiempo cuando el proceso de generar el archivo termina
    print("Progreso total global ---> 100%")
    tt =  ((fin - inicio)/60)#calculamos el tiempo total que se llevo para realizar el dataset
    print("\n\n#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("------> Informacion general del dataset creado")
    print("------> Instancias escritas en el archivo "+str(t))
    print("------> Cantidad de caracteristicas de cada instancia : 16")
    print("------> Descripcion de cada caracteristica")
    descripcion = """
atributo 1 = numero de instancia
atributo 2 = numero de columnas / numero de filas
atributo 3 = numero de 1's / tamanio de la imagen(filas * columnas)
atributo 4 = numero de 1's que hay en la columna de enmedio/tamanio de la imagen
atributo 5 = numero de 1's que hay en la columna a un cuarto/tamanio de la imagen
atributo 6 = numero de 1's que hay en la columna entre 4 * 3/tamanio de la imagen
atributo 7 = numero de 1's que hay en la fila de enmedio/tamanio de la imagen
atributo 8 = numero de 1's que hay en la fila a un cuarto/tamanio de la imagen
atributo 9 = numero de 1's que hay en la fila entre 4 * 3/tamanio de la imagen
atributo 10 = numero de cortes que hay en la columna de enmedio/tamanio de la imagen
atributo 11 = numero de cortes que hay en la columna a un cuarto/tamanio de la imagen
atributo 12 = numero de cortes que hay en la columna entre 4 * 3/tamanio de la imagen
atributo 13 = numero de cortes que hay en la fila de enmedio/tamanio de la imagen
atributo 14 = numero de cortes que hay en la fila a un cuarto/tamanio de la imagen
atributo 15 = numero de cortes que hay en la fila entre 4 * 3/tamanio de la imagen
atributo 16 = clase a la que pertenecen
"""
    #impresion de la informacion general del dataset
    print(descripcion)
    print("Clases : 0 --> 1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8 --> 9")
    print("-----> Nombre del archivo csv generado "+n_archivo)
    print("\n\nTiempo de procesamiento de las imagenes =  %.2f minutos." % tt)#mostramos el mensaje formateado
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : funcion atr2                                                             #
# DESCRIPCION : calcula los 1's entre el tamanio de la imagen                       #
# PARAMETROS : array img, int filas, int col                                        #
# RETORNO : int unos                                                                #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def atr2(img, filas, col):
    unos = 0#contador de los unos en la imagen
    for i in range(filas):#recorremos la imagen como una matriz de 2 dimensiones
        for j in range(col):
            if(img[i][j] == 1):#comparamos si el dato es 1
                unos+=1#aumentamos el contador
    return unos/(filas*col)#regresamos el numero de unos entre el tamanio de la imagen
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : funcion atributos                                                        #
# DESCRIPCION : calcula los atributos indicados en las columnas o en las filas      #
# PARAMETROS : array img, int filas, int col                                        #
# RETORNO : atri1, atri2, atri3, corte1, corte2, corte3                             #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def atributos(img, filas, col,isCol):
    #variable para almacenar el tamanio de la imagen
    tam = filas*col
    #contadores de cada atributo
    atri1 = atri2 = atri3 = 0
    #condiciones de cada atributo
    if(isCol == True):#si es columnas, las condiciones van enfocadas a estas
        condicion_atri1 = int(col/2)
        condicion_atri2 = int(col/4)
        condicion_atri3 = int((col/4)*3)
    elif(isCol == False):#si es una fila, cambiamos la condicion a filas
        condicion_atri1 = int(filas/2)
        condicion_atri2 = int(filas/4)
        condicion_atri3 = int((filas/4)*3)
    #listas para calcular los cortes
    lista1 = []
    lista2 = []
    lista3 = []
    #recorremos toda la imagen y comparamos
    for i in range(filas):
        for j in range(col):
            if(isCol == True):#si es una columna, comparamos la variable j que controla a las columnas
                if(j == condicion_atri1):#si mi contador en j(columnas) es igual a la condicion lo agregamos a la lista
                    lista1.append(img[i][j])#agregamos el valor en una lista, dependiendo la condicion
                    if(img[i][j] == 1):#comparamos si es un uno
                        atri1+=1#el contador de mi atributo aumenta en uno
                if(j == condicion_atri2):#comparamos si es un uno
                    lista2.append(img[i][j])#agregamos el valor en una lista, dependiendo la condicion
                    if(img[i][j] == 1):#comparamos si es un uno
                        atri2+=1#el contador de mi atributo aumenta en uno
                if(j == condicion_atri3):#comparamos si es un uno
                    lista3.append(img[i][j])#agregamos el valor en una lista, dependiendo la condicion
                    if(img[i][j] == 1):#comparamos si es un uno
                        atri3+=1#el contador de mi atributo aumenta en uno
            elif(isCol == False):#si es una fila entonces la variable de comparacion sera i
                if(i == condicion_atri1):
                    lista1.append(img[i][j])
                    if(img[i][j] == 1):
                        atri1+=1
                if(i == condicion_atri2):
                    lista2.append(img[i][j])
                    if(img[i][j] == 1):
                        atri2+=1
                if(i == condicion_atri3):
                    lista3.append(img[i][j])
                    if(img[i][j] == 1):
                        atri3+=1
    #valor inicial para calcular los cortes
    inicio1 = lista1[0]
    inicio2 = lista2[0]
    inicio3 = lista3[0]
    #contadores de cada corte
    corte1 = corte2 = corte3 = 0
    #condicion para los cortes en caso de que el inicio de la lista sea un uno, aumentamos el contador
    if(lista1[0] == 1):
        corte1+=1
    if(lista2[0] == 1):
        corte2+=1
    if(lista3[0] == 1):
        corte3+=1
    #condicion para los cortes en caso de que el fin de la lista sea un uno, aumentamos el contador
    if(lista1[len(lista1)-1] == 1):
        corte1+=1
    if(lista2[len(lista1)-1] == 1):
        corte2+=1
    if(lista3[len(lista1)-1] == 1):
        corte3+=1
    #recorremos la lista de las columnas o filas y calculamos los cortes
    for l in range(len(lista1)):
        if(inicio1 != lista1[l]):
            inicio1 = lista1[l]
            corte1+=1
        if(inicio2 != lista2[l]):
            inicio2 = lista2[l]
            corte2+=1
        if(inicio3 != lista3[l]):
            inicio3 = lista3[l]
            corte3+=1
    atributos = [(atri1/tam), (atri2/tam), (atri3/tam), corte1, corte2, corte3]
    return atributos
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : Funcion knn                                                              #
# DESCRIPCION : calcular el metodo KNN, llama a las demas funciones de KNN          #
# PARAMETROS : ninguno                                                              #
# RETORNO :  ninguno                                                                #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def knn():
    print("Aplicando el metodo KNN para el reconocimiento de imagenes OCR")
    print("Ingrese la ruta del archivo csv")
    ruta = input('----->  ')+".csv"#contatenamos la ruta con la extension .csv
    #ruta = 'dataset.csv'
    print("Ingrese la ruta de la imagen que desea reconocer")
    r_imagen = input('----->  ')+".png"#concatenamos el nombre de la imagen con la extension .png
    r = "test/"+r_imagen#la ruta la concatenamos con la carpeta por defecto que se llama test
    nueva = carac_imagen(r)#llamamos al metodo para obtener sus caracteristicas
    leer_data(ruta,nueva)#llamamos al metodo para leer el dataset
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : Funcion carac_imagen                                                     #
# DESCRIPCION : calcular los atributos de la imagen nueva                           #
# PARAMETROS : string r_imagen                                                      #
# RETORNO :  list datos(datos de la imagen nueva)                                   #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def carac_imagen(r_imagen):
    datos = []#lista donde se almacenaran los datos de la imagen ingresada
    img=im.imread(r_imagen)#abrir la imagen con este metodo para tener acceso a la matriz
    img1 = IM.open(r_imagen)#abrir la imagen con este metodo para tener acceso al metodo de obtener filas y columnas 
    col, filas = img1.size#obtenemos el tamanio de cada imagene
    datos.extend([float(filas)/float(col),atr2(img,filas,col)])#agregamos los 3 primeros atributos a la lista de datos
    r_col = atributos(img, filas, col,True)#lista con los resultados de los atributos de las columnas
    r_filas = atributos(img, filas, col,False) #lista con los resultados de los atributos de las filas
    col,filas = img1.size#obtenemos el tamanio de cada imagen
    r_col = atributos(img, filas, col,True)#lista con los resultados de los atributos de las columnas
    r_filas = atributos(img, filas, col,False) #lista con los resultados de los atributos de las filas
    #agregamos los demas atributos a nuestra lista de instancias
    datos.extend([r_col[0],r_col[1],r_col[2],r_filas[0],r_filas[1],r_filas[2],r_col[3],r_col[4],r_col[5],r_filas[3],r_filas[4],r_filas[5]])
    return datos
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : Funcion leer_data                                                        #
# DESCRIPCION : lee el archivo csv y llama al metodo para calcular sus distancias   #
# PARAMETROS : string ruta, list x(datos de la imagen a calcular)                   #
# RETORNO :  list distancia(la distancia de todas las instancias)                   #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def leer_data(ruta,x):
    read = csv.reader(open(ruta,'r'))#abrimos el dataset
    datos_distancia = []#lista para almacenar las distancias de cada instancia
    dis = 0#varible donde se iran almacenando las distancias de cada imagen
    for index,row in enumerate(read):#recorremos todo el dataset y accedemos a sus columnas con la funcion row
        #aqui sacamos los datos de cada renglon y los pasamos como parametros para la funcion de calcular distancia
        y = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]),float(row[12]),float(row[13]),float(row[14])]
        dis = distancia(x,y)#llamamos al metodo distancia y le pasamos como parametros los datos de la nueva imagen y de cada instancia del dataset
        atri = []#lista que contiene el numero de instancia, la distancia obtenida y la clase a la que pertenece
        atri.extend([int(index+1),dis,int(row[15])])#agregamos los 3 atributos
        datos_distancia.append(atri)#estos los agregamos a la lista datos_distancia
    vecinos(datos_distancia,ruta)#llamamos a la funcion vecinos pasandole como parametro la lista generada y la ruta del archivo
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : Funcion distancia                                                        #
# DESCRIPCION : calcula las distancias de una instancia                             #
# PARAMETROS : list x(instancia a calcular), list y(instancia de cada renglon)      #
# RETORNO :  float distancia                                                        #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def distancia(x,y):
    total = 0.0#variable donde se va almacenando el total de las distancias calculadas
    for i in range(len(x)):#recorremos la lista
        total+=((float(x[i])-float(y[i]))**2)#calculamos su distancia
    return math.sqrt(total)#regresamos la raiz cuadrada del valor de la variable total
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : Funcion vecinos                                                          #
# DESCRIPCION : calcula los vecinos mas cercanos y obtiene su clase                 #
# PARAMETROS : list datos_distancia, string ruta                                    #
# RETORNO :  ninguno                                                                #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def vecinos(datos_distancia,ruta):
    print("Ingrese el valor de K")
    k = int(input('----->  '))#leemos el valor de k ingresado por el usuario
    solo_distancias = []#lista que solo almacenara la distancia
    for x in range(len(datos_distancia)):#recorremos la lista de los datos de las distancia
        solo_distancias.append(datos_distancia[x][1])#en una nueva lista solo agregamos la pura distancia
    veci = []#lista que almacenara los valores dependiendo el valor de k ingresado
    distan = sorted(solo_distancias)#en una nueva lista, ordenamos la lista que solo contiene las distancias
    for i in range(len(distan)):#recorremos la lista ordenada de distancias
        if(i == int(k)):#cuando el contador del for sea igual al valor de k el ciclo se rompe
            break
        else:#sino
            veci.append(distan[i])#agregamos la distancia a la lista veci
    contador_distancias = 1
    print("\n\n")
    lista_a_ordenar = []
    for z in range(len(datos_distancia)):#recorremos la lista donde estan los 3 datos de cada instancia
        for y in range(len(veci)):#recorremos la lista de vecinos
            if(veci[y] == datos_distancia[z][1]):#si la distancia del vecino es igual a la distancia de la lista original de datos
                #print("Numero --> "+str(contador_distancias),"\tinstancia numero --> "+str(datos_distancia[z][0]) +" \tdistancia --> "+str(datos_distancia[z][1])+" \tque pertenece a la clase --> "+str(datos_distancia[z][2]))#impresion de datos deseados
                lista = []
                lista.extend([datos_distancia[z][0],datos_distancia[z][1],datos_distancia[z][2]])
                lista_a_ordenar.append(lista)
                contador_distancias+=1
    ordenar_distancias(lista_a_ordenar)

    #contadores de cada clase
    c0 = c1 = c2 = c3 = c4 = c5 = c6 = c7 = c8 = c9 = c = 0
    read = csv.reader(open(ruta,'r'))#abrimos el archivo
    for index,row in enumerate(read):#recorremos el archivo del dataset
        for j in range(k):#comparamos con cada valor de la lista de vecinos
            if(solo_distancias[c] == veci[j]):#comparamos si alguna distancia en k corresponde a una del dataset original
                if(int(row[15]) == 0):#comparaciones de cada clase
                    c0+=1#aumenta el contador de la clase en uno
                elif(int(row[15]) == 1):
                    c1+=1
                elif(int(row[15]) == 2):
                    c2+=1
                elif(int(row[15]) == 3):
                    c3+=1
                elif(int(row[15]) == 4):
                    c4+=1
                elif(int(row[15]) == 5):
                    c5+=1
                elif(int(row[15]) == 6):
                    c6+=1
                elif(int(row[15]) == 7):
                    c7+=1
                elif(int(row[15]) == 8):
                    c8+=1
                elif(int(row[15]) == 9):
                    c9+=1
        c+=1
    #impresiones de los contadores de cada clase
    print("\n------------------------------------------")
    print("\nInstancias de la clase 0 --> "+str(c0))
    print("Instancias de la clase 1 --> "+str(c1))
    print("Instancias de la clase 2 --> "+str(c2))
    print("Instancias de la clase 3 --> "+str(c3))
    print("Instancias de la clase 4 --> "+str(c4))
    print("Instancias de la clase 5 --> "+str(c5))
    print("Instancias de la clase 6 --> "+str(c6))
    print("Instancias de la clase 7 --> "+str(c7))
    print("Instancias de la clase 8 --> "+str(c8))
    print("Instancias de la clase 9 --> "+str(c9))
    print("\n\n")
    #comparaciones para cada clase
    if(c0 > c1 and c0 > c2 and c0 > c3 and c0 > c4 and c0 > c5 and c0 > c6 and c0 > c7 and c0 > c8 and c0 > c9):
        print("---------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 0")
    elif(c1 > c0 and c1 > c2 and c1 > c3 and c1 > c4 and c1 > c5 and c1 > c6 and c1 > c7 and c1 > c8 and c1 > c9):
        print("---------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 1")
    elif(c2 > c0 and c2 > c1 and c2 > c3 and c2 > c4 and c2 > c5 and c2 > c6 and c2 > c7 and c2 > c8 and c2 > c9):
        print("---------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 2")
    elif(c3 > c0 and c3 > c1 and c3 > c2 and c3 > c4 and c3 > c5 and c3 > c6 and c3 > c7 and c3 > c8 and c3 > c9):
        print("---------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 3")
    elif(c4 > c0 and c4 > c1 and c4 > c2 and c4 > c3 and c4 > c5 and c4 > c6 and c4 > c7 and c4 > c8 and c4 > c9):
        print("---------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 4")
    elif(c5 > c0 and c5 > c1 and c5 > c2 and c5 > c3 and c5 > c4 and c5 > c6 and c5 > c7 and c5 > c8 and c5 > c9):
        print("---------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 5")
    elif(c6 > c0 and c6 > c1 and c6 > c2 and c6 > c3 and c6 > c4 and c6 > c5 and c6 > c7 and c6 > c8 and c6 > c9):
        print("---------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 6")
    elif(c7 > c0 and c7 > c1 and c7 > c2 and c7 > c3 and c7 > c4 and c7 > c5 and c7 > c6 and c7 > c8 and c7 > c9):
        print("---------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 7")
    elif(c8 > c0 and c8 > c1 and c8 > c2 and c8 > c3 and c8 > c4 and c8 > c5 and c8 > c6 and c8 > c7 and c8 > c9):
        print("---------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 8")
    elif(c9 > c0 and c9 > c1 and c9 > c2 and c9 > c3 and c9 > c4 and c9 > c5 and c9 > c6 and c9 > c7 and c9 > c8):
        print("-----------------------------------------\n")
        print("La imagen ingresada es de clase  ---> 9")
    print("\n\n")  
#-----------------------------------------------------------------------------------#
#                                                                                   #
# NOMBRE : Funcion ordenar_distancia                                                #
# DESCRIPCION : ordena las distancias y sus instancias para mostrarlas              #
# PARAMETROS : list lista                                                           #
# RETORNO :  none                                                                   #
#                                                                                   #
#-----------------------------------------------------------------------------------#
def ordenar_distancias(lista):
    for z in range(len(lista)):#recorremos toda la lista
        for i in range(len(lista)-1):#la recorremos una vez mas pero hasta el tamanio menos 1
            if(lista[i][1] > lista[i+1][1]):#comparamos si el siguiente numero es mayor
                aux = lista[i]#guardamos la fila en una variable auxiliar
                lista[i] = lista[i+1]#la lista en la posicion actual la cambiamos por la posicion siguiente
                lista[i+1] = aux#la lista en la posicion siguiente la cambiamos por la fila de aux
    conta = 1
    for j in range(len(lista)):
        print("No. --> "+str(conta)+"\tinstancia --> "+str(lista[j][0])+"\tclase --> "+str(lista[j][2])+"\tdistancia --> "+str(lista[j][1]))
        conta+=1
#llamada el metodo menu, el cual inicia la ejecucion del programa
menu()