import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import re
import math
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys
import warnings
import pyqtgraph as pg
import csv
	
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
app = QtGui.QApplication([])

a = pg.PlotWidget()
a.setWindowTitle('XY plane')
styles = {"color": "#f00", "font-size": "20px"}

a.showGrid(x=True, y=True)
a.setXRange(0, 1000)
a.setYRange(0, 1000)
scatter1 = pg.ScatterPlotItem( symbol='o', size=10,pxMode=False)
a.setLabel("bottom", "X ","mm",**styles) 
a.setLabel("left", "Y ","mm",**styles) 
a.resize(600, 600)
a.setAspectLocked(True)

b = pg.PlotWidget()
b.setWindowTitle('YZ plane')
styles = {"color": "#f00", "font-size": "20px"}

b.showGrid(x=True, y=True)
b.setXRange(0, 1000)
b.setYRange(0, 1000)
scatter2 = pg.ScatterPlotItem( symbol='o', size=10,pxMode=False)
b.setLabel("bottom", "Y ","mm",**styles) 
b.setLabel("left", "Z ","mm",**styles) 
b.resize(600, 600)
b.setAspectLocked(True)

c = pg.PlotWidget()
c.setWindowTitle('XZ plane')
styles = {"color": "#f00", "font-size": "20px"}

c.showGrid(x=True, y=True)
c.setXRange(0, 1000)
c.setYRange(0, 1000)
scatter3 = pg.ScatterPlotItem( symbol='o', size=10,pxMode=False)
c.setLabel("bottom", "X ","mm",**styles) 
c.setLabel("left", "Z ","mm",**styles) 
c.resize(600, 600)
c.setAspectLocked(True)

a.show()
b.show()
c.show()

a.addItem(scatter1)
b.addItem(scatter2)
c.addItem(scatter3)

pos31= np.array([[]])
pos32= np.array([[]])
pos33= np.array([[]])

curve_z=np.array([[]])
curve_Z=np.array([[]])
z11=1
z22=2
z21=1
x11=1
y11=1
xaa=2
yaa=1
x=1
y=1
count=1
Zee=30
#Zoo=np.array([-628586.22102768,266193.71262433,-39435.25846325,2421.93985714])

Zoo=np.array([-628586.22102768,266193.71262433,-39435.25846325,2421.93985714])
z3=0
Va1=0
Ha1=0

def update_line(x1,y1,z2,x2,y2,z3):	
	global pos31,pos32,pos33,temp

	pos31=np.append(pos31,[[round(x2,3)*10,round(y2,3)*10]])
	pos32=np.append(pos32,[[round(y2,3)*10,round(z3,3)*10]])
	pos33=np.append(pos33,[[round(x2,3)*10,round(z3,3)*10]])
	pos41 = pos31.reshape((pos31.shape[0])/2,2)
	pos42 = pos32.reshape((pos32.shape[0])/2,2)
	pos43 = pos33.reshape((pos33.shape[0])/2,2)
	if pos41.shape[0]==150:
		pos31=np.delete(pos31,[0,1],axis=0)
		pos32=np.delete(pos32,[0,1],axis=0)
		pos33=np.delete(pos33,[0,1],axis=0)
#	print(pos41)
	scatter1.setData(pos=pos41)
	scatter2.setData(pos=pos42)
	scatter3.setData(pos=pos43)




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
		global z11,z22,z21,x11,y11,xaa,yaa,x,y,count,curve_Z,curve_z,Zee,Zoo,z3,Va1,Ha1
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
#		print(landmark(value,0))
		if bool(re.match("[0-9.]", x1))==1 and bool(re.match("[0-9.]", y1))==1 and bool(re.match("[0-9.]", z1) )==1 and bool(re.match("[0-9.]", x2))==1 and bool(re.match("[0-9.]", y2))==1 and bool(re.match("[0-9.]", z2) )==1:
			if float(z1)<=2.5 and float(z2)<=2.5:			
#				print(x2+y2+z2)
				z2=math.sqrt( ((float(x2)-float(x1))**2)+((float(y2)-float(y1))**2) )
				z3=(Zoo[0]*z2**3+Zoo[1]*z2**2+Zoo[2]*z2+Zoo[3])/10 #conversion to cm				
				if z3>10:
					x11= 2*math.tan(math.radians(Va1))*z3*.5625
					y11= 2*math.tan(math.radians(Ha1))*z3*.75
					x=((.5*(z3-30))/z3)
					y=((.5625*(z3-30))/(z3*2))+.21875
					xaa=2*math.tan(math.radians(Va1))*30*.5625
					yaa=2*math.tan(math.radians(Ha1))*30*.75
				X44=(xaa/(1-2*y))*(float(x1)-y)
				y4=(yaa/(1-2*x))*(float(y1)-x)
#				print(2*math.tan(math.radians(Va1))*50*.5625,2*math.tan(math.radians(Ha1))*50*.75)
#				print(z21,z22,x1,y1,z1,x4,y4,z3,X44,xaa,yaa)
#				print(count,curve_z,curve_Z,Zoo,z3)
				update_line(x2,y2,z2,X44,y4,z3)	
				print(X44,y4,z3)
				if value.find("Tap")>-1:
					count=count+1
					if count%2!=0:
						with open('Plots.csv', 'a') as newFile:	
						    newFileWriter = csv.writer(newFile)
					 	    newFileWriter.writerow(["next circle"])						
				if count%2==0:
					with open('Plots.csv', 'a') as newFile:	
					    newFileWriter = csv.writer(newFile)
				 	    newFileWriter.writerow([X44*10,y4*10,z3*10])
					print("recording")
				if count%2!=0:
					print("not recording")
				if value.find("Double")>-1:
					with open('Plots.csv', 'a') as newFile:	
					    newFileWriter = csv.writer(newFile)
				 	    newFileWriter.writerow(["waste circle"])
					print("waste circle")					
	app.processEvents()

    connection.close()

from ppadb.client import Client as AdbClient



client = AdbClient(host="127.0.0.1", port=5037)
device = client.device("DHE4C18C10003361")
device.shell("logcat", handler=dump_logcat)



