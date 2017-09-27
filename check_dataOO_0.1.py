import os
import csv
from my_classes import DataFolder
from datetime import datetime

# script for writing headers and data stats from different gazedata to file(s)

# path to data testing eg., 7mo,trec2

tre5mo_old = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\5mo,trec2"
tre7mo_testin = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\testing 7mo,trec2"
tre7mo_old = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\7mo,trec2"
mi = ("D:\\lasayr\\Aaltonen\\mi") #+ folder_name)

folder_path = tre7mo_old

# create new DataFolder to be inspected/processed, limit_files = (19,20) or (0, None)
data_folder = DataFolder(folder_path, limit_rows = 100, limit_files = (2600,2600+10))

# target output to current working directory, cwd
data_folder.set_output_folder(os.getcwd())

##

# list statistics from differt files to output "log"
start_time = datetime.now()
#percentiles parameter for numerical stats
percentiles = (0.1,99.9)
data_folder.write_stats_to_file(percentiles)
print(datetime.now() - start_time) #print time elapsed

headers = data_folder.get_headers()
for header in headers:
    print(header + ": " + str(data_folder.get_stats(header)))
    

