from Tkinter import *
from numpy import *
from random import *
from time import *
from _ast import If
import numpy as np
import time
import threading


largo = 900
ancho = 450
tamJug  = 40 #tamano del jugador
tamBal  = 25 #tamano del jugador
hiloBalon = None
dead=False
pausa=False
MarcaA=0
MarcaB=0
class Balon:
	img = ''
	pasos = 10
	direccion = 0 #0: parado  1-8: moviendose
	x=0
	y=0

	#el cambio se hace aui porque el hilo del balon llama a direccionar y tambien el hilo de cada
	#jugador, eso generaba el problema
	def cambiarDireccion(self,direc): # hace el cambio de direccion
		self.direccion=direc;
		return True

	def sePuedeMover(self, dir): #calcula si puede moverse en cierta posicion
		#prueba si se puede mover y si no corrige (el rebote con las orillas)
		x,y = cancha.coords(self.img) # obtiene las coordenadas del balon
		
		pasos=self.pasos # la distancia (pixeles) que se movera el balon se puede cambiar en los atributos
		
		#Tiene tantos ifs porque considera los casos de rebote en los bordes
		# revisa si puede avanzar y dependiendo de hacia donde no puede y que direcion lleva
		# rebota en una direccion contraria 
		if(dir==1):
			if(y+pasos>0):
				return True
			else:
				self.direccion=5
		elif(dir==2):
			if(y+pasos>0):
				if(x+pasos<largo):return True
				else:#limDer
					self.direccion=8
			else:
				if(x+pasos<largo):#limSup
					self.direccion=4
				else:
					self.direccion=6
		elif(dir==3):
			if(x+pasos<largo):
				return True
			else:
				self.direccion = 7
		elif(dir==4):
			if(y+pasos<ancho) and (x+pasos<largo):return True
			if(y+pasos<ancho):
				if(x+pasos<largo):return True
				else:#limDer
					self.direccion=6
			else:
				if(x+pasos<largo):#limInf
					self.direccion=2
				else:#
					self.direccion=8
		elif(dir==5):
			if(y+pasos<ancho):
				return True
			else: 
				self.direccion=1
		elif(dir==6):
			if(y+pasos<ancho) and (x+pasos>0):return True
			if(y+pasos<ancho):
				if(x+pasos>0):return True
				else:#limIzq
					self.direccion=4
			else:
				if(x+pasos>0):#limInf
					self.direccion=8
				else:#
					self.direccion=2
		elif(dir==7):
			if(x+pasos>0):
				return True
			else:
				self.direccion=3
		elif(dir==8):
			if(y+pasos>0) and (x+pasos>0):return True
			if(y+pasos>0):
				if(x+pasos>0):return True
				else:#limIzq
					self.direccion=2
			else:
				if(x+pasos>0):#limSup
					self.direccion=6
				else:
					self.direccion=4

		return True
	
	def checaGol(self):
		
		if(self.y>150 and self.y<300):
			if(self.x<50):#GOL B
				golAnimation(2)
			elif(self.x>850):#GOL A
				golAnimation(1)

	def direccionar(self): #mueve el jugador
		global dead

		while(not dead):


			if(self.sePuedeMover(self.direccion) and self.direccion!=0):
				#mientras se pueda mover en cierta direccion y la direccion del balon no indique que esta parado (0), se movera
				self.x,self.y = cancha.coords(self.img)
				if(self.direccion==1): #arriba
					cancha.move(self.img,0,-self.pasos) 
				elif(self.direccion==2):#arriba-der
					cancha.move(self.img,+self.pasos,-self.pasos)
				elif(self.direccion==3):#derecha
					cancha.move(self.img,+self.pasos,0)
				elif(self.direccion==4):#abajo-der
					cancha.move(self.img,+self.pasos,+self.pasos)
				elif(self.direccion==5):#abajo
					cancha.move(self.img,0,+self.pasos)
				elif(self.direccion==6):#abajo-izq
					cancha.move(self.img,-self.pasos,+self.pasos)
				elif(self.direccion==7):#izquierda
					cancha.move(self.img,-self.pasos,0)
				elif(self.direccion==8):#arriba-izq
					cancha.move(self.img,-self.pasos,-self.pasos)
				cancha.update()
				sleep(0.05)
				self.checaGol()

class Jugador:
	tipo = ''
	img = ''
	color = ''
	direccion = 0
	pasos = 0
	limSup = 0
	limInf = 0
	limIzq = 0
	limDer = 0

	def __init__(self, x, y, tipo, img, color):
		#constructor de la clase
		self.tipo = tipo
		self.x = x
		self.y = y
		self.color = color
		
		self.limSup = 0
		self.limInf = ancho


		#balon.img = cancha.create_image(balon.x,balon.y,anchor=CENTER,image=ballImgSub)
		if tipo == "delantero":
			self.pasos = 15 #pixeles que se dezplazara el jugador
			if(color =="blue"): #Establece los limites de movimiento segun el tipo de jugador 
				#ijug=PhotoImage(file="jugA.png")
				self.img = cancha.create_image(x,y,anchor=NW,image=img)
				self.limIzq = largo/4+100
				self.limDer = 900-130 
			else:
				self.img = cancha.create_image(x,y,anchor=NW,image=img)
				self.limIzq = 130 
				self.limDer = (largo/4)*3-100
		elif tipo == "defensa":
			self.pasos = 15#pixeles que se dezplazara el jugador
			if(color =="blue"):#Establece los limites de movimiento segun el tipo de jugador 
				self.img = cancha.create_image(x,y,anchor=NW,image=img)
				self.limIzq = 130
				self.limDer = largo/2
			else:
				self.img = cancha.create_image(x,y,anchor=NW,image=img)
				self.limIzq = largo/2
				self.limDer = 900-130
		else:
			self.pasos = 10#pixeles que se dezplazara el jugador
			self.limSup = ancho/2-150 
			self.limInf = ancho/2+150
			if(color =="navy"):#Establece los limites de movimiento segun el tipo de jugador 
				self.img = cancha.create_image(x,y,anchor=NW,image=img)
				self.limIzq = 0
				self.limDer = 130
			else:
				self.img = cancha.create_image(x,y,anchor=NW,image=img)
				self.limIzq = 900-130
				self.limDer = 900


	def mover(self,dir):

		if(dir==1): #arriba
			cancha.move(self.img,0,-self.pasos) 
		elif(dir==2):#arriba-der
			cancha.move(self.img,+self.pasos,-self.pasos)
		elif(dir==3):#derecha
			cancha.move(self.img,+self.pasos,0)
		elif(dir==4):#abajo-der
			cancha.move(self.img,+self.pasos,+self.pasos)
		elif(dir==5):#abajo
			cancha.move(self.img,0,+self.pasos)
		elif(dir==6):#abajo-izq
			cancha.move(self.img,-self.pasos,+self.pasos)
		elif(dir==7):#izquierda
			cancha.move(self.img,-self.pasos,0)
		elif(dir==8):#arriba-izq
			cancha.move(self.img,-self.pasos,-self.pasos)


	#   8  1  2
	#    \ | /
	# 7 ---|--- 3
	#    / | \
	#   6  5  4    
	# Direcciones de movimiento jiji    	

	def sePuedeMover(self,dir): #evalua si el jugador se puede mover en cierta direccion
		x1,y1 = cancha.coords(self.img)
		x2=x1+40
		y2=y1+40
		pasos=self.pasos
		
		if(dir==0): return False
		elif(dir==1):
			if(y1+pasos>self.limSup):return True
		elif(dir==2):
			if(y1+pasos>self.limSup) and (x2+pasos<self.limDer):return True
		elif(dir==3):
			if(x2+pasos<self.limDer):return True
		elif(dir==4):
			if(y2+pasos<self.limInf) and (x2+pasos<self.limDer):return True
		elif(dir==5):
			if(y2+pasos<self.limInf):return True
		elif(dir==6):
			if(y2+pasos<self.limInf) and (x1+pasos>self.limIzq):return True
		elif(dir==7):
			if(x1+pasos>self.limIzq):return True
		elif(dir==8):
			if(y1+pasos>self.limSup) and (x1+pasos>self.limIzq):return True
		
		return False
	
	def colision(self):
		x1,y1= cancha.coords(self.img) #coordenadas distales del jugador
		x=x1+20 # coordenadas centrales
		y=y1+20 #     del jugador
		bx,by = cancha.coords(balon.img) #coordenadas del balon
		dist = sqrt(pow(x-bx,2)+pow(y-by,2))

		if(dist<=40):
			#print("colision()")
			balon.cambiarDireccion(self.direccion)
			#print("("+str(x)+","+str(y)+"):: Color:"+self.color+"   Tipo:"+self.tipo)
			#sleep(100)
	
	def correr(self):
		global dead
		while(not dead):
			
			if(self.direccion!=0): 
				self.direccion=randint(1, 8)

			if self.sePuedeMover(self.direccion):
				#si puede moverse en esa direccion..
				#self.direccion = dir #cambia su direccion
				self.mover(self.direccion) #mueve al jugador
				cancha.update() #actualiza la cancha
				self.colision() #checa si hay colision
			sleep(0.05)

# ELEMENTOS DEL MAPA (cancha, jugadores, balon, etc) #
posInitA = [[325,(ancho/2)-125-tamJug/2],
		   [325,ancho/2-tamJug/2],
		   [325,(ancho/2)+125-tamJug/2],
		   [225,(ancho/2)-75-tamJug/2],
		   [225,(ancho/2)+75-tamJug/2]]
posInitB = [[525,(ancho/2)-125-tamJug/2],
		   [525,ancho/2-tamJug/2],
		   [525,(ancho/2)+125-tamJug/2],
		   [625,(ancho/2)-75-tamJug/2],
		   [625,(ancho/2)+75-tamJug/2]]
jugadoresA = []
jugadoresB = []
hilosA = []
hilosB = []
porteroA = None
porteroB = None
balon = Balon()
	
def dibujaCancha():
	global cancha
	radio = 60
	largoGde = 300
	anchoGde = 130
	largoCh = 150
	anchoCh = 50
	cancha.create_rectangle(2, 2, 900, 450, outline="white",fill="green",width=3)
	cancha.create_line(450,1,450,450, fill="white",width=3) #linea central
	cancha.create_oval((450-radio), (225-radio), (450+radio), (225+radio), outline="white", width=3)
	#areas del portero
	cancha.create_rectangle(2,225-(largoGde/2),anchoGde,225+(largoGde/2), outline="white",width=3)#area gde izq
	cancha.create_rectangle(900-anchoGde, 225-(largoGde/2), 900, 225+(largoGde/2), outline="white",width=3)#area gde der
	#areas de gol
	cancha.create_rectangle(2,225-(largoCh/2),anchoCh,225+(largoCh/2), outline="white",width=3) #area chica izq
	cancha.create_rectangle(900-anchoCh, 225-(largoCh/2), 900, 225+(largoCh/2), outline="white",width=3) #area chica der

# ANIMACIONES #
def golAnimation(team):
	vel=0.01
	iteam=None
	imgTeam=None
	#Se colocan las imagenes#
	fnd = PhotoImage(file="stadium.png")
	fndzoom=fnd.zoom(3)
	fondo=cancha.create_image(largo/2,ancho,anchor=CENTER,image=fndzoom)

	igol=PhotoImage(file="Goool.png")
	imgGol=cancha.create_image(1350,150,anchor=CENTER,image=igol)
	
	if(team==1):
		iteam = PhotoImage(file="eqA.png")
	else:
		iteam = PhotoImage(file="eqB.png")
	imgTeam=cancha.create_image(-450,300,anchor=CENTER,image=iteam)
		
	cancha.update()
	#animacion#
	while(1):
		cancha.move(imgGol,-20,0)
		cancha.move(imgTeam,+20,0)
		x,y = cancha.coords(imgGol)
		cancha.update()
		sleep(vel)
		if(abs(x-largo/2)<20):break
	marcador(team)
	sleep(1)
	while(1):
		cancha.move(imgGol,-20,0)
		cancha.move(imgTeam,+20,0)
		x,y = cancha.coords(imgGol)
		cancha.update()
		sleep(vel)
		if(abs(x<-500)):
			cancha.move(fondo,+ancho,+largo)
			cancha.update()
			break

	#SE REPOSICIONAN LOS ELEMENTOS#
	balon.direccion=0
	x,y = cancha.coords(balon.img)
	cancha.move(balon.img,largo/2-x,ancho/2-y)

	porteroA.direccion=0
	x1,y1 = cancha.coords(porteroA.img)
	cancha.move(porteroA.img,-x1,200-y1)
	
	porteroB.direccion=0
	x1,y1 = cancha.coords(porteroB.img)
	cancha.move(porteroB.img,850-x1,200-y1)
	i=0
	for j in jugadoresA:
		j.direccion=0
		x1,y1 = cancha.coords(j.img)
		cancha.move(j.img,posInitA[i][0]-x1,posInitA[i][1]-y1)
		i+=1
	i=0
	for j in jugadoresB:
		j.direccion=0
		x1,y1 = cancha.coords(j.img)
		cancha.move(j.img,posInitB[i][0]-x1,posInitB[i][1]-y1)
		i+=1
	cancha.update()
	sleep(1)
	#Se reinicia el juego#
	porteroA.direccion=randint(1, 8)
	porteroB.direccion=randint(1, 8)
	for j in jugadoresA:
		j.direccion=randint(1, 8)
		
	for j in jugadoresB:
		j.direccion=randint(1, 8)
	cancha.update()

def winAnimation(team):
	vel=0.01
	iteam=None
	imgTeam=None

	#se detiene todo
	balon.direccion=0
	porteroA.direccion=0
	porteroB.direccion=0
	
	i=0
	for j in jugadoresA:
		j.direccion=0
		i+=1
	i=0
	for j in jugadoresB:
		j.direccion=0
		i+=1
	cancha.update()
	#Se colocan las imagenes#
	fnd = PhotoImage(file="stadium.png")
	fndzoom=fnd.zoom(3)
	fondo=cancha.create_image(largo/2,ancho,anchor=CENTER,image=fndzoom)

	iwin=PhotoImage(file="winner4.png")
	imgWin=cancha.create_image(largo/2,150,anchor=CENTER,image=iwin)
	
	if(team==1):
		iteam = PhotoImage(file="eqA.png")
	else:
		iteam = PhotoImage(file="eqB.png")
	imgTeam=cancha.create_image(largo/2,300,anchor=CENTER,image=iteam)
		
	cancha.update()
	sleep(3)
	#animacion#
	while(1):
		cancha.move(imgWin,-20,0)
		cancha.move(imgTeam,+20,0)
		x,y = cancha.coords(imgWin)
		cancha.update()
		sleep(vel)
		if(abs(x<-500)):
			cancha.move(fondo,+ancho,+largo)
			cancha.update()
			break

def empateAnimation():
	vel=0.01
	#se detiene todo
	balon.direccion=0
	porteroA.direccion=0
	porteroB.direccion=0
	
	i=0
	for j in jugadoresA:
		j.direccion=0
		i+=1
	i=0
	for j in jugadoresB:
		j.direccion=0
		i+=1
	cancha.update()

	#Se colocan las imagenes#
	fnd = PhotoImage(file="stadium.png")
	fndzoom=fnd.zoom(3)
	fondo=cancha.create_image(largo/2,ancho,anchor=CENTER,image=fndzoom)

	iemp=PhotoImage(file="empate.png")
	imgEmp=cancha.create_image(1350,ancho/2,anchor=CENTER,image=iemp)

	cancha.update()
	#animacion#
	while(1):
		cancha.move(imgEmp,-20,0)
		x,y = cancha.coords(imgEmp)
		cancha.update()
		sleep(vel)
		if(abs(x-largo/2)<20):break
	sleep(1)
	while(1):
		cancha.move(imgEmp,-20,0)
		x,y = cancha.coords(imgEmp)
		cancha.update()
		sleep(vel)
		if(abs(x<-500)):
			cancha.move(fondo,+ancho,+largo)
			cancha.update()
			break

# FUNCIONES DEL CRONOMETRO/RELOJ #
def strtime(num):
	if num<=9:
		return ("0"+str(num))
	return str(num)
def times():
	global dead
	m=0 
	s=0
	while(not dead):
		while(pausa): #mientras hay pausa, se cicla para que no avance el reloj jeje
			pass

		if(s>=60):
			s=0
			m=m+1
		elif(m>=60):
			m=0
		clock.config(text= strtime(m)+":"+strtime(s))
		s+=1
		sleep(1)
		if(m==1 and s==10):
			n = int(meqA.cget("text"))
			m = int(meqB.cget("text"))
			if(m>n):#ganoB
				winAnimation(2)
			elif(m<n):#ganoA
				winAnimation(1)
			else:#empate
				empateAnimation()
			Nuevo()
			break


def marcador(team):
	if(team==1):
		n = int(meqA.cget("text"))
		n+=1
		meqA.config(text= str(n))
	else: 
		n = int(meqB.cget("text"))
		n+=1
		meqB.config(text= str(n))

def resetMarcador():
	meqA.config(text= str(0))
	meqB.config(text= str(0))

# BOTONES #
def Iniciar():
	global dead

	IniciarBtn["state"] = "disable"
	PausarBtn["state"] = "normal"
	NuevoBtn["state"] = "normal"

	dead=False

	#se inician los hilos#
	thReloj = threading.Thread(target=times)
	thReloj.start()
	
	for j in jugadoresA:
		j.direccion=randint(1, 8)
		hilosA.append(threading.Thread(target=j.correr))
		hilosA[len(hilosA)-1].start()

	for j in jugadoresB:
		j.direccion=randint(1, 8)
		hilosB.append(threading.Thread(target=j.correr))
		hilosB[len(hilosB)-1].start()
	porteroA.direccion=randint(1, 8)
	hiloPortA = threading.Thread(target=porteroA.correr)
	hiloPortA.start()
	porteroB.direccion=randint(1, 8)
	hiloPortB = threading.Thread(target=porteroB.correr)	
	hiloPortB.start()

	hiloBalon = threading.Thread(target=balon.direccionar)	
	hiloBalon.start()

def Pausar():
	global pausa
	pausa = True

	PausarBtn["state"] = "disable"
	ReiniciarBtn["state"] = "normal"

	balon.direccion=0
	porteroA.direccion=0
	porteroB.direccion=0
	
	for j in jugadoresA:
		j.direccion=0

	for j in jugadoresB:
		j.direccion=0

def Reiniciar():
	global pausa
	pausa = False
	
	PausarBtn["state"] = "normal"
	ReiniciarBtn["state"] = "disable"

	porteroA.direccion=randint(1, 8)
	porteroB.direccion=randint(1, 8)
	for j in jugadoresA:
		j.direccion=randint(1, 8)

	for j in jugadoresB:
		j.direccion=randint(1, 8)

def Nuevo():
	global dead

	IniciarBtn["state"] = "normal"
	PausarBtn["state"] = "disable"
	ReiniciarBtn["state"] = "disable"
	NuevoBtn["state"] = "disable"

	dead=True
	clock.config(text= "00:00")
	#SE REPOSICIONAN LOS ELEMENTOS#
	balon.direccion=0
	x,y = cancha.coords(balon.img)
	cancha.move(balon.img,largo/2-x,ancho/2-y)

	porteroA.direccion=0
	x1,y1 = cancha.coords(porteroA.img)
	cancha.move(porteroA.img,-x1,200-y1)
	
	porteroB.direccion=0
	x1,y1 = cancha.coords(porteroB.img)
	cancha.move(porteroB.img,850-x1,200-y1)
	i=0
	for j in jugadoresA:
		j.direccion=0
		x,y = cancha.coords(j.img)
		cancha.move(j.img,posInitA[i][0]-x,posInitA[i][1]-y)
		i+=1
	i=0
	for j in jugadoresB:
		j.direccion=0
		x,y = cancha.coords(j.img)
		cancha.move(j.img,posInitB[i][0]-x,posInitB[i][1]-y)
		i+=1

	for h in hilosA:
		hilosA.pop()
	for h in hilosB:
		hilosB.pop()
	resetMarcador()


#---------VENTANA-----------#
raiz = Tk()
raiz.title("Soccer")
raiz.resizable(0,0)
raiz.configure(bg='#2e2e2e')
geostr = str(largo)+"x"+str(ancho)
#raiz.geometry(geostr)

miFrame = Frame(raiz)
miFrame.config(background="#2e2e2e")
miFrame.pack(pady=5)

#---------BOTONES-----------#

IniciarBtn = Button(miFrame,text="Iniciar",width=10,bg='#16A085',command=lambda:Iniciar())
IniciarBtn.grid(row=1,column=1,padx=10)
IniciarBtn["state"] = "normal"

PausarBtn = Button(miFrame,text="Pausar",width=10,bg='#16A085',command=lambda:Pausar())
PausarBtn.grid(row=1,column=2,padx=10)
PausarBtn["state"] = "disable"

ReiniciarBtn = Button(miFrame,text="Reiniciar",width=10,bg='#16A085',command=lambda:Reiniciar())
ReiniciarBtn.grid(row=1,column=3,padx=10)
ReiniciarBtn["state"] = "disable"

NuevoBtn = Button(miFrame,text="Nuevo partido",width=10,bg='#16A085',command=lambda:Nuevo())
NuevoBtn.grid(row=1,column=4,padx=10)
NuevoBtn["state"] = "disable"

#Marcador equipoA
titA=Label(raiz,font=("times",50,"bold"),text="Equipo A")
titA.config(bg='#2e2e2e',fg="blue",font="Calibri 15 bold")
titA.place(x=30, y=10)
meqA=Label(raiz,font=("times",50,"bold"),text="0")
meqA.config(bg="#2e2e2e",fg="yellow",font="Calibri 25 bold")
meqA.place(x=50, y=40,width=50)

#Reloj
clock=Label(raiz,font=("times",50,"bold"),text="00:00")
clock.config(bg="#2e2e2e",fg="white",font="Calibri 25 bold")
clock.pack()

#Marcador equipoB
titB=Label(raiz,font=("times",50,"bold"),text="Equipo B")
titB.config(bg='#2e2e2e',fg="red",font="Calibri 15 bold")
titB.place(x=780, y=10)
meqB=Label(raiz,font=("times",50,"bold"),text="0")
meqB.config(bg="#2e2e2e",fg="yellow",font="Calibri 25 bold")
meqB.place(x=800, y=40, width=50)


#---------CANVAS-----------#
cancha = Canvas(raiz, width=largo, heigh=ancho, bg="black")
#cancha.pack(fill="both",side="right", expand=True)
cancha.pack()
dibujaCancha()



# colocacion inicial del balon #
ballImg = PhotoImage(file="ball.png")
ballImgSub = ballImg.subsample(tamBal)
balon.x = largo/2
balon.y = ancho/2
balon.img = cancha.create_image(balon.x,balon.y,anchor=CENTER,image=ballImgSub)

# Equipo A #
ijuga=PhotoImage(file="delA.png")
idefa=PhotoImage(file="defA.png")
ipora=PhotoImage(file="portA.png")

jugadoresA.append(Jugador(posInitA[0][0], posInitA[0][1],"delantero",ijuga,"blue"))
jugadoresA.append(Jugador(posInitA[1][0], posInitA[1][1],"delantero",ijuga,"blue"))
jugadoresA.append(Jugador(posInitA[2][0], posInitA[2][1],"delantero",ijuga,"blue"))

jugadoresA.append(Jugador(posInitA[3][0], posInitA[3][1],"defensa",idefa,"blue"))
jugadoresA.append(Jugador(posInitA[4][0], posInitA[4][1],"defensa",idefa,"blue"))

porteroA = Jugador(0,200,"portero",ipora,"navy")

# Equipo B #
ijugb=PhotoImage(file="delB.png")
idefb=PhotoImage(file="defB.png")
iporb=PhotoImage(file="portB.png")

jugadoresB.append(Jugador(posInitB[0][0], posInitB[0][1],"delantero",ijugb,"red"))
jugadoresB.append(Jugador(posInitB[1][0], posInitB[1][1],"delantero",ijugb,"red"))
jugadoresB.append(Jugador(posInitB[2][0], posInitB[2][1],"delantero",ijugb,"red"))

jugadoresB.append(Jugador(posInitB[3][0], posInitB[3][1],"defensa",idefb,"red"))
jugadoresB.append(Jugador(posInitB[4][0], posInitB[4][1],"defensa",idefb,"red"))

porteroB = Jugador(850,200,"portero",iporb,"brown")

cancha.update()

raiz.mainloop()