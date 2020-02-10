from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import re

root = Tk()

#	= Pruebas para el circular = 
#	
# ...,1,2,*3,4,5,1,2,3,4,5,... | 5
# ...,1,*2,3,1,2,3,... | 3
#
# ...,-1,2,*3,-1,2,3,-1,2,3,-1,... | 3
# ...,*-4,0,3,2,0,-1,-4,0,3,2,0,-1,... | 6
#
#	= Pruebas Periodica =
#
# ...,1,*-6,1,-6,...	| 2
# 10,2,*8,-2
#
#	= Pruebas Normales
#
# 3,*5,-1,0.5,4,0,11
# -1,0,*2,5
#
#		== UPDATES ==
#
#	>Ya no es necesario limpiar, solo para quitar texto de los campos
#	>Ya funcionan los flotantes
#	#	IMPORTANTE
#	>En las entradas periodicas se necesita OBLIGATORIAMENTE poner 3 puntos al inicio y al final con sus respectivas comas xd
#	...,1,*-6,1,-6,...
#	^^^            ^^^
#	>con_lista_aux manda 3 veces el periodo de la convolucion periodica xD en una lista
#	>Moví los botones para no hacer mas larga la interfaz
#

Xn = []
Hn = []
matrizTotal = [[]]
entradaXn = StringVar()
entradaHn = StringVar()

entradaNx = StringVar()
entradaNh = StringVar()

# ConvCircular
bConv = False

# ConvPeriodica
bConvPe = False

varCir = IntVar()

root.title("Convolucion Discreta")

# ==============================================

myFrame = Frame(root, width = 500, height = 520)
myFrame.pack()

labelTitle = Label(myFrame, text="Convolucion Discreta", font=("Quicksand",18))
labelTitle.place(x=120,y=10)

labelIns = Label(myFrame,text="Indicar el centro de la funcion con el simbolo '*'",font=("Quicksand",14))
labelIns.place(x=30, y=50)

labelXn = Label(myFrame, text="Introduce x(n):", font=("Quicksand",12))
labelXn.place(x=10, y=120)

txtXn = Entry(myFrame,width = 57,textvariable = entradaXn )
txtXn.place(x=10,y=140)

labelHn = Label(myFrame, text="Introduce h(n):", font=("Quicksand",12))

txtHn = Entry(myFrame,width = 57,textvariable = entradaHn)

labelNx = Label(root,text="Nx : ",font=("Quicksand",12))
txtNx = Entry(myFrame,width = 10,textvariable = entradaNx,state='disabled')

labelNh = Label(root,text="Nh : ",font=("Quicksand",12))
txtNh = Entry(myFrame,width = 10,textvariable = entradaNh, state='disabled')

labelNx.place(x=10, y=170)
txtNx.place(x=50, y=170)

labelNh.place(x=10, y=260)
txtNh.place(x=50, y=260)

lablelConv = Label(root,text="",font=("Quicksand",12))

buttonCal = Button(root,text="Calcular",font=("Quicksand",12),command=lambda:calculaConv(txtXn.get(),txtHn.get()))

buttonLimp = Button(root,text="Limpiar",font=("Quicksand",12),command=lambda:limpiar())

buttonGrafS = Button(root,text="Salida",font=("Quicksand",12),command=lambda:graficaSalida(calculaConv(txtXn.get(),txtHn.get())))

buttonGrafE = Button(root,text="Entrada",font=("Quicksand",12),command=lambda:graficaIn(txtXn.get(),txtHn.get()))


labelHn.place(x=10, y=210)
txtHn.place(x=10,y=230)
lablelConv.place(x=10,y=340)
buttonCal.place(x=30,y=300)
buttonLimp.place(x=130,y=300)
buttonGrafS.place(x=230,y=300)
buttonGrafE.place(x=320,y=300)
# ==============================================

def redondear(x):
    n = int(x)
    return n if n-1 < x <= n else n+1

#	Funcion para habilitar o deshabilitar los campos de texto
def bloquearTxt(xd):
	global bConv
	global bConvPe

	if xd == 0:
		txtNx.config(state='disabled') 
		txtNh.config(state='disabled') 
		bConv = False
		bConvPe = False

	elif xd == 1:
		txtNx.config(state='normal')
		txtNh.config(state='normal')
		bConv = True
		bConvPe = False
		
	elif xd == 2:
		txtNx.config(state='normal')
		txtNh.config(state='disabled') 
		bConv = False
		bConvPe = True

#	Convolucion Normalona
convCir = Radiobutton(myFrame,text="Conv. Normal", variable = varCir, value = 0, command = lambda:bloquearTxt(0))
convCir.place(x=10, y=90)

#	Convolucion Circular
convCir = Radiobutton(myFrame,text="Conv. Circular", variable = varCir, value = 1, command = lambda:bloquearTxt(1) )
convCir.place(x=140, y=90)

#	Convolución Periodica
convCir = Radiobutton(myFrame,text="Conv. Periodica", variable = varCir, value = 2, command = lambda:bloquearTxt(2) )
convCir.place(x=270, y=90)

def calculaConv(xn,hn):
	global matrizTotal
	global Xn 
	global Hn
	global bConv
	global bConvPe

	conv_lista_aux = []
	i_c_aux = 0
	convLista = []
	aux_row = []
	convListaCir = []

	# ==============================================
	
	#Guardamos las listas generadas del string para crear la matriz
	Xn = creaLista(xn)
	print(Xn)
	Hn = creaLista(hn)
	print(Hn)

	#Si es convolucion circular, en Xn y Hn guardamos los periodos y la primera fase del metodo es el mismo
	if bConv:
		Xn = separaPeriodos(Xn,int(txtNx.get()))
		Hn = separaPeriodos(Hn,int(txtNh.get()))

	#Si es convolucion periodica, solo obtenemos el periodo de Xn
	#Se realiza la convolución normal
	if bConvPe:
		Xn = separaPeriodos(Xn,int(txtNx.get()))

	#Guardamos el tamanio de ambas listas para no llamar a "len()"
	len_Xn = len(Xn)
	len_Hn = len(Hn)

	#Se obtiene el tamanio final de la lista de convolucion
	convLen = len_Xn + len_Hn - 1

	# ==============================================
	#				CONVOLUCION (convLista)

	if len_Xn > len_Hn:
		multFunc(Xn,Hn,False)
		#Se realiza la suma de las columnas j veces, que es el tamanio del renglon
		for j in range(convLen):
			convLista.append( sumaColumna(j,len_Hn) )
	elif len_Xn < len_Hn:
		multFunc(Hn,Xn,False)
		for j in range(convLen):
			convLista.append( sumaColumna(j,len_Xn) )
	elif len_Xn == len_Hn:
		multFunc(Xn,Hn,True)
		for j in range(convLen):
			convLista.append( sumaColumna(j,len_Hn) )

	print(matrizTotal)

	# ==============================================

	# Obtenemos el indice central de la convolucion
	i_c = indiceConv(xn,hn)

	# Obtenemos el indice de la convolcon periodica
	if bConvPe:
		i_c_aux = (i_c % int(txtNx.get())) + 1

	# ==============================================

	# Si es circular lo mandamos a la fase 2
	if bConv:
		#Le restamos 2 para quitar los "..." que se han tomado como elementos
		i_c -= 2
		#De acuerdo al perido más grande se manda a la funcion
		if int(txtNx.get()) > int(txtNh.get()):
			convListaCir = fase2(convLista,int(txtNx.get()))
		elif int(txtNx.get()) < int(txtNh.get()):
			convListaCir = fase2(convLista,int(txtNh.get()))
		else:
			#Si son iguales
			convListaCir = fase2(convLista,int(txtNh.get()))
		#Se asigna el nuevo centro xd
		convListaCir[i_c] = "*" + str(convListaCir[i_c])

	# ==============================================

	#Guardar numero sin asterisco
	num_aux = convLista[i_c]
	#Poner asterisco en la convolución
	convLista[i_c] = "*" + str(convLista[i_c])
	print(convLista)

	lablelConv.config(text="Convolucion: \n\n"+str(convLista))
	
	#				FIN CONV (normal)
	# ==============================================

	# Se limpia para que ya no le piques xd
	Xn = []
	Hn = []
	matrizTotal = [[]]

	# ==============================================

	if bConvPe:
		#Quitamos el asterisco y dejamos solo el numero
		convLista[i_c] = num_aux

		#Si es convolucion Periodica se realiza al funcion que retorna una lista con el
		#resultado de la suma por columnas
		conv_lista_aux = sumaXcolumnas(int(txtNx.get()),convLista)
		
		#Aumentamos 3 periodos mas a la suma
		conv_lista_aux = conv_lista_aux + conv_lista_aux + conv_lista_aux

		#Colocamos el asterisco a los 3 periodos anteriores
		conv_lista_aux[i_c_aux] = "*" + str(conv_lista_aux[i_c_aux])

		#Colocamos el asterisco a la convolución original
		convLista[i_c_aux] = "*" + str(convLista[i_c_aux])
		lablelConv.config(text="Convolucion: \n\n"+str(convLista)+"\n\n Suma por Columnas: \n\n "+str(conv_lista_aux))

	# ==============================================

	#Se imprime de más el y(n)
	if bConv:
		lablelConv.config(text="Convolucion: \n\n"+str(convLista)+"\n\ny(n) = "+str(convListaCir))
		return convListaCir
	else:
		return convLista

def matrix(datos):
	print(datos)
	tam = len(datos)
	newList = []
	strg = StringVar()
	for x in datos:
		strg = str(x)
		print(strg)

		for e in strg:	
			if(e == '*'):
				strg = strg.replace('*','')

		aux = float(strg)
		newList.append(aux)

	return newList

def centro(strg):
	indice_conv = 0
	cont = 0

	for i in strg:
		if(i == "*"):
			indice_conv = cont
		if(i == ","):
			cont += 1
	return indice_conv

def graficaSalida(dtS):
	dSy = matrix(dtS)
	dtS = listToString(dtS)
	c = centro(dtS)
	inicio = 0 - c
	fin = len(dSy) - c
	dSx = np.arange(inicio,fin,1)
	
	plt.figure('Grafica Salida')
	plt.stem(dSx,dSy, use_line_collection = True)
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('Xn * Hn')
	plt.show()


def graficaIn(dtXn, dtHn):
	dtXn = dtXn + ","
	dtXn = creaLista(dtXn)
	dXy = matrix(dtXn)
	dtXn = listToString(dtXn)
	cX = centro(dtXn)
	iX = 0 - cX
	fX = len(dXy) - cX
	dXx = np.arange(iX,fX,1)

	dtHn = dtHn + ","
	dtHn = creaLista(dtHn)
	dHy = matrix(dtHn)
	dtXn = listToString(dtHn)
	cH = centro(dtHn)
	iH = 0 - cH
	fH = len(dHy) - cH
	dHx = np.arange(iH,fH,1)

	plt.figure('Graficas de entrada')
	plt.subplot(1,2,1)
	plt.stem(dXx,dXy, use_line_collection = True)
	plt.title('Grafica Xn')
	plt.subplot(1,2,2)
	plt.stem(dHx,dHy, use_line_collection = True)
	plt.title('Grafica Hn')
	plt.show()

def listToString(s):
	str1 = ','.join([str(elem) for elem in s])
	return str1

#	Fucion que multiplica 2 listas pero F1 tiene que ser mayor que F2
def multFunc(*argv):
	global matrizTotal
	matrizTotal = [[]]

	lenF1 = argv[0]
	lenF2 = argv[1]

	aux = 0
	x = 0
	y = 0

	#print(lenF1)
	#print(lenF2)

	convLen_ = len(lenF1) + len(lenF2) - 1

	#Creando un arreglo bidimencional lleno de 0's
	matrizTotal = [[0] * convLen_ for z in range( len(lenF2) )]

	#Guardando la multiplicacion de cada elemento de Hm por todos los elementos de Xn
	for i in lenF2:
		for k in lenF1:
			aux = float(i) * float(k)
			#Guardando de acuerdo al renglon, al inicio el resultado se pone en la posicion 0
			#despues el resultado empieza a ponerse en 1, después en 2 y así
			matrizTotal[x][y+x] = aux
			#Cambia de columna
			y += 1
		#Cambia de renglon
		x += 1
		#Reinicia la columna
		y = 0

# Funcion que realiza la suma por columnas de la convolucion periodica
def sumaXcolumnas(p,conv):
	matriz = [[]]
	cont = 0
	periodoN = []

	#Llenamos de 0 la nueva lista que es periodo de la nueva convolucion
	for d in range(p):
		periodoN.append(0)

	print(periodoN)

	# x es el numero de renglones de la suma
	x = int( redondear(len(conv)/p) )

	#Creamos la Matriz de suma
	matriz = [[0] * p for z in range( x )]

	#Asignamos la conv a la nueva matriz de acuerdo al periodo
	for i in range(x):	
		for j in range(p):
			if cont < len(conv):
				matriz[i][j] = conv[cont]
				cont += 1
				print(cont)
				print("Matriz loka:")
				print(matriz)

	#Sumamos ALV
	for a in range(p): 	#Ancho
		for b in range(x):	#Largo
			periodoN[a] = periodoN[a] + matriz[b][a]
			print("Periodo: "+str(periodoN))

	print(periodoN)
	return periodoN


#	Funcion que suma las columnas de las matrices
def sumaColumna(numColumna,tamCna):
	global matrizTotal

	sum_ = 0

	for i in range(tamCna):
		#Bajamos de renglon para sumar los valores que estan en "numColumna"
		sum_ = sum_ + matrizTotal[i][numColumna]
		#print(sum_)

	return sum_

#	Funcion que obtiene el indice de la convolucion
def indiceConv(xn_,hn_):
	#Tomamos las entradas de string de H(n) y X(n)
	indice_x = 0
	indice_h = 0
	indice_conv = 0
	cont = 0

	#Contamos por comas para diferenciar los elementos
	for i in xn_:
		#Guardamos el indice donde se encuentre el "*"
		if(i == "*"):
			indice_x = cont
		if(i == ","):
			cont += 1

	cont = 0

	#Lo mismo para H(n)
	for j in hn_:
		if(j == "*"):
			indice_h = cont
		if(j == ","):
			cont += 1

	#Para sacar el indice de convolucion se suma ambos indices de xn y hn
	indice_conv = indice_x + indice_h
	print("Indice Conv: "+str(indice_conv))

	return indice_conv

#Funcion que toma n elementos de "lista" y retorna una nueva lista con n elementos
#
#	== SOLO TOMA LOS PRIMEROS N ELEMENTOS DEL ARREGLO ==
#	== NO IDENTIFICA EL PERIODO AUTOMATICAMENTE (no pude xd)==
def separaPeriodos(lista,n):

	nuevaLista = []

	for i in range(len(lista)):
		#Mientras sea menor se guarda cada elemento
		if i < n:	
			nuevaLista.append(lista[i])
		#Cuando es mayor, se acaba el periodo deseado, asi que lo mandamoooosh
		else:
			return nuevaLista

#Funcion de la fase 2, donde tomamos el periodo de la primera fase y lo sumamos con los elementos
#restantes y así obtenemos el periodo de la convolución
#	_______________________
#	4 -8 -15 4 13 7  -2 -3 (0) (0) (0) (0) ....... (f1)
#  |---------------||---------------------|
#	  Periodo (n) 	       Restantes
#
#Los paramtros son la convolucion de la fase1 (f1) y el tamaño del periodo mas grande
def fase2(listaConv,n):

	sobrantes = []
	nuevaLista = []

	#Empezamos por el n (tamaño del periodo) para que lo siguiente sean los elementos restantes
	for i in range(n,len(listaConv)):
		sobrantes.append(listaConv[i])

	#A la convolucion de la primera fase al tamaño del periodo mas grande le restamos el tamaño de la lista de 
	#los elementos restantes y así completamos con 0's para sumar
	#	 -2 -3 (0) (0) (0) (0)
	#	|---------------------|
	#		Restantes xd
	for j in range(n-len(sobrantes)):
		sobrantes.append(0)

	#Para todo el periodo se suma uno por uno con los restantes y se guarda en una nueva lista
	for k in range(n):
		nuevaLista.append(int(sobrantes[k])+int(listaConv[k]))

	return nuevaLista

#	Funcion que convierte la string de entrada a una lista de numeros
def creaLista(strg):

	strg = strg + ","

	newList = []
	aux = ""
	a = 0

	for k in range(len(strg)-1):
		#Consideramos que la posicion actual no es una coma, ni asterisco, ni punto xd
		if strg[k] != "," and strg[k] != "*":

			if a == 2 or a == 1:
				a -= 1
				continue

			if k == len(strg)-4 or k == 0:
				aux_p = strg[k] + strg[k+1] + strg[k+1]
				print("aux_p: "+aux_p)
				if aux_p == "...":
					a = 2
					continue

			#Si no es una coma, verificamos que el siguiente caracter no sea una coma
			#si el siguiente no es una coma signfica que es un numero de mas de 1 digito
			# 	1 , 23 , 456
			#	^   ^^   ^^^
			if strg[k+1] != ",":
				#Si es mas de un digito, cada digito lo guardamos en la variable aux
				aux = aux + strg[k]
				#Salimos del for para no asignar nada a la lista aun
				continue
			#Si el siguiente caracter es una coma, significa que el numero ya acabo
			aux = aux + strg[k]
			#Agregamos a la lista
			newList.append(aux)
			#Limpiamos
			aux = ""

	return newList

def limpiar():

	lablelConv.config(text="")
	entradaXn.set("")
	entradaHn.set("")
	entradaNx.set("")
	entradaNh.set("")

root.mainloop()

