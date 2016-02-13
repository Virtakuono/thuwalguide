#!/usr/bin/python

import math
import numpy

def pakistaniFlagEmblem(color='#B19F6E',offset=0,cutLeft=0,cutRight=0,cutUp=0,cutDown=0):

    # Define A to be something
    A = 3000.0
    B = 2*A/3
    C = A/4
    D = 3*A/4
    E = 13*B/20

    C1_Centerpoint = [C+D/2,B/2]
    LenDiag = math.sqrt(D*D+B*B)
    C2_Centerpoint = [C+D-D/LenDiag*E,B/LenDiag*E]

    C1_Radius = 11*B/40
    C2_Radius = 1*C1_Radius

    Distance_C1_C2 = math.sqrt((C2_Centerpoint[0]-C2_Centerpoint[0])**2 + (C2_Centerpoint[1]-C2_Centerpoint[1])**2)
    C3_Radius = C1_Radius - Distance_C1_C2
    C3_Radius /= 2

    C3_Centerpoint = [C2_Centerpoint[0]+D/LenDiag*C3_Radius,C2_Centerpoint[1]-B/LenDiag*C3_Radius]

    C1_Centerpoint[0] += offset*C1_Radius
    C2_Centerpoint[0] += offset*C1_Radius
    C3_Centerpoint[0] += offset*C1_Radius

    # Compute where circles C1 and C2 intersect

    def intersectionOfCircles(cp1,cp2,r1,r2):

        dirvec = [cp2[0]-cp1[0],cp2[1]-cp1[1]]
        for x in dirvec:
            x /= math.sqrt((cp2[0]-cp1[0])**2+(cp2[1]-cp1[1])**2)

        an1 = 0
        if dirvec[0]:
            an1 = math.atan(dirvec[1]/dirvec[0])
        an2 = an1+math.pi
        
        trialPoint = lambda z: [cp1[0]+r1*math.cos(z),cp1[1]+r2*math.sin(z)]
        distSquare = lambda x,y: (x[0]-y[0])**2+(x[1]-y[1])**2

        if (r1+r2)**2 < distSquare(cp1,cp2):
            return 0

        trialDistSquare = lambda z: distSquare(trialPoint(z),cp2)

        def sign(x):
            if not(abs(x)-x):
                return 1
            return -1

        tr1 = trialDistSquare(an1)
        tr2 = trialDistSquare(an2)

        for iteration in range(30):
            #print('Iteration %d, the angles are %f and %f, (%f,%f)'%(iteration,an1,an2,tr1-r2**2,tr2-r2**2))
            newTrial = 0.5*(an2+an1)
            trialDist = trialDistSquare(newTrial)
            if sign(trialDist-r2**2) == sign(tr2-r2**2):
                an2 = 1*newTrial
                tr2 = 1*trialDist
            else:
                an1 = 1*newTrial
                tr1 = 1*trialDist

        initPoint = 0
        if dirvec[0]:
            initPoint = math.atan(dirvec[1]/dirvec[0])

        return (trialPoint(an1),trialPoint(initPoint-(an1-initPoint)))
    
    
    intersects = intersectionOfCircles(C1_Centerpoint,C2_Centerpoint,C1_Radius,C2_Radius)

    an0 = -1*math.atan(D/B)
    fivePoints = []

    for ii in range(5):
        fivePoints.append([C3_Centerpoint[0]+math.cos(an0+math.pi*2*ii/5)*C3_Radius,C3_Centerpoint[1]+math.sin(an0+math.pi*2*ii/5)*C3_Radius])

    def segmentCross(start1,end1,start2,end2):
        '''
        Check whether two line segments determined
        by their endpoints cross.
        '''

        diff1 = numpy.array([end1[0]-start1[0],end1[1]-start1[1]])
        diff2 = numpy.array([end2[0]-start2[0],end2[1]-start2[1]])

        coefMat = numpy.array([[diff1[0],-1*diff2[0]],[diff1[1],-1*diff2[1]]])

        if abs(numpy.linalg.det(coefMat))< 1.0e-14:
            # two line segments are collinear
            return (False,numpy.array([numpy.nan,numpy.nan]))

        sol = numpy.linalg.solve(coefMat,[start2[0]-start1[0],start2[1]-start1[1]])
        if max(sol)> 1.0 or min(sol)<0.0:
            # lines are not parallel, but they do not intersect
            return (False,numpy.array([start1[0],start1[1]])+sol[0]*diff1)

        return (True,numpy.array([start1[0],start1[1]])+sol[0]*diff1)

    fiveOtherPoints = []

    for ii in range(5):
        fiveOtherPoints.append(segmentCross(fivePoints[(ii+1)%5],fivePoints[(ii+4)%5],fivePoints[ii%5],fivePoints[(ii+2)%5])[1])

    polygonString = '<polygon points="'
    for ii in range(5):
        point = fivePoints[ii]
        otherPoint = fiveOtherPoints[ii]
        polygonString = '%s%d,%d %d,%d '%(polygonString,point[0],point[1],otherPoint[0],otherPoint[1])
    polygonString = '%s" style="fill:%s;stroke:%s;stroke-width:1" />'%(polygonString[:-1],color,color)
    

    svgString = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    svgString = '%s<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 %d %d" version="1.1">\n'%(svgString,A,B)
    svgString = '%s<path d="M%d %dA%d %d 1 0 1 %d %d %d %d 0 1 0 %d %dz" stroke="%s" stroke-width="0" fill="%s"/>\n'%(svgString,intersects[0][0],intersects[0][1],C1_Radius,C1_Radius,intersects[1][0],intersects[1][1],C2_Radius,C2_Radius,intersects[0][0],intersects[0][1],color,color)
    svgString = '%s%s\n'%(svgString,polygonString)
    svgString = '%s</svg>\n'%(svgString)

    return svgString

for foo in range(5):
    print(pakistaniFlagEmblem(offset=2.4*foo-1))
