import os

import csv

from collections import OrderedDict

from itertools import islice

input_file_delimiter = "\t"

null_values = [".", ""] # two possible kinds values for missing samples

null_values_new = "-999999" #

x_coord = ['LEFT_GAZE_X', 'RIGHT_GAZE_X']
y_coord = ['LEFT_GAZE_Y', 'RIGHT_GAZE_Y']

screen_x_dim = 1920.0 #screen width, adjust for differnt sites? 

screen_y_dim = 1020.0 #screen height, adjust for differnt sites?


##

def miracle(number):
    for x in range(0, number):
        print(str(number))

#miracle(3)


##

def wonder(args):
    for x, arg in enumerate(args):
        print(arg)
        #print(str(x))
        #print(args(x))

#miracle(3)
## [subcode]
def get_headers(dir_path ,input_file):

    #table for header pairs

    maptable = OrderedDict()#  {}#dict([('KEY','value')])


    #read dictionary key-value pairs from file,
    #1st column is for key and second/last column for values

    with open(os.path.join(dir_path, input_file), "rt", ) as inputfile:

        reader = csv.reader(inputfile, delimiter = input_file_delimiter)

        # grab header information, into maptable

        
        #all_lines = list(reader)

        #print (all_lines)
    
        for row in reader:
    
            #a = next(reader)
            #maptable[a[0]] = a[len(a)-1]
            maptable[row[0]] = row[len(row)-1] 
            #print(a)
            

        return maptable

##
#routine for processing gazedata, read, manipulate, return

#takes a list of argument including

    #input folder

    #input file

    #maptable, mapping old data headers (in "file") to new data headers
    
def file_process(t_args):

    input_folder = (t_args[0]) 
    
    input_file = (t_args[1])

    maptable = (t_args[2]) #OrderedDict where key is old and value new header


    print (" Filename matches with the specified file_ext -> processing..")    
   

    newrows = [] #processed data, process in function
    

    # input file reading

    with open(os.path.join(input_folder, input_file), "rt") as inputfile:

        reader = csv.reader(inputfile, delimiter = input_file_delimiter)
        

        # grab header information, into a list

        data_headers = next(reader) #reader.__next__() 
                

        # loop file rows and cols, 
        
        for r, row in islice(enumerate(reader), 0, 40): #None
            
            newrow = []

            for h, header in enumerate(maptable.keys()):#enumerate(header_keys):

                ncol = h #od_headers[key]
                                
                try: #try to accces data element

                    foo = row[ncol]

                except(IndexError): #if index oob, use element of previuous row

                    foo = newrows[r-1]

                    foo = foo[k]

                foo = manipulate(foo, header)
                
                newrow.append(foo)

            newrows.append(newrow)

    return newrows, maptable.values()#list(header_keys)
            

    
##
#routine for processing gazedata, read, manipulate, return


def manipulate(data, header):            

    # manipulate data

    # take away the null-values if they exist    

    foo = data

    if foo not in null_values: #if row[ncol] not in null_values:

        if header in x_coord: #['LEFT_GAZE_X', 'RIGHT_GAZE_X']:

            foo = float(foo) / screen_x_dim#newrow.append(float(foo) / screen_x_dim) #newrow.append(float(row[ncol]) / 1920.0)

        elif header in y_coord: #['LEFT_GAZE_Y', 'RIGHT_GAZE_Y']:

            foo = float(foo) / screen_y_dim #newrow.append(float(foo) / screen_y_dim) #newrow.append(float(row[ncol]) / 1020.0)

        else:

            foo = foo # newrow.append(foo) #newrow.append(row[ncol])

        return foo
        
    else:

        return null_values_new


##
def string_or_number(s):
    try:
        z = int(s)
        return z
    except ValueError:
        try:
            z = float(s)
            return z
        except ValueError:
            return s
