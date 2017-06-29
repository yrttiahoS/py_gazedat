import os
import csv
from my_classes import DataFolder
from datetime import datetime, date
from collections import OrderedDict

# script for writing headers and data stats from different gazedata to file(s)

##
#parameter setting

#set output file
output_file_name = ("multi_folder_data_" + str(date.today()) + ".txt")
output_folder = os.getcwd()

#limits data analysis for quick peek...
limit_last_row = None
limit_last_file = None

# percentiles parameter for numerical stats
percentiles = (0.1,99.9)

# paths to data eg., 7mo,trec2
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

#testing with only some folders
folders = OrderedDict()
folders['tre24mo_old'] = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\24mo, trec2"
folders['tre24mo_new'] = "D:\\lasayr\\Aaltonen\\24mo"
folders['ct_6mo'] = "D:\\lasayr\\Aaltonen\\ct\\6mo"
folders['ct_18mo'] = "D:\\lasayr\\Aaltonen\\ct\\18mo"

##
#write "logfile" output to list statistics from differt files
with open(os.path.join(output_folder, output_file_name),
                  "wt", newline = "\n") as outputfile:
    #construct csv.writer based on outputfile
    writer = csv.writer(outputfile, delimiter="\t")

    #loop through folders containing gazedata files    
    for folder in folders:
        # use timer to time
        start_time = datetime.now()
        #print folder at hand for tracking process
        print("\n" + "process folder: " + folders[folder])
    
        # create new DataFolder to be inspected/processed,         
        data_folder = DataFolder(folders[folder],
                                 limit_rows = limit_last_row,
                                 limit_files = (0,limit_last_file)) 
        data_folder.set_output_folder(output_folder)
    
        #write stats directly with DataFolder class (to seprate files)
        data_folder.write_stats_to_file(percentiles)

        #"logfile", based on data headers
        writer.writerow( [folder]) #print time elapsed )
        writer.writerow( [str(datetime.now() - start_time)]) #print time elapsed )
        headers = data_folder.get_headers()
        output = []
        for header in headers:
            writer.writerow([header] + [str(data_folder.get_stats(header))]) 
        writer.writerow([])
