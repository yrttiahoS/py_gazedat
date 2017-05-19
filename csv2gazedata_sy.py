import os

import csv



# This Jussi's script converts eyetracking data in txt-format to gazedata-format

# It also converts X- and Y- coordinates to relative values for screen size.

# Input folder needs to be relative to the script location in the folder tree.

# In this case the folder where this script is located needs to have a folder

# named "files_to_change" where the files are located.

# In GitHub

input_folder = folder = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\7mo,trec2"
#input_folder = folder = "C:\Users\Public\Documents\Tampereen yliopisto\Eye tracker\TRE Cohort 2\gazeAnalysisLib analyses\7mo,trec2"

output_folder = "C:\\Users\\Public\\Documents\\Tampereen yliopisto\\Eye tracker\\TRE Cohort 2\\gazeAnalysisLib analyses\\testing data"

ending = ".gazedata" #input file extension, .txt

output_file_ending = ".gazedata"

input_file_delimiter = "\t"

null_values = [".", ""] # two possible kinds values for missing samples

replace_null_values = "-999999" # 

screen_x_dim = 1920.0 #screen width, adjust for differnt sites? 

screen_y_dim = 1020.0 #screen height, adjust for differnt sites?


 


#map for one type of "gazedata" (or txt) headers, values may not apply to all gazedata 
maptable = {"TIMESTAMP":"TETTime",

            "RECORDING_SESSION_LABEL":"Subject",

            "LEFT_GAZE_X":"XGazePosLeftEye",

            "LEFT_GAZE_Y":"YGazePosLeftEye",

            "RIGHT_GAZE_X":"XGazePosRightEye", 

            "RIGHT_GAZE_Y":"YGazePosRightEye",

            "TRIAL_INDEX":"TrialId",

            "SAMPLE_MESSAGE":"UserDefined_1",

            "RIGHT_PUPIL_SIZE":"DiameterPupilRightEye",

            "stimulus_right_2":"Stim",

            "__target_x__1":"Target"}





#subroutine for processing one file
def file_process(file):
    #if file.endswith(ending):

        print (" Filename matches with the specified ending -> processing..")

        #self.liststore_exp.append([file])

        input_file = file



        # input file reading

        newrows = []

        with open(os.path.join(input_folder, input_file), "rt") as inputfile:

            reader = csv.reader(inputfile, delimiter = input_file_delimiter)
            #reader.line_num())


            # grab header information, into a list

            headers = reader.__next__() #next(reader) #
            #print(headers)


            # calculate list index numbers for map-keys

            indexed_maptable = {}

            for key in maptable:
                print("key: " + key)
                print("index of header: " + str(headers.index("Subject")))
                print ("headers index key: " +headers.index(key))
                indexed_maptable[key] = headers.index(key)



            # loop file rows and cols, 

            imkeys = indexed_maptable.keys()

            for row in reader:

                newrow = []

                for key in imkeys:

                    ncol = indexed_maptable[key]

                    # take away the null-values if they exist

                    if row[ncol] not in null_values:

                        if key in ['LEFT_GAZE_X', 'RIGHT_GAZE_X']:

                            newrow.append(float(row[ncol]) / 1920.0)

                        elif key in ['LEFT_GAZE_Y', 'RIGHT_GAZE_Y']:

                            newrow.append(float(row[ncol]) / 1020.0)

                        else:

                            newrow.append(row[ncol])

                    else:

                        newrow.append(replace_null_values)

                newrows.append(newrow)




# scan through files in a directory

diritems = os.listdir(input_folder)



print ("Directory contains " + str(len(diritems)) + " files.")



for filenum, file in enumerate(diritems): #diritems

    #print ("Checking file " + str(filenum + 1) + '/' + str(len(diritems)))

    if file.endswith(ending):
        print ("Process file " + str(filenum + 1) + '/' + str(len(diritems)))
        file_process(file)
##    
##
##        print " Filename matches with the specified ending -> processing.."
##
##        #self.liststore_exp.append([file])
##
##        input_file = file
##
##
##
##        # input file reading
##
##        newrows = []
##
##        with open(os.path.join(input_folder, input_file), "rb") as inputfile:
##
##            reader = csv.reader(inputfile, delimiter = input_file_delimiter)
##
##
##
##            # grab header information, into a list
##
##            headers = reader.next()
##
##
##
##            # calculate list index numbers for map-keys
##
##            indexed_maptable = {}
##
##            for key in maptable:
##
##                indexed_maptable[key] = headers.index(key)
##
##
##
##            # loop file rows and cols, 
##
##            imkeys = indexed_maptable.keys()
##
##            for row in reader:
##
##                newrow = []
##
##                for key in imkeys:
##
##                    ncol = indexed_maptable[key]
##
##                    # take away the null-values if they exist
##
##                    if row[ncol] not in null_values:
##
##                        if key in ['LEFT_GAZE_X', 'RIGHT_GAZE_X']:
##
##                            newrow.append(float(row[ncol]) / 1920.0)
##
##                        elif key in ['LEFT_GAZE_Y', 'RIGHT_GAZE_Y']:
##
##                            newrow.append(float(row[ncol]) / 1020.0)
##
##                        else:
##
##                            newrow.append(row[ncol])
##
##                    else:
##
##                        newrow.append(replace_null_values)
##
##                newrows.append(newrow)



        # output file formation

        # resolve the output file name

        input_filename_parts = file.split(".") #input_file.split(".")

        output_file = input_filename_parts[0] + output_file_ending



        # open file

        with open(os.path.join(output_folder, output_file), "wb") as outputfile:

            writer = csv.writer(outputfile, delimiter='\\t')



            # form header row

            newheaders = []

            for key in imkeys:

                newheaders.append(maptable[key])



            # write header row

            writer.writerow(newheaders)



            # write datarows

            for newrow in newrows:

                writer.writerow(newrow)



            print (" File processed.")

#    else:

        #print (" Filename did not match the ending -> did nothing.")

