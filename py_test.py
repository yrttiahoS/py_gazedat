import os

import csv

import sys

#import math

from collections import OrderedDict

import routine # a script with functions

#from my_classes import MyClass

#print(sys.version)


#foo = routine.string_or_number('neutral2.bmp')


stim = ['control.bmp', 'neutral2.bmp', 'control.bmp', 'neutral2.bmp']

##stim = ['control.bmp', 1, 'control.bmp', 'neutral2.bmp',
##        'control.bmp', 'neutral2.bmp', 'control.bmp', 'neutral2.bmp',
##        'control.bmp', 'aaneutral2.bmp']
##
##
##print(sorted(list(stim)))
##print()
print((set(stim)))

print(len(stim))

od  = OrderedDict()
od['masa']= stim

print(len(od['masa']))

print(os.path.join ("aa", "bb"))

limit_files = [0, None]

limit_files.append([])
print(str(limit_files))

##
##ab = ["a", 1, "c", "c", "a"]
##bb= []
##for el in ab:
##    if isinstance(el, str): bb.append(1)
##    else: bb.append(0)
##
##    
##print(all(bb))
##

#print(any (isinstance(ab,str)))

#print(isinstance(foo, str))

#headers = rderedDict("a": None, "b": None, "c": None)
#headers = ["a", "b", "c", "c", "a"]
#headers2 = ["Q", "W"]
##print(sorted(headers))
##print(set(headers))
##
##od = OrderedDict.fromkeys(headers)
##
##fod = "a" in od.keys()
##
##print  (fod)


##print("aa" == "ab")
##
##od = OrderedDict()
##od['a'] = [1,2,3]
##od['b'] = None
##print(od['a'][len(od['a'])-1])
##od['a'].append(2)
##
##
##print(not od['a'])
##
##aa = list([1,1])
##for el in [2,3]: aa.append(el)
###aa.append([2,3])
##
##a = [10,10]
###aa.append(10,10)
##print(aa)
##
##print(max(aa))
##print(len(aa))
##print(isinstance(1,str))



#print(os.getcwd() )
##
##
##aa =  not isinstance(headers[0], str)
##print(aa)

##
##a = {'numbero': [1,2],  "wordolo": "nuppi"}
###a = {'numberot': 1, 2, 3, 4, "wordolot": "nuppi", "nappi", "noppi"}
#intti = float('a')
##print( min(a['numbero']) )
##


##
##print(range(0,10))
##
##a = []
##
##for i in range(9):
##    a.append(i)
##    print(str(a))


#from os.path import join, getsize

##for root, dirs, files in os.walk('C:\\Users\\'):
##    if 'testing 7mo,trec2' in root:      
##        print(root, " ", end=" FOUND! ")
##        print("")


##
##
##def funny(argue):
##    if not argue:
##        print("yell more")
##    else:
##        print("i agrue")
##
##funny("s")
##
##funny(None)
##
##
##default_input_folder = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\testing 7mo,trec2"
##print(os.path.isdir(default_input_folder))

#C:\\Users\\



#x = MyClass("gillo")

#print(x.f())

#print(x.__doc__)
#round(k*3.14)
#
#y = []
#k = 25
#for i, item in enumerate(range(k+1)):
#    print (str(i))
##    yx = (i/k)*math.pi
#    y.append (math.sin((i/k)*2*math.pi)) #*math.pi
#    


#print(x.f())
#print(x.get_i())


##input_file = "headers_tre_5mo_to_7mo.txt"
##input_file = "headers_txt_data.txt"
##
##input_file_delimiter = "\t"
##
##aa = ["q","w","e","r"]
##
##aa = [aa, aa, aa]

#print(list(enumerate(aa)))

##bb = zip( range(20000,20001,1), aa)
#print(list(range(3)))
#print(list(bb))

##for index, element in bb:
##    print(element)

#a = routine.wonder(("amo", "rati", "her"))

##d = dict()
##od = OrderedDict()
##
##od["yks"] = 1
##od["kaks"] = 2
##od["kolme"] = 3
##
##d["yks"] = 1
##d["kaks"] = 2
##d["kolme"] = 3

#print(od)
#   print(d)


##if ("a" is "a"):
##    print("a is a")
##
##b = "abc"


#print("aaaa" + chr(9) + "aaaa") #tab
#print("aaaa" + chr(13) + "aaaa") #CR is a bytecode for carriage return (from the days of typewriters)
#print("aaaa" + chr(10) + "aaaa") #LF similarly, for line feed


# scan through files in a directory

# diritems = os.listdir(os.getcwd())


#table for header pairs

# maptable = {}#dict([('KEY','value')])


#read dictionary key-value pairs from file

#maptable = routine.get_headers(os.getcwd(), input_file)
#print (maptable)
#print (len(maptable.keys()))
#print (maptable.keys())
##print (maptable.values())

#testing a function in imported code

#routine.miracle(5) 


#list_my = [1, 2, 3, 4]

#print(len(list_my))


##def file_handle(file):
##    print (file)
##    print (file.split("."))
##
##for filenum, file in enumerate(diritems):
##    file_handle(file)
##
##
##for i, a in enumerate(["uu","jee"]):
##    print(i)
##    print(a)
##
##
##
##print ("Directory contains "
##+ str(len(diritems)) + " files.")
