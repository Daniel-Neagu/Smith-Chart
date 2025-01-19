import pyqtgraph as pg
import numpy as np
from PyQt5.QtCore import Qt

"""
def plotCircleReal(centerx, centery,radius,numpoints,color,thick,plot_graph):
        
    #if given a circle of the type (gr-x/(1+x))^2 + (gi^2) = (1/(1+x))^2
    #need to plot the entirety of the circle and can just do... since we can make sure it's contained        
    #by the unit circle from what we input without having to mask
    angles = np.linspace(0,2*np.pi, numpoints)
    impedence = 1/radius -1
    x = radius * np.cos(angles) + centerx
    y = radius * np.sin(angles) + centery
    imp_label = pg.TextItem(str(int(impedence*10+0.5)/10.0).removesuffix(".0"),color='white')#
    imp_label.setPos(centerx-radius, 0)
    plot_graph.addItem(imp_label)
    plot_graph.plot(x,y, pen=pg.mkPen(color, width=thick, style=Qt.DotLine))#,style=Qt.SolidLine
"""
def plotCircleReal(impedence,color,width,style,plot_graph,numpoints=1000):
    #find circle variables
    radius = 1/(1+impedence)
    centerx = impedence/(1+impedence)
    centery = 0 
    angles = np.linspace(0,2*np.pi, numpoints)
    x = radius * np.cos(angles) + centerx
    y = radius * np.sin(angles) + centery
    imp_label = pg.TextItem(str(int(impedence*10+0.5)/10.0).removesuffix(".0"),color='white')#
    imp_label.setPos(centerx-radius, 0)
    plot_graph.addItem(imp_label)
    plot_graph.plot(x,y, pen=pg.mkPen(color=color, width=width, style=style))#,style=Qt.SolidLine

def plotCircleImagLol(impedence,color,width,style,plot_graph,numpoints=1000):
    #finds circle variables
    centerx = 1
    centery = 1/impedence
    radius = np.abs(centery)
    
    #calculations based on https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect 
    #finds intersection of two circles
    d = np.sqrt(centerx**2+centery**2)
    l = (1-radius**2 + d**2)/(2*d)
    h = np.sqrt(1-l**2)

    #intersections between two circles
    x1 = l/d*(centerx) + h/d*(centery)
    x2 = l/d*(centerx) - h/d*(centery)
    y1 = l/d*(centery) - h/d*(centerx)
    y2 = l/d*(centery) + h/d*(centerx)

    #displacements between center of imag. circle and the intersected points
    dx1 = x1-centerx
    dy1 = y1-centery
    dx2 = x2-centerx
    dy2 = y2-centery

    #finds the arctan angle of the intersected points with respect to the imag. circle, NOT UNIT CIRCLE
    #in order to then calculate the respective point by doing cos,sin(arctan(dy,dx)) * radius + centerx,y
    if(centery>0):  #for positive impedence circles
        if(np.arctan2(dy2,dx2)<0):
            imtheta = 2*np.pi + np.arctan2(dy2,dx2) #arctan2 returns only from [pi,-pi] so need to adjust for correct quadrant
        else:
            imtheta = np.arctan2(dy2,dx2)
        angles1 = np.linspace(imtheta,3/2*np.pi,numpoints)
        imp_label = pg.TextItem(str(int(impedence*10)/10.0).removesuffix(".0"),color='white')
        imp_label.setPos(x2, y2)
    else: #negative impedence circles
        if(np.arctan2(dy1,dx1)>0):
            imtheta = np.arctan2(dy1,dx1)
        else:
            imtheta = 2*np.pi + np.arctan2(dy1,dx1)
        angles1 = np.linspace(np.pi/2,imtheta,numpoints)
        imp_label = pg.TextItem(str(int(impedence*10)/10.0).removesuffix(".0"),color='white')
        imp_label.setPos(x1, y1)

    #calculates the x and y positions for the impedence circle curve
    finalx1 = radius * np.cos(angles1) + centerx
    finaly1 = radius * np.sin(angles1) + centery
    
    #plots
    plot_graph.addItem(imp_label)
    plot_graph.plot(finalx1,finaly1,pen=pg.mkPen(color=color, width=width, style=style))

def plotCircle(centerx, centery, radius, numpoints, color, thick,plot_graph):
    angles = np.linspace(0,2*np.pi, numpoints)
    x = radius * np.cos(angles) + centerx
    y = radius * np.sin(angles) + centery
    #mask = np.where(x**2 + y**2 <= 1)
    #distances = np.hypot(x, y)  # Calculates sqrt(x**2 + y**2)
    #mask = distances <= np.sqrt(1)
    #maskx = x[mask]
    #masky = y[mask]
    plot_graph.plot(x,y, pen=pg.mkPen(color, width=thick,style=Qt.SolidLine))#,style=Qt.SolidLine

def plotWaveLengthCircle(radius, numpoints, color, thick,plot_graph):
    angles = np.linspace(0,2*np.pi, numpoints)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles) 
    plot_graph.plot(x,y, pen=pg.mkPen(color, width=thick,style=Qt.SolidLine))#,style=Qt.SolidLine
    labels = np.linspace(0,np.pi*24/25,25)
    for i,d in enumerate(labels):
        wave_label = pg.TextItem(str(np.around((25-i)*0.01,2)).removesuffix(".0"),color='white',angle=d*180/np.pi)
        wave_label.setPos(radius*np.cos(d),radius*np.sin(d))
        plot_graph.addItem(wave_label)
        #super cool
        #dashed_line = pg.InfiniteLine(pos=(radius*np.cos(d),radius*np.sin(d)), angle=d*180/np.pi, pen=pg.mkPen('r', style=pg.QtCore.Qt.DashLine))
        #plot_graph.addItem(dashed_line)
    labels = np.linspace(np.pi,np.pi*49/25,25)
    for i,d in enumerate(labels):
        wave_label = pg.TextItem(str(np.around((50-i)*0.01,2)).removesuffix(".0"),color='white',angle=d*180/np.pi)
        wave_label.setPos(radius*np.cos(d),radius*np.sin(d))
        plot_graph.addItem(wave_label)
    


def plotLine(startx, starty, endx,endy,numpoints,color,plot_graph):
    x = np.linspace(startx,endx,numpoints)
    y = np.linspace(starty,endy,numpoints)
    plot_graph.plot(x,y,pen=pg.mkPen(color,width=2))

def blank_plot(plot_graph):
        
     # Clear all items from the plot
    plot_graph.clear()
    plot_graph.showAxis('left', False)
    plot_graph.showAxis('bottom', False)
    plot_graph.setXRange(-1, 1)
    plot_graph.setYRange(-1, 1)

    #sets the x and y axis
    plotLine(-1,0,1,0,100,'lightblue',plot_graph)
    plotLine(0,-1,0,1,100,'lightblue',plot_graph)

    #sets outside circle
    plotCircleReal(0,'lightblue',8,Qt.DotLine,plot_graph)
    
    #plots the imag circles
    #need to convert a list of imag values to the circles with impedence = imag value       
    imag = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.2,1.4,1.6,1.8,2,3,4,5,10,20,50]
    for i in imag:
        plotCircleImagLol(i,'lightgreen',4,Qt.DotLine,plot_graph)
        plotCircleImagLol(-i,'lightgreen',4,Qt.DotLine,plot_graph)
        #plotCircleImagLol(1,-1/(i),1/(i),1000,'lightblue',4,plot_graph)

    #plots the real circles
    #need to convert a list of real values to the circles with impedence = real value
        
    real = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.2,1.4,1.6,1.8,2,3,4,5,10,20,50]
    for i in real:
        #plotCircleReal(i/(1+i),0,1/(1+i),1000,'lightblue',4,plot_graph)
        plotCircleReal(i,'lightblue',4,Qt.DotLine,plot_graph)

    #wavelength area
    plotWaveLengthCircle(1.15,1000,'lightblue',6,plot_graph)

    
def plotPoints(x,y,plot,color):
    plot.plot(
        x,  # X-coordinate
        y,  # Y-coordinate
        pen=None,  # No connecting line
        symbol='o',  # Circular point
        symbolSize=20,  # Size of the symbol (diameter)
        symbolBrush=color # Blue fill color
    )

def plotWavelengthLine(R,x1,y1,plot,color):
    #the line must pass through (0,0) (x1,y1), and end when r=1.15 the radius of the wavelength circle so...
    #y = x * y1/x1
    #x^2+y^2 = R^2
    #=>X = sqrt(R^2-y^2)
    #=> y = sqrt(R^2-y^2)*y1/x1
    #=>y^2 = (R^2-y^2)*y1^2/x1^2
    #=>y = R*y1/|x1| / sqrt(1+y1^2/x1^2)
    #=> x = y*x1/y1
    y = R*y1/np.abs(x1) / np.sqrt(1+y1**2/x1**2)
    x = y*x1/y1
    plotLine(0,0,x,y,100,color,plot)
