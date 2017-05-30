import os
import csv
from my_classes import DataFolder

# script for writing headers from different gazedata to file(s)



# path to data
folder_path = ("D:\\lasayr\\Aaltonen\\mi") #+ folder_name)

# create new DataFolder to be inspected/processed
data_folder = DataFolder(folder_path, limit_files = 1)

# target output to current working directory, cwd
data_folder.set_output_folder(os.getcwd())
            
#print(os.getcwd() )
    
##

# list headers from differt files to output "log"
data_folder.write_headers_to_file()
