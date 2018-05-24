##Script for reading, modifying and re-writing gazedata
#%reset -f

import os
#import routine
from my_classes import DataFolder
from my_classes import HeaderReader

#read header conversion map 
folder = "C:/Users/lasayr/Documents/GitHub/py_gazedat"
file = "header map 3D_std.txt"
hr = HeaderReader(folder, file)

# Source folder:
input_folder = "C:\\Users\\lasayr\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\7mo,trec2"
#input_folder = "D:\\lasayr\\Aaltonen\\\ct\\ct_18mo"
#input_folder = "D:\\lasayr\\Aaltonen\\mi"
#input_folder = "D:\\lasayr\\Aaltonen\\24mo,trec2"
inFolderUnique = os.path.split(input_folder)[1]
output_folder = "C:\\Users\\lasayr\\Documents\\D\\Aaltonen\\" + inFolderUnique + "_std\\anon"

folder_an = 'C:\\Users\\lasayr\Documents\\D\\Aaltonen\\7mo,trec2_std\\anon'
input_folder = folder_an
output_folder = folder_an + '\\moreAnon'

# Init DataFolder
dl = "01 Jan 00"
data_folder = DataFolder(input_folder, map_header = hr, date_limit = dl ,limit_files = (0,2),  limit_rows = None)#, fileModelCur)#, limit_files = (0,3))#, limit_rows = 20, limit_files = (1,3))                         

#get files
files = data_folder.get_filelist()

# Print header map, conversion table
data_folder.print_header_map()

headers = data_folder.get_headers()

#data_folder.write_stats_to_file(percentiles = (1,99))

print("\nFiles selected: " + str(data_folder.get_filelist()))
# Change output folder, default is: C:\Users\Public\Documents\Tampereen yliopisto\Eye tracker\TRE Cohort 2\gazeAnalysisLib analyses\testing data
#data_folder.set_output_folder(output_folder)
data_folder.rewrite_data(output_folder, anonymize = True)        
    
