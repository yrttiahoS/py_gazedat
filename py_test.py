import os

import csv

import sys

from collections import OrderedDict

import routine # a script with functions

from my_classes import MyClass

#print(sys.version)


x = MyClass()


print(x.f())
print(x.get_i())


input_file = "headers_tre_5mo_to_7mo.txt"
input_file = "headers_txt_data.txt"

input_file_delimiter = "\t"

aa = ["q","w","e","r"]

#print(list(enumerate(aa)))

bb = zip( range(20000,20001,1), aa)
#print(list(range(3)))
#print(list(bb))

##for index, element in bb:
##    print(element)

#a = routine.wonder(("amo", "rati", "her"))

d = dict()
od = OrderedDict()

od["yks"] = 1
od["kaks"] = 2
od["kolme"] = 3

d["yks"] = 1
d["kaks"] = 2
d["kolme"] = 3

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


