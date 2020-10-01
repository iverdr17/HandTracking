import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import re
import math
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys
import requests
import time

	
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 4
w.setWindowTitle('Pixel Coordinates XY plane (0-1 units)')
a=gl.GLAxisItem()
a.setSize(1,1,1)
e=gl.GLAxisItem()
e.setSize(60,60,60)
w.addItem(e)
w.setBackgroundColor('w')

b = gl.GLViewWidget()
b.opts['distance'] = 180
b.setWindowTitle('World Coordinates XY plane(30-60 units)')
b.addItem(e)
b.setBackgroundColor('w')

c = gl.GLViewWidget()
c.opts['distance'] = 180
c.setWindowTitle('World Coordinates YZ(Scale 30-60 cm)')
c.addItem(e)
c.setBackgroundColor('w')

d = gl.GLViewWidget()
d.opts['distance'] = 180
d.setWindowTitle('World Coordinates  XZ(Scale 30-60 cm)')
d.addItem(e)
d.setBackgroundColor('w')

sp1 = gl.GLScatterPlotItem( color=(0,0,0,1), size=.02, pxMode=False)
sp2 = gl.GLScatterPlotItem( color=(0,0,0,1), size=.6, pxMode=False)
sp3 = gl.GLScatterPlotItem( color=(0,0,0,1), size=.6, pxMode=False)
sp4 = gl.GLScatterPlotItem( color=(0,0,0,1), size=.6, pxMode=False)
sp1.setGLOptions('translucent')
sp2.setGLOptions('translucent')
sp3.setGLOptions('translucent')
sp4.setGLOptions('translucent')

w.addItem(sp1)
b.addItem(sp2)
c.addItem(sp3)
d.addItem(sp4)

#w.show()
#b.show()
#c.show()
#d.show()
#e.show()
#f.show()
#g.show()
#h.show()

pos31= np.array([[]])
pos32= np.array([[]])

z11=1
z22=2
z21=1
x11=1
y11=1
xaa=2
yaa=1
x=1
y=1
Va1=30
count=0
Ha1=90
def update_line(x1,y1,z2,x2,y2,z3):	
	global pos31,pos32
	pos31=np.append(pos31,[[round(float(x1),2),round(float(y1),2),round(float(z2),2)]],axis=1)
	pos32=np.append(pos32,[[round(float(x2),2),round(float(y2),2),round(float(z3),2)]],axis=1)

#	print(pos3)
	if pos31.shape[1]==423:
		pos31=np.delete(pos31,[0,1,2],axis=1)
	if pos32.shape[1]==423:
		pos32=np.delete(pos32,[0,1,2],axis=1)

	pos41 = pos31.reshape((pos31.shape[1])/3,3)
	pos42 = pos32.reshape((pos32.shape[1])/3,3)
	sp1.setData(pos=pos41)
	sp2.setData(pos=pos42)
	sp3.setData(pos=pos42)
	sp4.setData(pos=pos42)
	print(pos41.shape)



def landmark(value,index):
	ch = chr(97+index)

	Land1="Landmark["+str(index)+"]"
	Land2=")"+ch
	value1=(value[value.find(Land1):value.find(Land2)+1])
	x=value1[value1.find('(')+1:value1.find(',')]
	y=value1[value1.find(',')+1:value1.find('!')]
	z=value1[value1.find('!')+1:value1.find(')')]
#	print(value1)
	return x,y,z

def angle(value2):
	Ha=value2[value2.find("(")+1:value2.find(",")]
	Va=value2[value2.find(",")+1:value2.find(")")]
#	return float(Ha),float(Va)
	return Ha,Va
def dump_logcat(connection):
    while True:
        data = connection.read(1600)
        if not data:
            break
	if data.find("Landmark[0]")>-1:
		global z11,z22,z21,x11,y11,xaa,yaa,x,y,Va1,count,Ha1
		value=(data[data.find("Landmark[0]"):data.find("Press")+2])
		value2=data[data.find("focallengthinmm"):data.find(")in")+1]
		Ha,Va=angle(value2)
		
		if bool(re.match("[0-9.]", Ha))==1 and bool(re.match("[0-9.]", Va))==1:
			Ha1=float(Ha)
			Va1=float(Va)

		xa=2*math.tan(math.radians(Va1))*float(z11)
		ya=2*math.tan(math.radians(Ha1))*float(z11)
#		print(xa,ya)
		x1,y1,z1=landmark(value,5)
		x2,y2,z2=landmark(value,17)
		x3,y3,z3=landmark(value,0)
#		print(landmark(value,0))
		if bool(re.match("[0-9.]", x1))==1 and bool(re.match("[0-9.]", y1))==1 and bool(re.match("[0-9.]", z1) )==1 and bool(re.match("[0-9.]", x2))==1 and bool(re.match("[0-9.]", y2))==1 and bool(re.match("[0-9.]", z2) )==1 and bool(re.match("[0-9.]", x3))==1 and bool(re.match("[0-9.]", x3))==1 and bool(re.match("[0-9.]", x3) )==1:
			if float(z1)<=2.5 and float(z2)<=2.5:			
#				print(x2+y2+z2)
				z2=math.sqrt( ((float(x2)-float(x1))**2)+((float(y2)-float(y1))**2) )

#0.1770482823415692	0.08928792109329571			
#				z1=float(z1)*z11
				z3= (30/(z22-z21))*(float(z2)-z21)+30
#				print(z2)
				if value.find("Tap")>-1:
#					z11=30/z1
					z21=0.1770482823415692
					count=count+1
				if value.find("Double")>-1:
#					z11=30/z1
					z22=0.08928792109329571
					xaa=2*math.tan(math.radians(Va1))*30*.5625
					yaa= 2*math.tan(math.radians(Ha1))*30*.75
					count=count+1
				if z3>10:
					x11= 2*math.tan(math.radians(Va1))*z3*.5625
					y11= 2*math.tan(math.radians(Ha1))*z3*.75
					x=((.5*(z3-30))/z3)
					y=((.5625*(z3-30))/(z3*2))+.21875
				X4= y*x11-(x11/(.5625))*(float(x2)-.21875)
				X41= (y-1)*x11-(x11/(.5625))*(float(x2)-.21875)
				x4= (xaa/(X41-X4))*(float(x2)-X4)
				X44=(xaa/(1-2*y))*(float(x1)-y)
#				x4= (xaa/(.5625))*(float(x1)-.21875)+x*x11
				y4=(yaa/(1-2*x))*(float(y1)-x)
				x5= (x11/(.5625))*(float(x2)-.21875)
				x6= (x11/(.5625))*(float(x3)-.21875)
				l1=math.sqrt( ((x5-x4)**2)+((float(y2)*y11-float(y1)*y11)**2) )
				l2=math.sqrt( (((float(x2)-float(x1))*x11/.5625)**2)+(((float(y2)-float(y1))*y11/.75)**2) )
		#		print(z21,z22,x1,y1,z1,x4,y4,z3,X44,xaa,yaa)
				print(z21,z22,X44,y4,z3)
				update_line(x2,y2,z2,X44,y4,z3)	

				if count==2:
					data={'x':round(X44,2),'y':round(y4,2),'z':round(z3,2)}
					r=requests.post('http://web.iitd.ac.in/~mez158451/WebHTMServer/index.php',json=data)					
				#	time.sleep(.1)
					print(r.text)
	app.processEvents()

    connection.close()

from ppadb.client import Client as AdbClient



client = AdbClient(host="127.0.0.1", port=5037)
device = client.device("DHE4C18C10003361")
device.shell("logcat", handler=dump_logcat)



