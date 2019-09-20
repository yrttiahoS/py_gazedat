import os

import glob

import csv

import time

from collections import OrderedDict

from collections import namedtuple

import routine

from itertools import islice

import numpy as np

from datetime import date

import random

EMPTY_STRING = " "

HEADERFILENAME = 'headers.txt'

OBSOLETE_HEADER = 'OBSOLETE'

NULL_VALUES = [".", "", "1.#INF", "-1.#INF", "1.#IND", "-1.#IND", 
               "-1.#QNAN" , "1.#QNAN", "-"] #  possible kinds values for missing samples

NULL_VALUES_NEW = "-999999" #

INPUT_DELIMITER_DEFAULT = '\t'

X_COORD_HEADERS = ['LEFT_GAZE_X', 'RIGHT_GAZE_X']
Y_COORD_HEADERS = ['LEFT_GAZE_Y', 'RIGHT_GAZE_Y']
SUBJECT_HEADER = 'Filename'#'Subject'
STIM_HEADER = 'Stim'
TIME_HEADER = 'TETTime'
LATERAL_STIM_HEADER = 'LateralStimPos'

SCREEN_X_DIM = 1920.0 #screen width, adjust for differnt sites? 

SCREEN_Y_DIM = 1020.0 #screen height, adjust for differnt sites?



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

    def __init__(self, t_args, limit = None, percentiles = (1,99), anonymize = False ):
        self.input_folder = (t_args[0]) 
        self.input_file = (t_args[1])
        self.maptable = (t_args[2]) #OrderedDict where key is old and value new header
        #self.mapCurrent = (t_args[3]) #OrderedDict where key is old and value new header
#        self.newrows = [] #processed data, process in function
        self._limit_row = limit# (t_args[3]) # limit for rows to process, None if no limit
        self._input_file_delimiter = INPUT_DELIMITER_DEFAULT
        
        self.output_file = self.input_file
        
        # extension of the file extracted
        self.file_ext = os.path.splitext(self.input_file)[-1]
         
        # anonymize if needed
        if anonymize:
            self._anon, self._timestamp, = self._anonymize_fun() #finds 1st timevalue
        else:
            self._anon = False
                      
        print('Read data to GazeReader')
        datrows, datheaders = self._read_data()     #reads in data
        self.data_rows = datrows
        self.data_headers = datheaders

        self.data_od = {}#OrderedDict()

        # percentile points for extracting nearly min-max range of gazedata values
        print(percentiles[0])
        self.lo_perc = percentiles[0] 
        self.hi_perc = percentiles[1]
        
        self.r_ind = -1
        
    def _anonymize_fun(self):        
    # do anonymization-related procedures
        anonymizationBool = True
        
        timevalue = self._find_timestart()
    
        file_anon = 'Anon-' + time.strftime("%H%M%S", time.localtime()) + '%d' % (time.time() % 1 * 1000)    
        self.set_filename_out(file_anon)
        
        return anonymizationBool, timevalue   
        
    def _read_data(self):
    # input file reading
    # this should be private?
    # this doesn't return data if no maptable provided...
    # this returns headers anyway

        # First row of data values is by default 1,
        # that is, first col after headers. If no headers must
        # be set 0.
        #first_datarow = 1

        with open(os.path.join(self.input_folder, self.input_file), "rt") as inputfile:
            reader = csv.reader(inputfile, delimiter = self._input_file_delimiter)
        
            # Grab header information, into a list
            data_headers = next(reader) #reader.__next__() 

            # Check if headers are numerical (or strings that can
            # be converted to numbers).
            headers_numform=[]
            truly_strings=[]
            for header in data_headers:                
                # Convert header to num if possible.
                headers_numform.append(routine.string_or_number(header))
                # Check if header remained a string.
                truly_strings.append(isinstance(headers_numform[-1], str)) #[-1] is the last element...!
            # If no good headers (i.e., strings) make headers empty.
            if not all(truly_strings):
                data_headers = self._read_headers()
                # "Restart" the reader, so that no data will be missed afterwards.
                inputfile.seek(0) 

                                
            # Data rows storage for this function            
            newrows = []
            
            if not self.maptable:
                newheaders = data_headers
                return newrows, data_headers

            hdrKeys = self.maptable.getKeys()
            #newheaders = [] #['' for i in range(len(hdrKeys))]
            newheaders = [" " for i in range(self.maptable.get_n_of_uniqueCols())]

            #make new headers
            for header in enumerate(hdrKeys):#enumerate(header_keys):
                if not self.maptable.get_header_newName(header[1]) == OBSOLETE_HEADER:
                    newCol = self.maptable.get_header_colNum(header[1])-1
                    newheaders.pop(newCol)
                    newheaders.insert(newCol,self.maptable.get_header_newName(header[1]))
                    
            
            # Loop file rows and cols,
            for r, row in islice(enumerate(reader), 0, self._limit_row): #None                
                # initialize newrow as list with elements upto deisred cols
                newrow = [EMPTY_STRING for i in range(len(newheaders))]#[" " for i in range(self.maptable.get_n_of_uniqueCols())]

                #Loop Headers
                for header in enumerate(hdrKeys):#enumerate(header_keys):
                    # Find column number of Standard Header
                    # from current input file's headers
                    try:
                        col = data_headers.index(header[1])
                        #print("header: "+header[1])
                        #print("col: "+ str(col))
                    except(ValueError):
                        col = -1
                        #print("header: "+header[1])
                        #print("header not found in current input")
                    
                    if col < len(row) and col > 0:
                        dataCell = row[col]
                    else:
                        dataCell = EMPTY_STRING
                        
                    a = self._anon    
                    dataCell = self._manipulate(dataCell, self.maptable.get_header_newName(header[1]), a)
                    if not self.maptable.get_header_newName(header[1]) == OBSOLETE_HEADER:
                        newCol = self.maptable.get_header_colNum(header[1])-1
                        #print(header[1])
                        #print('newCOl: ' + str(newCol))
                        #newrow.append(dataCell)
                        if newrow[newCol] == EMPTY_STRING:
                            newrow.pop(newCol)
                            newrow.insert(newCol, dataCell)
                                
                newrows.append(newrow)
                
    
        return newrows, newheaders#self.maptable.values()#list(header_keys)
##
    def get_data_stats(self, header_key):
    # returns ~min, ~max of number (actually lo/hi percentiles)
    # or unique of strings of variable
    # uses OrderedDict self.data_od as main data structure
    # header_key is used to index specific variable

        if not header_key:
            return []
            
        # initialize data if not alreadey            
        if not self.data_od:
            self._odictionarize_data()

        # list of statistics from the current file/variable
        stats_file = self.data_od[header_key]
        if not stats_file:
            print("no data for: " + header_key)
            return []

        # check if variable includes string values
        stats_include_str = []
        for stat in stats_file:
            if isinstance(stat, str): stats_include_str.append(1)
            else: stats_include_str.append(0)
        stats_include_str = any(stats_include_str)

        # extract min, max of numerical values
        if not stats_include_str:
            min_value = np.percentile(self.data_od[header_key] , self.lo_perc) #min(self.data_od[header_key])
            max_value = np.percentile(self.data_od[header_key] , self.hi_perc)
            return_value = [min_value, max_value]
        # extract unique strings (no duplicates)
        else:
            return_value = (list(set(self.data_od[header_key])))

        return return_value


##
    def _find_timestart(self):
    # input file reading
    # this is "private" function for GazeReader
    # it returns the timestamp of first ET frame
    # (Can be used for anonymization, when removing unique timestamp...)

        # Only some first data rows are needed for this function
        # So set row limit to some small number (2 enuff?)
        limit_original = self._limit_row 
        self._limit_row = 10

        # Run data into Ordered Dictionary
        # initialize variable to zero
        #self._timestamp = 0
        self._odictionarize_data(anonymize = False)
        # Find 1st timevalue
        timeval =  self.data_od[TIME_HEADER][0]
        
        #Return things as default
        self.data_od = {}#OrderedDict()
        self._limit_row = limit_original
            
        # return
        return timeval
    
    
##
    def _odictionarize_data(self, anonymize = False):
    # input file reading
    # this is "private" function for GazeReader
    # it reads fat into OrderedDict
    
        with open(os.path.join(self.input_folder, self.input_file), "rt") as inputfile:
            reader = csv.reader(inputfile, delimiter = self._input_file_delimiter)

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
                #newrow = []
                # loop cols
                for h, header in enumerate(self.data_od.keys()):
                    try: # try to accces data element    
                        foo = row[h]    
                    except(IndexError): #if index oob, use element of previuous row                                                
                        #print("bad row: " + str(r) + " for: " + header)
                        foo = []

                    # process data value    
                    foo = self._manipulate(foo, header, anonymize)
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

    def set_percentiles(self, lo_percentile, hi_percentile):
    # set percentiles for very low and high data values
        self.lo_perc = lo_percentile 
        self.hi_perc = hi_percentile

    def _read_headers(self):
    # read headers from current folder

            print("Writing headers from a separate file for " + self.input_file + ".")
        
            with open(os.path.join(self.input_folder, HEADERFILENAME), "rt") as inputfile:
                reader = csv.reader(inputfile, delimiter = self._input_file_delimiter)
                headers = next(reader)
                return headers
                
    
    def _manipulate(self, dataIn, header, anonymize = False):            
    # manipulate data
    # more manipulations could be included...
            
        if not dataIn: return NULL_VALUES_NEW
        else: dataOut = dataIn

        #truth = isinstance("1", int)
        #routine.string_or_number(123)
        
        # take away the null-values if they exist    
        if dataOut not in NULL_VALUES: 
            if header == SUBJECT_HEADER: #eg. "Subject"
                    if dataIn == EMPTY_STRING:
                        dataOut = self.input_file
                    if anonymize: # set filename to anonynous 
                        dataOut = self.output_file
            elif header == STIM_HEADER: #eg. "Stim"
                dataIn = routine.string_or_number(dataIn)
                if isinstance(dataIn, str):
                    dataOut = dataIn
                else:
                    dataIn = int(dataIn)
                    if   1 <= dataIn <= 2:
                        dataOut = "fearful.bmp"
                    elif 3 <= dataIn <= 4:
                        dataOut = "control.bmp"
                    elif 5 <= dataIn <= 6:
                        dataOut = "happy.bmp"
                    elif 7 <= dataIn <= 8:
                        dataOut = "neutral.bmp"
                        
            elif header == LATERAL_STIM_HEADER: #eg. "LateralStimPos"
                #print(dataIn)
                if routine.string_or_number(dataIn) == 1:
                    dataOut = "left"
                elif routine.string_or_number(dataIn) == 2:
                    dataOut = "right"
            
            elif header == TIME_HEADER: #eg. "LateralStimPos"
                #print(dataIn)
                #try: #Possible error caused by non-existing var: self._anon 
                if anonymize:
                    dataOut = str(float(dataIn) - self._timestamp)
                #except AttributeError:   
                #    pass
                    #print('variable \"self._anon\" not found')
                                    
                    
            #print("dataOut = right")
            # Currently no need for scaling gaze coordinates...
            #elif header in X_COORD_HEADERS: #['LEFT_GAZE_X', 'RIGHT_GAZE_X']:
            #    dataOut = float(dataOut) / SCREEN_X_DIM#newrow.append(float(dataOut) / SCREEN_X_DIM) #newrow.append(float(row[ncol]) / 1920.0)
            #elif header in Y_COORD_HEADERS: #['LEFT_GAZE_Y', 'RIGHT_GAZE_Y']:      
            #    dataOut = float(dataOut) / SCREEN_Y_DIM #newrow.append(float(dataOut) / SCREEN_Y_DIM) #newrow.append(float(row[ncol]) / 1020.0)
            else:
                dataOut = dataOut
            return dataOut            
        else:
            #print(header)
            return NULL_VALUES_NEW


    def get_filename(self, no_ext = True, in_out = 'out'):        
    # returns the file being read/processed
    # in_out defines whether input or output filename is returned
    
        if in_out == 'out':
            fn = self.output_file
        elif in_out == 'in':
            fn = self.input_file
        else:
            print("Only in/out are acceptable parameter values!")
        
        if no_ext:
            #return filename without extension
            #find extendsion start
            i_ext = fn.find('.') 
            return fn[0:i_ext]
        else:
            return fn

    def get_row_count(self):        
    # returns the number of rows read and stored
        return (len(self.data_rows))

    def get_headers(self):        
    # returns list of headers

        # if no maptable for headers available, return "plain" headers
        if not self.maptable:
            return self.data_headers
        # if conversion map for new headers available, return new headers
        else:
            if isinstance(self.maptable, HeaderReader):
                newheaders = self.data_headers# list(self.maptable.values()) #list(d.values())
            # remove obsolete headers
            if OBSOLETE_HEADER in newheaders:
                newheaders.remove(OBSOLETE_HEADER)
            return newheaders
        
    def get_new_row(self):        
    # returns a new data row at each call
        self.r_ind += 1        
        if self.r_ind < self.get_row_count():
            return self.data_rows[self.r_ind]
        else:
            return False
    
    def set_filename_out(self, filename_new):        
    # sets a new name fot the file being read/processed
        fn  = str(filename_new)
        if fn.endswith(self.file_ext):
            self.output_file = fn
        else:
            self.output_file = fn + self.file_ext

    
    
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
                 date_limit = "1 Jan 00",
                 date_limit_type = "c", #c=created, m=modified
                 #map_header_current = None,
                 output_folder = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\testing data",
                 ): #t_args,

        self.dirpath = path # input folder path
        self.limit_rows = limit_rows # limit data rows per file processed
        self.limit_files = limit_files # limit n files
        self.file_ext = file_ext # input file type
        self.file_delimiter = input_file_delimiter # delimiter e.g., tab "\t"
        # first header map is for the exemplary data
        self.map_header = map_header # map for old and new headers,
        # second header map is for current data folder idiosyncracies
        #self.map_header_current = map_header_current # map for old and new headers
        self.date_limit = time.strptime(date_limit, "%d %b %y")
        self.output_folder = output_folder # output folder
        self.headers_folder = os.getcwd() # folder of header transform map

        self.folder_level_data = OrderedDict() # data from all files in folder
        self.out_stats = OrderedDict() #extracted descriptive stat

        # for investigating file headers
        # if no header map is provided, the aim is to
        # read headers "bottom-up" and store them to outputfile
        if not self.map_header:
            folder_path = os.path.split(self.dirpath)
            folder_tail = folder_path[1]            
            self.output_file = ( "headers in " + folder_tail + "_" +
                                 str(date.today()) + ".txt")
        else:
            self.output_file = ( "output_"  + str(date.today()) + ".txt")
        

        # get list of files            
        #self.diritems = os.listdir(path)
        self.diritems  = [fileName for fileName in os.listdir(path) if fileName.endswith(file_ext)]
        self.diritems = self.diritems[self.limit_files[0]:self.limit_files[1]]
        self.diritems = self.timethreshold_items(self.diritems,date_limit_type)
        print("-------------------------")
        print("Files selected: " + str(self.diritems))
        print("-------------------------")
        #self.diritems = glob.glob(os.path.join(path,"*" ,file_ext)) //not work!
        #print ("Directory contains " + str(len(self.diritems)) + " files.")

        
##
    def set_output_folder(self, folder):
    # chahnge output folder
        print ("Output to: " + folder)

        if not os.path.isdir(folder):
            os.mkdir(folder)
        
        self.output_folder = folder

##
    def write_headers_to_file(self):
    # function for storing into outputfile headers used in files in the folder

        with open(os.path.join(self.output_folder, self.output_file),
                  "wt", newline = "\n") as outputfile:
                
            writer = csv.writer(outputfile, delimiter=self.file_delimiter)
    
            for filenum, file in islice(enumerate(self.diritems),  self.limit_files[0], self.limit_files[1]): 
                #print ("Checking file " + str(filenum + 1) + '/' + str(len(diritems)))
                if file.endswith(self.file_ext):
                    #print(os.path.join(self.output_folder, self.output_file))
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
    def write_stats_to_file(self, percentiles):
    # function for summarizing variable scales, with min,max or string tags

        # make specific output file with this function
        _output_file = "daata stats and " + self.output_file

        # collect statistics from all files in folder    
        for filenum, file in islice(enumerate(self.diritems), self.limit_files[0], self.limit_files[1]): 
            #print ("Checking file " + str(filenum + 1) + '/' + str(len(self.diritems)))
            if file.endswith(self.file_ext):
                #print(os.path.join(self.output_folder, self.output_file))
                print ("Process file " + str(filenum + 1) + '/' + str(len(self.diritems)))
                print(file)

                #read in data, process, and strore in newrows
                args_pro = self.dirpath, file, self.map_header
        
                # make new GazeReader object for reading and processing input file
                f_processor = GazeReader(args_pro, self.limit_rows, percentiles) #40 is optional limit for rows

                for header in f_processor.get_headers():
                    #print("header: " + header)
                    stats = f_processor.get_data_stats(header)
                    if header not in self.folder_level_data.keys():
                        self.folder_level_data[header] = stats
                    else:
                        for el in stats:
                            self.folder_level_data[header].append(el)
                            #if isinstance(el, str):
                                #print(header + " has strings")
                            
                    #!!assign list instead!!!1

        #reduce statistical data for outputting                
        #self.out_stats  already defined at __init__()

        ##        
        # loop through variables/headers      
        for header in self.folder_level_data.keys():
            stats_folder = self.folder_level_data[header]

            if not stats_folder: continue
            
            # check if variable includes string values
            stats_include_str = []
            for stat in stats_folder:
                if isinstance(stat, str): stats_include_str.append(1)
                else: stats_include_str.append(0)         

            # extract min, max of numerical values
            if not any(stats_include_str):
                min_value = min(self.folder_level_data[header])
                max_value = max(self.folder_level_data[header])
                self.out_stats[header] = min_value, max_value
                
            # extract unique strings
            else:
                if all(stats_include_str):
                    self.out_stats[header] = sorted(list(set(self.folder_level_data[header])))
                else:
                    self.out_stats[header] = list(set(self.folder_level_data[header]))
                #print(header + " has strings")
         

        # do the writing
        with open(os.path.join(self.output_folder, _output_file),
                  "wt", newline = "\n") as outputfile:
            writer = csv.writer(outputfile, delimiter=self.file_delimiter)
            writer.writerow( self.out_stats.keys() )
            writer.writerow( self.out_stats.values() )

 ##
    def rewrite_data(self, outputfolderIn = None, anonymize = False):
    #function for rewriting data with new format

        if outputfolderIn:
            self.set_output_folder(outputfolderIn)
        
        if anonymize:   
            random.shuffle(self.diritems)
        
        # access data from all files in folder    
        for filenum, file in islice(enumerate(self.diritems), self.limit_files[0], self.limit_files[1]): 
            #print ("Checking file " + str(filenum + 1) + '/' + str(len(diritems)))
            if file.endswith(self.file_ext):
                #print(os.path.join(self.output_folder, self.output_file))
                print ("\nProcess file " + str(filenum + 1) + '/' + str(len(self.diritems)))
                print(file + '\n') 
                print("Write new file to: " + self.output_folder)

                #read in data, process, and strore in newrows
                args_pro = self.dirpath, file, self.map_header#,
                #self.map_header_current  #None#self.map_header

                # make new GazeReader object for reading and processing input file
                f_processor = GazeReader(args_pro, self.limit_rows, anonymize = anonymize)#, percentiles = percentiles) #40 is optional limit for rows

                # make name for new gazedata file
                _output_file = (f_processor.get_filename(no_ext=True) + "_std.gazedata")
                print(_output_file)
                # output/gazedatafile opening
                with open(os.path.join(self.output_folder, _output_file),
                  "wt", newline = "\n") as outputfile:

                    writer = csv.writer(outputfile, delimiter=self.file_delimiter)

                    #write headers to new file
                    headers = f_processor.get_headers()
                    
                    #NEW HEADERS ARE ALREADY IN USE FOR GazeReader, if initialized with a header map!!!
                    writer.writerow( headers )
                    
                    #write data rows to new file
                    found_new_row = f_processor.get_new_row()
                    while found_new_row:
                        #print(found_new_row)
                        writer.writerow( found_new_row )
                        found_new_row = f_processor.get_new_row()
                        
 ##           
    def get_headers(self):        
        # returns list of headers
        
        #if stats calculated do this
        if len(self.out_stats.keys()) > 0:
            return self.out_stats.keys()
        else:
            #read in data from first file to get it's headers
           args_pro = self.dirpath, self.diritems[1], self.map_header
        
           # make new GazeReader object for reading and processing input file
           limit_rows = 1
           f_processor = GazeReader(args_pro, limit_rows)
           return f_processor.get_headers()
        
        

    def get_stats(self, header):
        #return stats of specific variable
        return self.out_stats[header]

    def timethreshold_items(self, items, type):
        #return stats of specific variable

        items_v2 = []
        timeThreshold = time.mktime(self.date_limit) 
        print("Number of files in folder: " + str(len(items)))
        for itemNum, item in (enumerate(items)): 
            if type == "m": 
                itemModified = os.path.getmtime(self.dirpath + '\\' + item)
            if type == "c":
                itemModified = os.path.getctime(self.dirpath + '\\' + item)
            if itemModified < timeThreshold:
                print(item + " is too old")                
            else:
                filedate = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(itemModified))
                items_v2.append(item)
                print(item + " has good date: " + filedate)
        print("Number of files selected for processing: " + str(len(items_v2)))
        return items_v2

    def get_filelist(self):
        #return stats of specific variable
        return self.diritems
    

    def print_header_map(self):
        print("List header map, folder: "+ self.dirpath +"; old: new")

        #try if the self.map_headers is ordered dictionary
        try: 
            for k in self.map_header.keys():
                print (k + ": " + self.map_header[k])
                
        except(AttributeError): #if it is HeaderReader
            for k in self.map_header.getKeys():
                #print(k)
                print (k + ": " + self.map_header.get_header_newName(k) +
                       ", col: " + str(self.map_header.get_header_colNum(k)))

class HeaderReader:
    """A class for Reading and processing Headers"""

    def __init__(self, path, file ):

        self.file = file #
        self.path = path #
        self._input_file_delimiter = INPUT_DELIMITER_DEFAULT
        self.od = self._read_headers()
            
        
        
    def _read_headers(self):        
        # returns list of headers

        od = OrderedDict()
        
        headerInfo = namedtuple('headerInfo', 'newName colNum')
        
        with open(os.path.join(self.path, self.file), "rt", ) as inputfile:

            reader = csv.reader(inputfile, delimiter = self._input_file_delimiter)

            # grab header information, into 
      
            for row in reader:
                #print(row)
                #maptable[row[0]] = row[len(row)-1] 
                #od['TitanicThing'] = Strong('FamousName', 88)
                od[row[0]] = headerInfo(row[1], row[2])
            
            
        return od


    def getKeys(self):
        return self.od.keys()

    def get_n_of_uniqueCols(self):
        nCols = 0
        previousColNum = -1
        for key in self.od.keys():
            thisColNum = self.get_header_colNum(key)
            if  thisColNum != previousColNum and thisColNum > 0:
                nCols += 1
                #print(key)
                #print(thisColNum)
            previousColNum = thisColNum
                
        return nCols
        

    def get_header_colNum(self, header):

        return int(self.od[header].colNum)
    
    def get_header_newName(self, header):
        #print(header)
        return self.od[header].newName

    
                                                 
                        
                    

