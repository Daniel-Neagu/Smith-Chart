import numpy as np

#checks if the impedence entered is an actual number
def checkForValidImpedence(loadre,loadim):
    try:
        real = float(loadre.text())
        imag = float(loadim.text())
    except ValueError:
        return False
    return True

#converts impedence given by text from the buttons/input to float for calculations
def convertImpTextToFloat(loadre,loadim):
    real = float(loadre.text())
    imag = float(loadim.text())
    return [real,imag]

#get the RefCoeffMag at the load
def getRefCoeffMag(loadre,loadim,charimp):
    return np.abs(np.sqrt(((loadre-charimp)**2+loadim**2)/((loadre+charimp)**2+loadim**2)))

#get norm impedence #assumes that the input/normvalue is both a float, and also valid
def getNormValue(input,normValue):
    return input/normValue
#normalize impedence
def getloadnorm(load,char):
    try:
        loadimp = float(load.text())

        try:
            charimp = float(char.text())            
        except ValueError:
            charimp = 50
        return loadimp/charimp
    except ValueError:
        return ""

def getRefCoeffMagAtLoad(loadre,loadim,char):
    try:
        loadim = float(loadim.text())
        loadre = float(loadre.text())

        try:
            charimp = float(char.text())            
        except ValueError:
            charimp = 50
        return np.abs(np.sqrt(((loadre-charimp)**2+loadim**2)/((loadre+charimp)**2+loadim**2)))
    except ValueError:
        return ""
    

def getSWR(RefCoeffMag):
    return (1 + RefCoeffMag)/(1-RefCoeffMag)

#DOES NOT WORK LOL I AM STUPID OR SMTH????
def getSWRIntersectionWithRealEq1(RefCoeffMag):
    x = (0.5-2*(1-RefCoeffMag)**2)/2
    y = np.sqrt(RefCoeffMag**2-x**2)
    return [[x,x],[y,-y]]


def getIntersections2Circles(centerx1,centery1,radius1,centerx2,centery2,radius2):
    d = np.sqrt((centerx1-centerx2)**2+(centery1-centery2)**2)
    l = (radius1**2-radius2**2 + d**2)/(2*d)
    h = np.sqrt(radius1**2-l**2)

    #intersections between two circles
    x1 = l/d*(centerx2-centerx1) + h/d*(centery2-centery1)+centerx1
    x2 = l/d*(centerx2-centerx1) - h/d*(centery2-centery1)+centerx1
    y1 = l/d*(centery2-centery1) - h/d*(centerx2-centerx1)+centery1
    y2 = l/d*(centery2-centery1) + h/d*(centerx2-centerx1)+centery1

    return [[x1,x2],[y1,y2]]

#takes a point on the unit circle and converts it to an impedence, real + imaginary
def convertPointToImpedence(x,y):
    #determing the real impedence
    #the intersection between the real and imag imp. circles is at 
    # (x,y) the given point, and (1,0) since all the circles on the smith chart begin there
    #given this we can find the center of the real imp. circle since we know that it's (xc,yc) yc value equals 0
    # we also can express the radius or center of the real circle in terms of the normalized real impedence
    # generally, if (1,0) as an arbitrary (x2,y2) we would have xc = ((y2-y1)/(x1-x2)*(y2+y1-2yc)-(x1+x2))*(-1/2)
    # and the we know that the real circle has center at (r/(r+1),0) therefore xc = r/(r+1) and r = xc/(1-xc)

    xc = ((x+1)-(y)/(1-x)*(y))*(0.5)
    r = xc/(1-xc)

    #similarly i think for the imaginary impedence, since we know the centre of the imag circle is at (1,yc)

    yc = ((1-x)/(y)*(x-1)-(y))*(-0.5)
    x = 1/yc

    return [r,x]

def convertImpedenceToPoint(re,im):
    #ASSUME THAT THE IMPEDENCE INPUT IS ALREADY NORMALIZED THOUGH !!!!!!
    points = getIntersections2Circles(re/(re+1),0,1/(re+1),1,1/im,abs(1/im))
    if round(points[0][0],5) ==1:
        return [points[0][1],points[1][1]]
    else:
        return [points[0][0],points[1][0]]


def getDistBetweenImpValues(r1,x1,r2,x2,R):
    #finds the distance required to add to the TL to convert the load's resistance to 1+jb
    #find where on circle the point would have landed because we know it's angle with respect to the origin 
    #from then we can simply calculate the wavelengths as a portion or fraction of the 0.25 wavelength across a semicircle proportional to the angle/pi
    #we can call the getintersection of 2 circles function to find the intersections of the real and imaginary circle to calculate the (x,y) of the input
    #we are going to assume that we start at (r1,x1) AND ARE GOING CLOCKWISE UNTIL (r2,x2)

    start = convertImpedenceToPoint(r1,x1)
    x1 = start[0]
    y1 = start[1]
  
    end = convertImpedenceToPoint(r2,x2)
    x2 = end[0]
    y2 = end[1]

    """print("points")
    print(start[0],start[1])
    print(end[0],end[1])"""

    #WE CAN OBTAIN THE ANGLES OF EACH POINT W RESPECT TO THE X-AXIS AS ROTATED on the origin
    if (np.arcsin(y1/R)<0):
        theta1 = 2*np.pi-np.arccos(x1/R)
    else:
        theta1 = np.arccos(x1/R)

    if (np.arcsin(y2/R)<0):
        theta2 = 2*np.pi-np.arccos(x2/R)
    else:
        theta2 = np.arccos(x2/R)
    

    alpha = (theta1-theta2+2*np.pi)%(2*np.pi)

    """alpha = np.abs(theta1-theta2)
    if(theta1<theta2):
        alpha = 2*np.pi-alpha"""
    
    d = alpha/np.pi * 0.25
    #we know that the wavelength along one half of the circumference is 0.25 lambda
    #therefore 0.25 lambda / pi
    #so the distance in terms of wavelengths between the impedences is found from d/0.25 = alpha/pi => d = alpha/pi * 0.25 lambda
    return d

def getShortCircuitShuntLength(B,Zo,Zin):
    #needs to rely on a valid value for B
    #B = 2pi/wavelength
    #this model is specifically doing shunt matching therefore a short circuit impedence is added
    #that means that Zin = jZotan(Bd)
    #therefore we can take the value of b we have and do tan-1(b/Zo) / B = l
    return np.arctan(Zin)/B+np.pi

