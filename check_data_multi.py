import os
import csv
from my_classes import DataFolder
from datetime import datetime, date
from collections import OrderedDict

# script for writing headers and data stats from different gazedata to file(s)

output_file = ("multi_folder_data_" + str(date.today()) + ".txt")
output_folder = os.getcwd()

# path to data testing eg., 7mo,trec2
folders = OrderedDict()

folders['tre5mo_old'] = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\5mo,trec2"
folders['tre5mo_new'] = "D:\\lasayr\\Aaltonen\\5mo"
folders['tre7mo_old'] = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\7mo,trec2"
folders['tre24mo_old'] = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\24mo, trec2"
folders['tre24mo_new'] = "D:\\lasayr\\Aaltonen\\24mo"
folders['ct_6mo'] = "D:\\lasayr\\Aaltonen\\ct\\6mo"
folders['ct_18mo'] = "D:\\lasayr\\Aaltonen\\ct\\18mo"
folders['hki'] = "D:\\lasayr\\Aaltonen\\hki"
folders['mi'] = "D:\\lasayr\\Aaltonen\\mi"

##

# list statistics from differt files to output "log"

# percentiles parameter for numerical stats
percentiles = (0.1,99.9)

with open(os.path.join(output_folder, output_file),
              "wt", newline = "\n") as outputfile:
            writer = csv.writer(outputfile, delimiter="\t")
    
for folder in folders:
    # use timer to time
    start_time = datetime.now()

    print(folders[folder])
    
    # create new DataFolder to be inspected/processed,         limit_files = (19,20) or (0, None)
    data_folder = DataFolder(folders[folder], limit_rows = 10, limit_files = (0,3))#   limit_files = (1,20))
    data_folder.set_output_folder(output_folder)
    #write stats directly with DataFolder class (to seprate files)
    data_folder.write_stats_to_file(percentiles)

    headers = data_folder.get_headers()
    output = []
    for header in headers:
        output.append(header + ":\t" + str(data_folder.get_stats(header)) +"\n")

    writer.writerow( str(datetime.now() - start_time)) #print time elapsed )
    writer.writerow( folder )
    writer.writerow( output )
            
##
##    

