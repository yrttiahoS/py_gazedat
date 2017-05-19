from collections import OrderedDict

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

    def __init__(self):
        self.i = 12345

    def f(self):
        return 'hello world'

    def get_i(self):
        return self.i



class GazeReader:
    """A class for Reading and processing gazedata"""
    
    def __init__(self, t_args):
        self.input_folder = (t_args[0]) 
        self.input_file = (t_args[1])
        self.maptable = (t_args[2]) #OrderedDict where key is old and value new header
#        self.newrows = [] #processed data, process in function
        datrows, datheaders = read_data()
        self.data_rows = datrows
        self.data_headers = datheaders
    
    
    def read_data():
    # input file reading

        with open(os.path.join(self.input_folder, self.input_file), "rt") as inputfile:
    
            reader = csv.reader(inputfile, delimiter = input_file_delimiter)
            
            
            # grab header information, into a list
    
            data_headers = next(reader) #reader.__next__() 
                    
    
            #data rows storage for this function
            
            newrows = []
    
            # loop file rows and cols, 
            
            for r, row in islice(enumerate(reader), 0, 40): #None
                
                newrow = []
    
                for h, header in enumerate(self.maptable.keys()):#enumerate(header_keys):
    
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
        
        
    
    