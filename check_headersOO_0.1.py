import os
import csv
from my_classes import DataFolder
from datetime import datetime
from collections import OrderedDict

# script for writing headers from different gazedata to file(s)



# path to data
folder_path = ("D:\\lasayr\\Aaltonen\\mi") #+ folder_name)

# create new DataFolder to be inspected/processed
data_folder = DataFolder(folder_path)# limit_files = (1,None))#(1,100))

# target output to current working directory, cwd
data_folder.set_output_folder(os.getcwd())
            
#print(os.getcwd() )
    
##

# list headers from differt files to output "log"
start_time = datetime.now()
data_folder.write_headers_to_file()
print(datetime.now() - start_time) #print time elapsed
