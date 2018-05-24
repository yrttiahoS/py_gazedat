from datetime import datetime, date

import os

import time

import csv

import sys

import calendar
#import math

from collections import OrderedDict
from collections import namedtuple


import routine # a script with functions

import numpy as np

import my_classes
#from my_classes import GazeReader
#from my_classes import HeaderReader
##from itertools import islice
import random
random.shuffle(files)
files
print('heillo')

print('acsascscaheillo')


##
##input_folder = "D:\\lasayr\\Aaltonen\\\ct\\6mo"
###"C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\7mo,trec2"
##
##diritems  = [fileName for fileName in os.listdir(input_folder) if fileName.endswith('.gazedata')]
##
###write date
##tt = time.strptime("19 Oct 17", "%d %b %y")
###convert date to epoch time, seconds
##seconds = time.mktime(tt) 
##
##print(diritems[len(diritems)-1])
##print(os.path.getctime(input_folder + '\\' + diritems[1]))
##print(time.time())
##print(tt)
##print(seconds)



#a = os.path.split(input_folder)
#print(os.path.split(input_folder)[1])



##truth = isinstance("1", int)
##routine.string_or_number(123)
##print("truth:" + str(truth))
##
##
##
##input_folder = "D:\\lasayr\\Aaltonen\\24mo"
##print (input_folder + "\\testing")
##
##a=3
##if 1 <= a <= 2:
##    print(str(a))
##else:
##    print("a not in range")


##
##with open(os.path.join('header map 3D.txt'), "rt") as inputfile:
##    reader = csv.reader(inputfile, delimiter = '\t')
##    for r, row in islice(enumerate(reader), 0, 20):
##        print(str(r) + ": " + str(row))
##        inputfile.seek(0)

            
##folder = "C:/Users/infant/Documents/GitHub/py_gazedat"
##file = "header map 3D.txt"
##hr = HeaderReader(folder, file)
##
##print(hr.get_header_colNum('TETTime'))
##print(hr.get_header_newName('r_cam_y'))
##
##hKeys = hr.getKeys()
##
####for header in enumerate(hKeys):
####    #print(header)
####    print(hr.get_header_newName(header[1]))
##
##headersList = ['' for i in range(4)]#['cl1', 'cl2', 'cl3']
###ind = headersList.index('cl4')
##
##newheaders = []
##
##for header in enumerate(hKeys):#enumerate(header_keys):
##                if not hr.get_header_newName(header[1]) == my_classes.OBSOLETE_HEADER:
##                    newheaders.append(hr.get_header_newName(header[1]))
##
##
##
##print('Rubject' in newheaders)
##print(type(hr))
##val =  isinstance(hr, HeaderReader)
##print(val)
##
##n = hr.get_n_of_uniqueCols()
##print(n)
##
##l= ["x" for i in range(9)]
##target = 3
##print(l)
##l.pop(target)
##l.insert(target, "X")
##print(l)


od = OrderedDict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
od = OrderedDict.fromkeys(headers) 
header = '6'
#od = OrderedDict.fromkeys(headers) 

l = tuple('name')
od['Thing'] = l

print('l:' + str(l))
print('od:' + str(od))
print('od(Thing):' + str(od['Thing']))
print('num in od(Thing):' + str(od['Thing'][1]))

#od['Thing'].append(13)
#od['guido'].append(31)
#od['sape'].append(13)
#od['guido'].append(31)



#di = dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
#
#folder = os.getcwd() + '\\'
#with open((folder + 'foo.gazedata'),'w') as data:    data.write(str(od))
#with open((folder + 'food.gazedata'),'w') as data:    data.write(str(di))

##
##Strong = namedtuple('Strong', 'name num')
##
##strong1 = Strong('name', 123)
##od['StrongThing'] = strong1
##od['TitanicThing'] = Strong('FamousName', 88)
##
##print(strong1.name)
##print(od['StrongThing'].num)
##print(od['TitanicThing'].num)
##
