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
from time import sleep

####SETUP####
SIM900_add = 'ASRL1'
SIM921_slot= '5'
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

temp_arr=np.asarray(temp_list, dtype='float')
rest_arr=np.asarray(rest_list, dtype='float')
#SIM900 needs rounding of lakeshore values to take them
temp_arr = np.round(temp_arr, 5)
rest_arr = np.round(rest_arr, 5)
#Optional plotting to see curve
plt.loglog(temp_arr,rest_arr )
plt.show()

#Initialise cal
SIM900_mf=SIM900(SIM900_add)
SIM900_mf.write(SIM921_slot, 'CINI '+curve_to_update+', '+curve_to_update+', '+curve_string)
sleep(1)
#Add cal points
#Note points must be added in increasing resistance value according to SIM921 docs
for i in range(len(temp_list)-1, -1, -1):
    string_to_write='CAPT '+curve_to_update+', '+str(rest_arr[i])+', '+str(temp_arr[i])
    SIM900_mf.write(SIM921_slot, string_to_write)
    sleep(1)

#Check the curve
print('Calibration finished')
print(SIM900_mf.ask(SIM921_slot, 'CINI? 1'))
#Set the curve to be used
SIM900_mf.write(SIM921_slot, 'CURV '+curve_to_update)
#Set the temp to be displayed
SIM900_mf.write(SIM921_slot, 'DTEM ON')

#Option to read it back and plot it to check
rb_temp=[]
rb_rest=[]
for i in range(1, len(temp_list)+1, 1):
	resp=SIM900_mf.ask(SIM921_slot, 'CAPT? '+curve_to_update+', '+str(i))
	resp=resp.split(',')
	rb_rest.append(resp[0])
	rb_temp.append(resp[1])
	sleep(1)
rb_rest_arr=np.asarray(rb_rest, dtype='float')
rb_temp_arr=np.asarray(rb_temp, dtype='float')
plt.loglog(rb_temp_arr, rb_rest_arr)
plt.show()
