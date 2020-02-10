# Convoluciones
Teoría de comunicaciones y señales - ESCOM

Programa que calcula convoluciones en tiempo discreto entre ellas
-Convolucion Circular
-Convolucion Periodica
-Convolucion Normal

El programa necesita la libreria tkinter y matplotlib

	= Pruebas para el circular = 
	
 ...,1,2,*3,4,5,1,2,3,4,5,... | 5
 ...,1,*2,3,1,2,3,... | 3

 ...,-1,2,*3,-1,2,3,-1,2,3,-1,... | 3
 ...,*-4,0,3,2,0,-1,-4,0,3,2,0,-1,... | 6

	= Pruebas Periodica =

 ...,1,*-6,1,-6,...	| 2
 10,2,*8,-2

	= Pruebas Normales

 3,*5,-1,0.5,4,0,11
 -1,0,*2,5

		== UPDATES ==

	>Ya no es necesario limpiar, solo para quitar texto de los campos
	>Ya funcionan los flotantes
# IMPORTANTE
	>En las entradas periodicas se necesita OBLIGATORIAMENTE poner 3 puntos al inicio y al final con sus respectivas comas xd
	...,1,*-6,1,-6,...
	^^^            ^^^
	>con_lista_aux manda 3 veces el periodo de la convolucion periodica xD en una lista
	>Moví los botones para no hacer mas larga la interfaz

