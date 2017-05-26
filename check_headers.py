import os

import csv

#import routine

#from collections import OrderedDict

from itertools import islice

from my_classes import GazeReader


input_folder = 'testing 7mo,trec2' #"C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\testing 7mo,trec2"

n_files = 1 # set limit for files to be processed, None if no limit desired

output_folder = os.getcwd()#"C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\testing data"

output_file = "headers listing"

file_ext = ".gazedata" #input file extension, .txt

input_file_delimiter = "\t"

output_file_delimiter = input_file_delimiter

headers_folder = os.getcwd() #path for headers inputfile

headers_inputfile = "headers_tre_5mo_to_7mo.txt"

# find directory by "walking" through the system

for root, dirs, files in os.walk('C:\\Users\\'):
    
    if input_folder in root:      
    
        print(root, " ", end=" FOUND! ")
        
        print("")
        
        input_folder = root
        
print (input_folder)

# list files in a directory, 

diritems = os.listdir(input_folder)

print ("Directory contains " + str(len(diritems)) + " files.")



headers_in_files = []

#loop through files, limit loop by isslice(items, start, stop), can be None

for filenum, file in islice(enumerate(diritems), 0, n_files): 

    #print ("Checking file " + str(filenum + 1) + '/' + str(len(diritems)))

    if file.endswith(file_ext):

        print ("Process file " + str(filenum + 1) + '/' + str(len(diritems)))

        print(file)


        #read in data, process, and strore in newrows

        args_pro = input_folder, file, map_header
        
        
        # make new GazeReader object for reading and processing input file 
        
        f_processor = GazeReader(args_pro, 40) #40 is optional limit for rows
        
        f_processor.set_row_limit(40) # limit rows, good for debugging
        
        #        print("Newrows length: " + str(f_processor.get_row_count()))
    
        headers_in_files.append(str(filenum) + output_file_delimiter + f_processor.get_headers())
        # open output file

with open(os.path.join(output_folder, output_file), "wt") as outputfile:

    writer = csv.writer(outputfile, delimiter=output_file_delimiter)

    for ii in enumerate(headers_in_files):
    
        writer.writerow(ii)
        
