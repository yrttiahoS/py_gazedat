import os
import csv
from my_classes import DataFolder

# script for writing headers and data stats from different gazedata to file(s)

# path to data testing 7mo,trec2
folder_path = ("C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\5mo,trec2")
#"C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\testing 7mo,trec2"
#("D:\\lasayr\\Aaltonen\\mi") #+ folder_name)


# create new DataFolder to be inspected/processed
data_folder = DataFolder(folder_path, limit_rows = None, limit_files = (19,20))

# target output to current working directory, cwd
data_folder.set_output_folder(os.getcwd())

##

# list statistics from differt files to output "log"
data_folder.write_stats_to_file()
