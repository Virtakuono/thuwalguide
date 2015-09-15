#!/usr/bin/python

import math

# Define A to be something
A = 1000.0
B = 2*A/3
C = A/4
D = 3*A/4
E = 13*B/20

C1_Centerpoint = [C+D/2,B/2]
LenDiag = math.sqrt(D*D+B*B)
C2_Centerpoint = [A-D/LenDiag*E,B/LenDiag*E]

C1_Radius = 11*B/40
C2_Radius = 1*C1_Radius

Distance_C1_C2 = math.sqrt((C1_Centerpoint[0]-C2_Centerpoint[0])**2 + (C1_Centerpoint[1]-C2_Centerpoint[1])**2)
C3_Radius = C1_Radius - Distance_C1_C2
C3_Radius /= 2

C3_Centerpoint = [C1_Centerpoint[0]+D/LenDiag/2*C3_Radius,C1_Centerpoint[1]-B/LenDiag/2*C3_Radius]

