import os

import csv

#from collections import OrderedDict # No need to import although GazeReader is

#initialized with an OrderedDict (!)

from itertools import islice

input_file_delimiter = "\t"

null_values = [".", ""] # two possible kinds values for missing samples

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
            for r, row in islice(enumerate(reader), 0, self._limit_row): #None                
                newrow = []
                #loop cols
                for h, header in enumerate(self.maptable.keys()):#enumerate(header_keys):
                    ncol = h #od_headers[key]                                    
                    try: #try to accces data element    
                        foo = row[ncol]    
                    except(IndexError): #if index oob, use element of previuous row    
                        foo = newrows[r-1]    
                        foo = foo[k]
    
                    foo = self._manipulate(foo, header)                    
                    newrow.append(foo)
    
                newrows.append(newrow)
    
        return newrows, self.maptable.values()#list(header_keys)
        
        
    def set_row_limit(self, number):
        self._limit_row = number
        
        
    def _manipulate(self, data, header):            
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


class DataFolder:
    """A class for accessing gazedata in a specific folder"""
    
    def __init__(self,
                 path,
                 limit_rows = None,
                 limit_files = None,
                 file_ext = ".gazedata",
                 input_file_delimiter = '\t',
                 map_header = None,
                 output_folder = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\testing data",
                 ): #t_args,

        self.dirpath = path
        self.limit_rows = limit_rows
        self.limit_files = limit_files
        self.file_ext = file_ext
        self.file_delimiter = input_file_delimiter
        self.map_header = map_header
        self.output_folder = output_folder
        self.headers_folder = os.getcwd()

        if not self.map_header:
            folder_path = os.path.split(self.dirpath)
            folder_tail = folder_path[1]            
            self.output_file = ( "headers in " + folder_tail + ".txt")
                    
        self.diritems = os.listdir(path)
        print ("Directory contains " + str(len(self.diritems)) + " files.")

        print(self.file_delimiter)

        #self.greader = GazeReader(t_args, limit)


    def set_output_foldder(self, folder):
        self.output_folder = folder


    def write_headers_to_file(self):

        with open(os.path.join(self.output_folder, self.output_file), "wt") as outputfile:
                
            writer = csv.writer(self.outputfile, delimiter=self.file_delimiter)
    
            for filenum, file in islice(enumerate(self.diritems), 0, self.limit_files): 
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

