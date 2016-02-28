#########################################################################
#																		#
#				PROGRAMA PARA REALIZAR EL RECONOCIMIENTO				#
#						DE IMAGENES MEDIANTE OCR						#
#																		#
#					ELABORADO POR: MARCOS, ROBERTO						#
#																		#
#########################################################################

#################################################################################
#																				#		
#			DESCRIPCION DE LOS ATRIBUTOS DE LAS INSTANCIAS 						#
#																				#
#  atributo 0 = numero consecutivo												#
#  atributo 1 = numero de columnas / numero de filas 							#
#  atributo 2 = numero de 1's / tamanio de la imagen(filas * columnas) 			#
#  atributo 3 = numero de 1's que hay en la columna de enmedio 					#
#  atributo 4 = numero de 1's que hay en la columna a un cuarto 				#
#  atributo 5 = numero de 1's que hay en la columna entre 4 * 3 				#
#  atributo 6 = numero de 1's que hay en la fila de enmedio 					#
#  atributo 7 = numero de 1's que hay en la fila a un cuarto 					#
#  atributo 8 = numero de 1's que hay en la fila entre 4 * 3 					#
#  atributo 9 = numero de cortes que hay en la columna de enmedio 				#
#  atributo 10 = numero de cortes que hay en la columna a un cuarto 			#
#  atributo 11 = numero de cortes que hay en la columna entre 4 * 3 			#
#  atributo 12 = numero de cortes que hay en la fila de enmedio 				#
#  atributo 13 = numero de cortes que hay en la fila a un cuarto 				#
#  atributo 14 = numero de cortes que hay en la fila entre 4 * 3 				#
#  atributo 15 = clase a la que pertenecen 										#
#																				#	
#################################################################################

#librerias ocupadas en el programa
import os
import matplotlib.image as im
from PIL import Image as IM
import csv,random,math,operator
from time import time
#####################################################################################
#																					#
# NOMBRE : funcion main 															#
# DESCRIPCION : es la primera en ejecutarse y llama a la funcion proceso			#
# PARAMETROS : ninguno																#
# RETORNO : ninguno																	#
# 																					#
#####################################################################################
def menu():

	hola = """
#########################################################
#
#   PROGRAMA PARA REALIZAR EL METODO OCR DE IMAGENES
#
#     		ELABORADO POR: ROBERTO, MARCOS
#			8 B
#	    	MINERIA DE DATOS
#                      2016
# 														
#########################################################
"""
	print(hola)
	repetir = 1
	while(repetir == 1):
		print("\nMenu de opciones\n1 --> Generar el archivo .csv\n2 --> Aplicar el OCR mediante KNN")
		opcion = int(input('------>  '))
		if(opcion == 1):	
			path = input('Ingresa la ruta de la carpeta padre\n')
			load(path)#llamamos al metodo load pasando como parametro la ruta del directorio
		elif(opcion == 2):
			knn()
		else:
			print("Ha ingresado una opcion incorrecta")
			menu()
		print("Desea ejecutar de nuevo el programa??\n1 --> Si\n2 --> No")
		repetir = int(input('---->  '))
	print("Programa finalizado, elaborado por: Roberto, Marcos\n\t\t8 B")
#####################################################################################
#																					#
# NOMBRE : funcion load 															#
# DESCRIPCION : leer las carpetas y los archivos dentro de la carpeta padre			#
# PARAMETROS : string padre, es la ruta del directorio padre 						#
# RETORNO : ninguno																	#
# 																					#
#####################################################################################
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

#####################################################################################
#																					#
# NOMBRE : funcion leer																#
# DESCRIPCION : abre todas las imagenes con las rutas obtenidas anteriormente		#
# PARAMETROS : list de todas las rutas de las imagenes		 						#
# RETORNO : ninguno																	#
# 																					#
#####################################################################################
def leer(rutas):

	#para saber el tiempo en que inicio el proceso
	inicio = time()
	archivo = input('Escribe el nombre del archivo para guardar los datos\n');
	n_archivo = archivo + ".csv"
	abrir = open(n_archivo,'w')#abrimos el archivo para escribir
	#para escribir el el archivo csv
	csvsalida = open(n_archivo, 'w', newline='')
	escribir = csv.writer(csvsalida)
	#recorremos todas las imagenes para sacar sus atributos
	print("Escribiendo las caracteristicas en el archivo csv")
	print("Sea paciente, este proceso puede llevar unos minutos")
	t = 0#variable total de instancias escritas
	carpeta = -1#para indicar el proceso	
	for i in range(len(rutas)):
		instancias = []#lista para los atributos por cada instancia
		img=im.imread(rutas[i])#abrir la imagen con este metodo para tener acceso a la matriz
		img1 = IM.open(rutas[i])#abrir la imagen con este metodo para tener acceso al metodo para calcular filas y columnas
		col, filas = img1.size#obtenemos el tamanio de cada imagen
		instancias.append(i+1)#atributo 0
		instancias.append(atr1(filas,col))#atributo 1
		instancias.append(atr2(img,filas,col))#atributo 2
		#lista con los resultados de los atributos de las columnas
		r_col = atrcolumnas(img, filas, col)
		#lista con los resultados de los atributos de las filas
		r_filas = atrfilas(img, filas, col)
		instancias.append(r_col[0])#atributo 3
		instancias.append(r_col[1])#atributo 4
		instancias.append(r_col[2])#atributo 5
		instancias.append(r_filas[0])#atributo 6
		instancias.append(r_filas[1])#atributo 7
		instancias.append(r_filas[2])#atributo 8
		instancias.append(r_col[3])#atributo 9
		instancias.append(r_col[4])#atributo 10
		instancias.append(r_col[5])#atributo 11
		instancias.append(r_filas[3])#atributo 12
		instancias.append(r_filas[4])#atributo 13
		instancias.append(r_filas[5])#atributo 14
		#del numbre de la ruta, tomamos el nombre de la carpeta
		#que este caso esta en la posicion 6
		#y este es la clase a la que pertenece
		instancias.append(int(rutas[i][6]))#atributo 15
		#guardamos en una lista nueva los renglones a escribir en el archivo
		data = [(instancias[0],instancias[1],instancias[2],instancias[3],instancias[4],instancias[5],instancias[6],instancias[7],instancias[8],instancias[9],instancias[10],instancias[11],instancias[12],instancias[13],instancias[14],instancias[15])]
		escribir.writerows(data)
		t = i+1
		#mostramos el proceso actual de la operacion
		if(carpeta != int(rutas[i][6])):
			carpeta +=1
			print("\nProgreso actual = escribiendo datos de la carpeta ---> "+str(rutas[i][6]))
			print("Progreso total global ---> "+str(carpeta)+str("0%"))
		#fin del for total
	csvsalida.close()
	fin = time()
	print("Progreso total global ---> 100%")
	tt =  ((fin - inicio)/60)
	print("\n\nTiempo de procesamiento de las imagenes =  %.2f minutos." % tt)
	print("\nProceso terminado, se han escrito "+str(t)+" instancias en el archivo "+ str(n_archivo)+"\n\n")

#####################################################################################
#																					#
# NOMBRE : funcion atr1																#
# DESCRIPCION : calcula el valor de las filas entre las columnas de cada imagen		#
# PARAMETROS : int col, int filas							 						#
# RETORNO : float filas/columnas													#
# 																					#
#####################################################################################
def atr1(filas, col):

	return float(filas)/float(col)
#####################################################################################
#																					#
# NOMBRE : funcion atr2																#
# DESCRIPCION : calcula los 1's entre el tamanio de la imagen 						#
# PARAMETROS : array img, int filas, int col				 						#
# RETORNO : int unos 																#
# 																					#
#####################################################################################
def atr2(img, filas, col):
	
	unos = 0
	for i in range(filas):
		for j in range(col):
			if(img[i][j] == 1):
				unos+=1
	return unos/(filas*col)

#####################################################################################
#																					#
# NOMBRE : funcion atrcolumnas														#
# DESCRIPCION : calcula los atributos indicados en las columnas						#
# PARAMETROS : array img, int filas, int col				 						#
# RETORNO : atri3, atri4, atri5, atri 9, atri10, atr11								#
# 																					#
#####################################################################################
def atrcolumnas(img, filas, col):

	#contadores de cada atributo
	atri3 = atri4 = atri5 = 0
	#condiciones de cada atributo
	condicion_atri3 = int(col/2)
	condicion_atri4 = int(col/4)
	condicion_atri5 = int((col/4)*3)
	#listas para calcular los cortes
	lista1 = []
	lista2 = []
	lista3 = []
	#recorremos toda la imagen y comparamos
	for i in range(filas):
		for j in range(col):
			if(j == condicion_atri3):
				lista1.append(img[i][j])#agregamos el valor en una lista, dependiendo la condicion
				if(img[i][j] == 1):
					atri3+=1
			if(j == condicion_atri4):
				lista2.append(img[i][j])
				if(img[i][j] == 1):
					atri4+=1
			if(j == condicion_atri5):
				lista3.append(img[i][j])
				if(img[i][j] == 1):
					atri5+=1
	#valor inicial para calcular los cortes
	inicio1 = lista1[0]
	inicio2 = lista2[0]
	inicio3 = lista3[0]
	#contadores de cada corte
	c_corte1 = 0
	c_corte2 = 0
	c_corte3 = 0
	#condicion para los cortes
	if(lista1[0] == 1):
		c_corte1+=1
	if(lista2[0] == 1):
		c_corte2+=1
	if(lista3[0] == 1):
		c_corte3+=1
	if(lista1[len(lista1)-1] == 1):
		c_corte1+=1
	if(lista2[len(lista1)-1] == 1):
		c_corte2+=1
	if(lista3[len(lista1)-1] == 1):
		c_corte3+=1
	#recorremos la lista de las columna y calculamos los cortes
	for l in range(len(lista1)):
		if(inicio1 != lista1[l]):
			inicio1 = lista1[l]
			c_corte1+=1
		if(inicio2 != lista2[l]):
			inicio2 = lista2[l]
			c_corte2+=1
		if(inicio3 != lista3[l]):
			inicio3 = lista3[l]
			c_corte3+=1
	atributos_col = [atri3, atri4, atri5, c_corte1, c_corte2, c_corte3]
	return atributos_col

#####################################################################################
#																					#
# NOMBRE : funcion atrfilas															#
# DESCRIPCION : calcula los atributos indicados en las filas						#
# PARAMETROS : array img, int filas, int col				 						#
# RETORNO : int atri6, atri7, atri8, atri12, atri13, atri4							#
# 																					#
#####################################################################################
def atrfilas(img, filas, col):

	#contadores de cada atributo
	atri6 = atri7 = atri8 = atri12 = atri13 = atri14 = 0
	#condiciones de cada atributo
	condicion_atri6 = int(filas/2)
	condicion_atri7 = int(filas/4)
	condicion_atri8 = int((filas/4)*3)
	#listas para calcular los cortes
	lista1 = []
	lista2 = []
	lista3 = []
	#recorremos toda la imagen y comparamos
	for i in range(filas):
		for j in range(col):
			if(i == condicion_atri6):
				lista1.append(img[i][j])#agregamos el valor en una lista, dependiendo la condicion
				if(img[i][j] == 1):
					atri6+=1
			if(i == condicion_atri7):
				lista2.append(img[i][j])#agregamos el valor en una lista, dependiendo la condicion
				if(img[i][j] == 1):
					atri7+=1
			if(i == condicion_atri8):
				lista3.append(img[i][j])#agregamos el valor en una lista, dependiendo la condicion
				if(img[i][j] == 1):
					atri8+=1
	#valor inicial para calcular los cortes
	inicio1 = lista1[0]
	inicio2 = lista2[0]
	inicio3 = lista3[0]
	#contadores de cada corte
	c_corte1 = c_corte2 = c_corte3 = 0
	#condicion para los cortes
	if(float(lista1[0]) == 1.0):
		c_corte1+=1
	if(float(lista2[0]) == 1.0):
		c_corte2+=1
	if(float(lista3[0]) == 1.0):
		c_corte3+=1
	if(float(lista1[len(lista1)-1]) == 1.0):
		c_corte1+=1
	if(float(lista2[len(lista1)-1]) == 1.0):
		c_corte2+=1
	if(float(lista3[len(lista1)-1]) == 1.0):
		c_corte3+=1
	#recorremos la lista de las columna y calculamos los cortes
	for l in range(len(lista1)):
		if(inicio1 != lista1[l]):
			inicio1 = lista1[l]
			c_corte1+=1
		if(inicio2 != lista2[l]):
			inicio2 = lista2[l]
			c_corte2+=1
		if(inicio3 != lista3[l]):
			inicio3 = lista3[l]
			c_corte3+=1
	atributos_filas = [atri6, atri7, atri8, c_corte1, c_corte2, c_corte3]
	return atributos_filas

#####################################################################################
#																					#
# NOMBRE : funcion knn																#
# DESCRIPCION : calcular el metodo KNN 												#
# PARAMETROS : ninguno										 						#
# RETORNO :  ninguno 								 								#
# 																					#
#####################################################################################
def knn():

	print("Aplicando el metodo KNN para el reconocimiento de imagenes OCR")
	print("Ingrese la ruta del archivo csv")
	ruta = input('----->  ')+".csv"
	#ruta = 'dataset.csv'
	print("Ingrese la ruta de la imagen que desea reconocer")
	r_imagen = input('----->  ')+".png"
	r = "test/"+r_imagen
	nueva = carac_imagen(r)
	leer_data(ruta,nueva)

#####################################################################################
#																					#
# NOMBRE : funcion carac_imagen														#
# DESCRIPCION : calcular los atributos de la imagen nueva							#
# PARAMETROS : string r_imagen								 						#
# RETORNO :  list datos(datos de la imagen nueva)	 								#
# 																					#
#####################################################################################
def carac_imagen(r_imagen):

	datos = []
	img=im.imread(r_imagen)#abrir la imagen con este metodo para tener acceso a la matriz
	img1 = IM.open(r_imagen)#abrir la imagen con este metodo para tener acceso al metodo 
	col, filas = img1.size#obtenemos el tamanio de cada imagene
	datos.append(atr1(filas,col))#atributo 1
	datos.append(atr2(img,filas,col))#atributo 2
	#lista con los resultados de los atributos de las columnas
	r_col = atrcolumnas(img, filas, col)
	#lista con los resultados de los atributos de las filas
	r_filas = atrfilas(img, filas, col)
	datos.append(r_col[0])#atributo 3
	datos.append(r_col[1])#atributo 4
	datos.append(r_col[2])#atributo 5
	datos.append(r_filas[0])#atributo 6
	datos.append(r_filas[1])#atributo 7
	datos.append(r_filas[2])#atributo 8
	datos.append(r_col[3])#atributo 9
	datos.append(r_col[4])#atributo 10
	datos.append(r_col[5])#atributo 11
	datos.append(r_filas[3])#atributo 12
	datos.append(r_filas[4])#atributo 13
	datos.append(r_filas[5])#atributo 14
	return datos

#####################################################################################
#																					#
# NOMBRE : funcion leer_data														#
# DESCRIPCION : lee el archivo csv y llama al metodo para calcular sus distancias	#
# PARAMETROS : string ruta, list x(datos de la imagen a calcular)					#
# RETORNO :  list distancia(la distancia de todas las instancias)					#
# 																					#
#####################################################################################
def leer_data(ruta,x):

	read = csv.reader(open(ruta,'r'))
	datos_distancia = []
	dis = 0
	for index,row in enumerate(read):
		#aqui sacamos los datos de cada renglon y los pasamos como parametros para la funcion de calcular distancia
		y = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]),float(row[12]),float(row[13]),float(row[14])]
		dis = distancia(x,y)
		atri = []
		atri.append(int(index+1))
		atri.append(dis)
		atri.append(int(row[15]))
		datos_distancia.append(atri)
	vecinos(datos_distancia,ruta)
#####################################################################################
#																					#
# NOMBRE : funcion distancia														#
# DESCRIPCION : calcula las distancias de una instancia 							#
# PARAMETROS : list x(instancia a calcular), list y(instancia de cada renglon)		#
# RETORNO :  float distancia 														#
# 																					#
#####################################################################################
def distancia(x,y):

	total = 0.0
	for i in range(len(x)):
		total+=((float(x[i])-float(y[i]))**2)
	return math.sqrt(total)

#####################################################################################
#																					#
# NOMBRE : funcion vecinos															#
# DESCRIPCION : calcula los vecinos mas cercanos y obtiene su clase					#
# PARAMETROS : list datos_distancia, string ruta		 							#
# RETORNO :  ninguno		 														#
# 																					#
#####################################################################################
def vecinos(datos_distancia,ruta):
	print("Ingrese el valor de K")
	k = int(input('----->  '))
	solo_distancias = []#solo almacenara la distancia
	for x in range(len(datos_distancia)):
		solo_distancias.append(datos_distancia[x][1])
	#solo obtener las distancias ordenadas dependiendo de k
	veci = []
	distan = sorted(solo_distancias)
	for i in range(len(distan)):
		if(i == int(k)):
			break
		else:
			veci.append(distan[i])
	#print(veci)
	for z in range(len(datos_distancia)):
		for y in range(len(veci)):
			if(veci[y] == datos_distancia[z][1]):
				print("Instancia numero --> "+str(datos_distancia[z][0]) +" \tdistancia --> "+str(datos_distancia[z][1])+" \tque pertenece a la clase --> "+str(datos_distancia[z][2]))
	#contadores de cada clase
	c0 = c1 = c2 = c3 = c4 = c5 = c6 = c7 = c8 = c9 = c = 0
	read = csv.reader(open(ruta,'r'))#abrimos el archivo
	for index,row in enumerate(read):#recorremos el archivo del dataset
		for j in range(k):#comparamos con cada valor de la lista de vecinos
			if(solo_distancias[c] == veci[j]):#comparaciones para cada clase
				if(int(row[15]) == 0):
					c0+=1
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
	#comparaciones para cada clase
	if(c0 > c1 and c0 > c2 and c0 > c3 and c0 > c4 and c0 > c5 and c0 > c6 and c0 > c7 and c0 > c8 and c0 > c9):
		print("La imagen ingresada es un CERO ---> 0")
	elif(c1 > c0 and c1 > c2 and c1 > c3 and c1 > c4 and c1 > c5 and c1 > c6 and c1 > c7 and c1 > c8 and c1 > c9):
		print("La imagen ingresada es un UNO ---> 1")
	elif(c2 > c0 and c2 > c1 and c2 > c3 and c2 > c4 and c2 > c5 and c2 > c6 and c2 > c7 and c2 > c8 and c2 > c9):
		print("La imagen ingresada es un DOS ---> 2")
	elif(c3 > c0 and c3 > c1 and c3 > c2 and c3 > c4 and c3 > c5 and c3 > c6 and c3 > c7 and c3 > c8 and c3 > c9):
		print("La imagen ingresada es un TRES ---> 3")
	elif(c4 > c0 and c4 > c1 and c4 > c2 and c4 > c3 and c4 > c5 and c4 > c6 and c4 > c7 and c4 > c8 and c4 > c9):
		print("La imagen ingresada es un CUATRO ---> 4")
	elif(c5 > c0 and c5 > c1 and c5 > c2 and c5 > c3 and c5 > c4 and c5 > c6 and c5 > c7 and c5 > c8 and c5 > c9):
		print("La imagen ingresada es un CINCO ---> 5")
	elif(c6 > c0 and c6 > c1 and c6 > c2 and c6 > c3 and c6 > c4 and c6 > c5 and c6 > c7 and c6 > c8 and c6 > c9):
		print("La imagen ingresada es un SEIS ---> 6")
	elif(c7 > c0 and c7 > c1 and c7 > c2 and c7 > c3 and c7 > c4 and c7 > c5 and c7 > c6 and c7 > c8 and c7 > c9):
		print("La imagen ingresada es un SIETE ---> 7")
	elif(c8 > c0 and c8 > c1 and c8 > c2 and c8 > c3 and c8 > c4 and c8 > c5 and c8 > c6 and c8 > c7 and c8 > c9):
		print("La imagen ingresada es un OCHO ---> 8")
	elif(c9 > c0 and c9 > c1 and c9 > c2 and c9 > c3 and c9 > c4 and c9 > c5 and c9 > c6 and c9 > c7 and c9 > c8):
		print("La imagen ingresada es un NUEVE ---> 9")		
#llamada el metodo menu, el cual inicia la ejecucion del programa
menu()