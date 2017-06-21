import os

import glob

import csv

from collections import OrderedDict # No need to import although GazeReader is

import routine

#initialized with an OrderedDict (!)

from itertools import islice

input_file_delimiter = "\t"

null_values = [".", "", "1.#INF", "-1.#INF", "1.#IND", "-1.#IND", 
               "-1.#QNAN" , "1.#QNAN", "-"] #  possible kinds values for missing samples

null_values_new = "-999999" #

x_coord = ['LEFT_GAZE_X', 'RIGHT_GAZE_X']
y_coord = ['LEFT_GAZE_Y', 'RIGHT_GAZE_Y']

screen_x_dim = 1920.0 #screen width, adjust for differnt sites? 

screen_y_dim = 1020.0 #screen height, adjust for differnt sites?



class MyClass:
    """A simple example class"""
    #i = 12345

    def __init__(self, arku = "qwerty"):
        self.i = 12345
        self.word = arku

    def f(self):
        if not self.word:
            return 'hello world'
        else:
            return self.word

    def get_i(self):
        return self.i



class GazeReader:
    """A class for Reading and processing gazedata"""

    def __init__(self, t_args, limit = None ):
        self.input_folder = (t_args[0]) 
        self.input_file = (t_args[1])
        self.maptable = (t_args[2]) #OrderedDict where key is old and value new header
#        self.newrows = [] #processed data, process in function
        self._limit_row = limit# (t_args[3]) # limit for rows to process, None if no limit
        datrows, datheaders = self.read_data()
        self.data_rows = datrows
        self.data_headers = datheaders

        self.data_od = {}#OrderedDict()
        
        self.r_ind = -1
            
    def read_data(self):
    # input file reading
        with open(os.path.join(self.input_folder, self.input_file), "rt") as inputfile:
            reader = csv.reader(inputfile, delimiter = input_file_delimiter)
        
            # grab header information, into a list
            data_headers = next(reader) #reader.__next__() 
                
            #data rows storage for this function            
            newrows = []

            if not self.maptable:
                return newrows, data_headers
            
            # loop file rows and cols,
            bad_row_found = False
            for r, row in islice(enumerate(reader), 0, self._limit_row): #None                
                newrow = []
                #loop cols
                for h, header in enumerate(self.maptable.keys()):#enumerate(header_keys):
                    try: #try to accces data element    
                        foo = row[h]    
                    except(IndexError): #
                        bad_row_found = True
                        print (str(row[h]))
                        break #break out from incomplete row
                        #foo = newrows[r-1], if index oob, use element of previuous row    
                    
                    foo = self._manipulate(foo, header)                    
                    newrow.append(foo)
                    
                if not bad_row_found:
                    newrows.append(newrow)
    
        return newrows, self.maptable.values()#list(header_keys)
##
    def get_data_stats(self, header_key):
    # returns min, max of number, or unique of strings of variable
    # uses OrderedDict self.data_od as main data structure
    # header_key is used to index specific variable
    
        # initialize data if not alreadey            
        if not self.data_od:
            self._odictionarize_data()

        # list of statistics from the current file/variable
        stats_file = self.data_od[header_key]

        # check if variable includes string values
        stats_include_str = []
        for stat in stats_file:
            if isinstance(stat, str): stats_include_str.append(1)
            else: stats_include_str.append(0)
        stats_include_str = any(stats_include_str)

        # extract min, max of numerical values
        if not stats_include_str:
            min_value = min(self.data_od[header_key])
            max_value = max(self.data_od[header_key])
            return_value = [min_value, max_value]
        # extract unique strings (no duplicates)
        else:
            return_value = (list(set(self.data_od[header_key])))

        return return_value


        
##
    def _odictionarize_data(self):
    # input file reading
    # this is "private" function for GazeReader
    # it reads fat into OrderedDict
    
        with open(os.path.join(self.input_folder, self.input_file), "rt") as inputfile:
            reader = csv.reader(inputfile, delimiter = input_file_delimiter)

            # grab header information, into a list
            headers = next(reader)

            # return if no good headers
            if not isinstance(headers[0], str):
                for i, el in enumerate(headers):
                    headers[el] = "Header_" + str(i)
                return "No string headers"
            
            #initialize od with headers as keys
            self.data_od = OrderedDict.fromkeys(headers) 
                
            # loop file rows and cols,             
            for r, row in islice(enumerate(reader), 0, self._limit_row): 
                newrow = []
                # loop cols
                for h, header in enumerate(self.data_od.keys()):
                    ncol = h 
                    try: # try to accces data element    
                        foo = row[ncol]    
                    except(IndexError): #i f index oob, use element of previuous row    
                        d = self.data_od[header]       
                        foo = d[len(d)-1]

                    # process data value    
                    foo = self._manipulate(foo, header)
                    # convert to number if possible
                    foo = routine.string_or_number(foo)
                    # initialize variable or append new value
                    if not self.data_od[header]:
                        self.data_od[header] = [foo]
                    else:
                        self.data_od[header].append(foo)
                    
          
##        
    def set_row_limit(self, number):
    # set limit for how may rows will be read from input file
        self._limit_row = number
        
        
    def _manipulate(self, data, header):            
    # manipulate data
    # more manipulations could be included...
    
        # take away the null-values if they exist    
        foo = data
        if foo not in null_values: 
            if header in x_coord: #['LEFT_GAZE_X', 'RIGHT_GAZE_X']:
                foo = float(foo) / screen_x_dim#newrow.append(float(foo) / screen_x_dim) #newrow.append(float(row[ncol]) / 1920.0)
            elif header in y_coord: #['LEFT_GAZE_Y', 'RIGHT_GAZE_Y']:      
                foo = float(foo) / screen_y_dim #newrow.append(float(foo) / screen_y_dim) #newrow.append(float(row[ncol]) / 1020.0)                
            else:
                foo = foo 
            return foo            
        else:            
            return null_values_new


    def get_row_count(self):        
    # returns the number of rows read and stored
        return (len(self.data_rows))

    def get_headers(self):        
    # returns list of headers
        return self.data_headers
        
    def get_new_row(self):        
    # returns a new data row at each call
        self.r_ind += 1        
        if self.r_ind < self.get_row_count():
            return self.data_rows[self.r_ind]
        else:
            return False
    
    def restart(self):
    # resets the counter for new data rows, starts over again
        self.r_ind = -1

##
class DataFolder:
    """A class for accessing gazedata in a specific folder                  """
    """We have many folders with vairiable gazedata. The headers,           """
    """datavalue scales, tags, and structure may all be variable.           """
    """With DataFolder, it is possible to output these things for comparison"""
##    
    def __init__(self,
                 path,
                 limit_rows = None,
                 limit_files = (0, None),
                 file_ext = ".gazedata",
                 input_file_delimiter = '\t',
                 map_header = None,
                 output_folder = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\testing data",
                 ): #t_args,

        self.dirpath = path # input folder path
        self.limit_rows = limit_rows # limit data rows per file processed
        self.limit_files = limit_files # limit n files
        self.file_ext = file_ext # input file type
        self.file_delimiter = input_file_delimiter # delimiter e.g., tab "\t"
        self.map_header = map_header # map for old and new headers
        self.output_folder = output_folder # output folder
        self.headers_folder = os.getcwd() # folder of header transform map

        self.folder_level_data = OrderedDict() # data from all files in folder

        # for investigating file headers
        # if no header map is provided, the aim is to
        # read headers "bottom-up" and store them to outputfile
        if not self.map_header:
            folder_path = os.path.split(self.dirpath)
            folder_tail = folder_path[1]            
            self.output_file = ( "headers in " + folder_tail + ".txt")

        # get list of files            
        self.diritems = os.listdir(path)
        #self.diritems = glob.glob(os.path.join(path,"*" ,file_ext)) //not work!
        print ("Directory contains " + str(len(self.diritems)) + " files.")

        
##
    def set_output_folder(self, folder):
    # chahnge output folder
        print ("Output to: " + folder)
        self.output_folder = folder

##
    def write_headers_to_file(self):
    # function for storing into outputfile headers used in files in the folder

        with open(os.path.join(self.output_folder, self.output_file), "wt") as outputfile:
                
            writer = csv.writer(outputfile, delimiter=self.file_delimiter)
    
            for filenum, file in islice(enumerate(self.diritems),  self.limit_files[0], self.limit_files[1]): 
                #print ("Checking file " + str(filenum + 1) + '/' + str(len(diritems)))
                if file.endswith(self.file_ext):
                    print(os.path.join(self.output_folder, self.output_file))
                    print ("Process file " + str(filenum + 1) + '/' + str(len(self.diritems)))
                    print(file)

                    #read in data, process, and strore in newrows
                    args_pro = self.dirpath, file, self.map_header
        
                    # make new GazeReader object for reading and processing input file
                    f_processor = GazeReader(args_pro, self.limit_rows) #40 is optional limit for rows
        
                    #f_processor.set_row_limit(40) # limit rows, good for debugging
                    row_list_to_write = f_processor.get_headers()
                    row_list_to_write.insert(0, file)
                    writer.writerow( row_list_to_write )

##
    def write_stats_to_file(self):
    # function for summarizing variable scales, with min-max or string tags

        # make specific output file with this function
        _output_file = "data stats and " + self.output_file

        # collect statistics from all files in folder    
        for filenum, file in islice(enumerate(self.diritems), self.limit_files[0], self.limit_files[1]): 
            #print ("Checking file " + str(filenum + 1) + '/' + str(len(diritems)))
            if file.endswith(self.file_ext):
                print(os.path.join(self.output_folder, self.output_file))
                print ("Process file " + str(filenum + 1) + '/' + str(len(self.diritems)))
                print(file)

                #read in data, process, and strore in newrows
                args_pro = self.dirpath, file, self.map_header
        
                # make new GazeReader object for reading and processing input file
                f_processor = GazeReader(args_pro, self.limit_rows) #40 is optional limit for rows
        
                for header in f_processor.get_headers():
                    stats = f_processor.get_data_stats(header)
                    if header not in self.folder_level_data.keys():
                        self.folder_level_data[header] = stats
                    else:
                        for el in stats:
                            self.folder_level_data[header].append(el)
                            if isinstance(el, str):
                                print(header + " has strings")
                            
                    #!!assign list instead!!!1

        #reduce statistical data for outputting                
        out_stats = OrderedDict()

        ##        
        # loop through variables/headers      
        for header in self.folder_level_data.keys():
            stats_folder = self.folder_level_data[header]

            # check if variable includes string values
            stats_include_str = []
            for stat in stats_folder:
                if isinstance(stat, str): stats_include_str.append(1)
                else: stats_include_str.append(0)         

            # extract min, max of numerical values
            if not any(stats_include_str):
                min_value = min(self.folder_level_data[header])
                max_value = max(self.folder_level_data[header])
                out_stats[header] = min_value, max_value
                
            # extract unique strings
            else:
                if all(stats_include_str):
                    out_stats[header] = sorted(list(set(self.folder_level_data[header])))
                else:
                    out_stats[header] = list(set(self.folder_level_data[header]))
                print(header + " has strings")
         
                #out_values += str(list(set(self.folder_level_data[header]))) + "/t"

        # do the writing
        with open(os.path.join(self.output_folder, _output_file), "wt") as outputfile:
            writer = csv.writer(outputfile, delimiter=self.file_delimiter)
            writer.writerow( out_stats.keys() )
            writer.writerow( out_stats.values() )

 ##                       

                    
                                                 
                        
                    

