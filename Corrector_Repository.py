# This file contains different functions required for dark and whitefield correction
# as well as the handling/isolation/removal of dark/white frames from the datasets
# for CAFS. It is done without the use of pandas and mainly native python functions.

# Made to apply to the datasets retrieved from the SAXS/WAXS Beamline. These
# datasets include a logfile of the frames taken throughout the scan and a seperate
# but corresponding collection of JSON objects in a file.

# The code and functions in this file are designed to be very modular for simple
# application and flexibility in their application.

# This file was created by Pierce Bowman, 27/04/2024

# Import the necessary modules:
import json
import matplotlib.pyplot as plt
import datetime as dt

def df_and_wf_identifier(log_file_path):
    # This function takes in the logfile and returns the indexes of the dark and 
    # white frames respectively, so long as they name the file naming conventions,
    # that is, dark frames contain 'dark' and white frames contain 'thru'.

    # REMEMBER TO MAKE SURE THAT THESE TERMS ARE NOT ACCIDENTALLY PRESENT,
    # OTHERWISE IT WILL MIS-IDENTIFY

    # Initialise the file object and the index arrays
    log_file = open(log_file_path,"r")
    df_idx = [] # dark frames indexes
    wf_idx = [] # white frames indexes

    # Read in the first line to initialise for the while loop;
    line = log_file.readline()

    # Set up the counter for the index
    c = 1

    # Begin reading through and storing the indexes of any dark and white frames
    while line:

        # Convert the JSON object to a dict type for python to utilise
        frame = json.loads(line)

        # Add any dark or white indexes 
        if 'dark' in frame["chanh_filename"]:
            df_idx.append(c)
        elif 'thru' in frame["chanh_filename"]:
            wf_idx.append(c)

        # Iterate the counter and read in the next line
        c = c + 1
        line = log_file.readline()

    # Remember to close the log file
    log_file.close()

    return df_idx, wf_idx

def frame_seperator(log_file_path, df_idx, wf_idx):
    # This function is used to read the log file and return three seperate lists
    # of the JSON objects as dicts. One list of the of the dark frame dicts, one
    # of the white frames and one list of the frame dicts minus the others.

    # Initialise the file object and the frame arrays
    log_file = open(log_file_path,"r")
    df = [] # dark frames
    wf = [] # white frames
    rf = [] # remaining frames

    # Read in the first line to initialise for the while loop;
    line = log_file.readline()

    # Set up the counter for the loop
    c = 1

    # Begin reading through and storing any dark frames
    while line:

        # Convert the JSON object to a dict type for python to utilise
        frame = json.loads(line)

        # Add any dark or white frames 
        if c in df_idx:
            df.append(frame)
        elif c in wf_idx:
            wf.append(frame)
        else:
            rf.append(frame)
        
        # Iterate the counter and read in the next line
        c = c + 1
        line = log_file.readline()

    # Remember to close the log file
    log_file.close()

    return rf, df, wf

def log_variable_plotter(input_frames, x_axis, *variable_names):
    # This function will take lists of the input frames, whether it be the
    # sample/real frames, dark frames or white frames or which ever and will
    # plot the variables input into the function. It is formatted to the frame
    # lists output by the frame_separator function.

    # the x-axis will be a string decided by the user from either time,
    # energy or frame number:

    if x_axis.casefold() == "time".casefold():
        # This is the time x-axis option, outputs in seconds

        # Initialise x-axis
        x = []

        # Initialise the time axis based on the timestamp
        tstring = input_frames[0].get("TimeStamp")
        tlist = tstring.split(' ') # split the timestamp string into a date and time string
        dstring = tlist[0]
        tstring = tlist[-1]
        
        # Split the date string into year, month and day
        dlist = dstring.split('-') 
        yearI = int(dlist[0])
        monthI = int(dlist[1])
        dayI = int(dlist[2])

        # Split the time string into hours, minutes and seconds
        tlist = tstring.split(':')
        hoursI = int(tlist[0])
        minutesI = int(tlist[1])
        secondsI = tlist[2]
        secondsL = secondsI.split('.')
        secondsI = int(secondsL[0])
        msecondsI = int(secondsL[1])

        # Create the initial time as a datetime object
        tI = dt.datetime(yearI,monthI,dayI,hoursI,minutesI,secondsI,msecondsI)

        # Create a counter for the loop
        counter = 0

        # Retreive the x-axis values from the input_frames list
        while counter < len(input_frames):

            # Get the Timestamp for the current frame and split it for the datetime object
            time = input_frames[counter].get("TimeStamp")
            tlist = time.split(' ') # split the timestamp string into a date and time string
            dstring = tlist[0]
            tstring = tlist[-1]
        
            # Split the date string into year, month and day
            dlist = dstring.split('-') 
            year = int(dlist[0])
            month = int(dlist[1])
            day = int(dlist[2])

            # Split the time string into hours, minutes and seconds
            tlist = tstring.split(':')
            hours = int(tlist[0])
            minutes = int(tlist[1])
            seconds = tlist[2]
            secondsL = seconds.split('.')
            seconds = int(secondsL[0])
            mseconds = int(secondsL[1])

            # Create the current time datetime object, measure time difference and add to list
            tF = dt.datetime(year,month,day,hours,minutes,seconds,mseconds)
            t = tF-tI # Creates t as a timedelta object which calculates the time passage
            x.append(t) # Add to the list

            # Iterate the counter
            counter = counter + 1

        # Retrieve the variable values for each desired variable then plot the graph
        
        # Initialise the subplot (sharing the time axis, see https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html for more)
        plt.subplots(len(variable_names), sharex = True)
        
        for var in variable_names:

            # Initialise y
            y = []

            # Reset the counter for the variables loop
            counter = 0

            while counter < len(input_frames):

                # Add the relevant variable to the y value list
                y.append(input_frames[counter].get(var))

                # Iterate counter
                counter = counter + 1

            # Now create the subplots using the x values and the current variable, var;
            plt.subplot(x,y)
            plt.ylabel(var)
            plt.title("Plot of " + var + " in seconds from first measurement")
        
        # Display the plots
        plt.xlabel('Time (seconds)')
        plt.show()

    elif x_axis.casefold() == "energy".casefold():
        # This is the energy x-axis option

        # Initialise x-axis and subplot
        x = []
        plt.subplots(len(variable_names), sharex = True)

        # Set the counter for the loop
        counter = 0
        
        while counter < len(input_frames):

            # Add the relevant variable to the y value list
            x.append(input_frames[counter].get("Si111_monochromator_energy"))

            # Iterate counter
            counter = counter + 1
        
        for var in variable_names:

            # Initialise y
            y = []

            # Reset the counter for the loop
            counter = 0

            while counter < len(input_frames):

                # Add the relevant variable to the y value list
                y.append(input_frames[counter].get(var))

                # Iterate counter
                counter = counter + 1

            # Now create the subplots using the x values and the current variable, var;
            plt.subplot(x,y)
            plt.ylabel(var)
            plt.title("Plot of " + var + " in seconds from first measurement")
        
        # Display the plots
        plt.xlabel('Time (seconds)')
        plt.show()

    elif x_axis.casefold() == "frames".casefold():
        # This is the number of frames x-axis option

        # Initialise subplot
        
        plt.subplots(len(variable_names), sharex = True)

        # Set the counter for the loop
        counter = 0
        
        for var in variable_names:

            # Initialise x and y
            x = []
            y = []

            # Reset the counter for the loop
            counter = 0

            while counter < len(input_frames):

                # Add the relevant variable to the y value list
                x.append(counter)
                y.append(input_frames[counter].get(var))

                # Iterate counter
                counter = counter + 1

            # Now create the subplots using the x values and the current variable, var;
            plt.subplot(x,y)
            plt.ylabel(var)
            plt.title("Plot of " + var + " in seconds from first measurement")
        
        # Display the plots
        plt.xlabel('Time (seconds)')
        plt.show()

    else:
        print("Invalid x-axis type input, try either 'time', 'energy' or 'frames")

def dark_corrector(raw_frames, df):
    # This function will apply the dark field correction to the frames passed in
    # and output the dark field corrected frames

    
    return corrected_frames

def white_corrector(raw_frames, wf):
    # This function will apply the white field correction to the frames passed in
    # and output the white field corrected frames


    return corrected_frames

def sawtooth_corrector():
    # This function is designed to deal with the sawtooth pattern that is incuded
    # in the absorption due to the limitation on the undulator resolution. once the
    # step-size reached below 5 eV this sawtooth pattern would be prominent. So
    # this function applies a correction utilising the whitefield frames measured
    # immediately after the sample frames and before the energy change. this should
    # also effecticely deal with any quantum efficiency issue between the ANDOR and
    # ion chamber.



    
    return corrected_frames