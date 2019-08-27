#########################################################
#
# Script to load calibration files from CERNOX temp sensors (LAKESHORE) to
# SIM921 AC resistance bridges
#
# G Taylor - August 2019
#
#########################################################
from visa import *
from hardware import SIM900
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt

####SETUP####
SIM900_add = ''
SIM921_slot= '4'
curve_to_update = '1' #1 to 3
curve_type='LINEAR'
curve_string='1KCAL'
#Get data curve
temp_list=[]
rest_list=[]
CalFile = askopenfilename(initialdir="Z:\\", title="Choose calibration file")
with open(CalFile) as calfile:
    for index, row in enumerate(calfile):
        if index<3:
            pass
        else:
            temp_list.append((row.split()[0]))
            rest_list.append((row.split()[1]))

#Optional plotting to see curve
'''
temp_arr=np.asarray(temp_list, dtype='float')
rest_arr=np.asarray(rest_list, dtype='float')
plt.loglog(temp_arr,rest_arr )
plt.show()
'''

#Initialise cal
SIM900_mf=SIM900(SIM900_add)
SIM900_mf.write(SIM921_slot, 'CINI '+curve_to_update+', '+curve_to_update+', '+curve_string)

#Add cal points
#Note points must be added in incresing resistance value according to SIM921 docs
for i in range(len(temp_list)-1, -1, -1):
    string_to_write='CAPT '+curve_to_update+', '+rest_list[i]+', '+temp_list[i]
    SIM900_mf.write(SIM921_slot, string_to_write)

#Check the curve
print(SIM900_mf.ask(SIM921_slot, 'CINI? 1'))

#Option to read it back and plot it to check
rb_temp=[]
rb_rest=[]
for i in range(len(temp_list)):
	resp=SIM900_mf.write(SIM921_slot, 'CAPT?, '+curve_to_update+', '+str(i))
	rb_rest.append(resp[0])
	rb.temp.append(resp[1])
rb_rest_arr=np.asarray(rb_rest, dtype='float')
rb_temp_arr=np.asarray(rb_temp, dtype='float')
plt.loglog(rb_temp_arr, rb_rest_arr)
plt.show()
