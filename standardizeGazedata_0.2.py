##Script for reading, modifying and re-writing gazedata
##*this will have some algorithms from
##gazedata2gazedata_sy3.py and the like, but should use classes in my_classes.py
##*use DataFolder class to access all gazefiles in folder
##	**write new method for writing new data into folder
##		*method will loop through files, i.e., GazeReader objects
##		*method will read (gettinf from GazeReader), 
##			    change (by accessing separate textfile),
##				 and write headers to new file (use writer object?)
##		*method will read, change, and write datarow one-by-one into new file,
##			same logic as with headers, changing might be more tricky?
##		*i.e., GazeReader will never have to give up entire data!

## first things 1st

import routine
from my_classes import DataFolder

# Set folder and data for header conversion map
folder = "C:/Users/infant/Documents/GitHub/py_gazedat"
fileModelHM = "header map.txt"
fileModelCur = "??????.txt"

# Read old-new conversion map, for headers
hmModel = routine.get_headers(folder,fileModelHM)
hmCurrent = routine.get_headers(folder,fileModelCur)


#vals = list(hm.values()) #list(d.values())
#vals.remove('OBSOLETE')
#print(vals)

## then do some business

# Source folder:
input_folder = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\7mo,trec2"
output_folder = "D:\\lasayr\\Aaltonen\\TREc2_7mo_std"

# Init DataFolder
data_folder = DataFolder(input_folder, map_header = hm)#, limit_files = (0,3))#, limit_rows = 20, limit_files = (1,3))                         

# Print header map, conversion table
data_folder.print_header_map()

# Change output folder, default is: C:\Users\Public\Documents\Tampereen yliopisto\Eye tracker\TRE Cohort 2\gazeAnalysisLib analyses\testing data
#data_folder.set_output_folder(output_folder)

data_folder.rewrite_data(output_folder)        
    
