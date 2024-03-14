# This is the file that I (Pierce) am going to be writing up functions and things to be used for the experiment
# Can be altered or moved over to whatever file required, this is just where i'm 'drafting'.

# First function is a JSON file interpreter, as the log files output from the experiment are going to be given as
# .json files. This function will be applied to the live log file in order to ;

#       1. Seperate the files by JSON object, as the log file will have a JSON file per measurement and the
#          native JSON decoder is incompatible with a json file of multiple objects in the given format.

#       2. Identify the dark field frames, storing them separately.

#       3. Apply the json decoder to each json object and extract different variables, storing like variables
#          into arrays for easy access and analysis at the experiment.

# The function will take in the name of the logfile as a parameter.

# import the json library and plotting module
import json
import matplotlib.pyplot as plt
import datetime

def liveLogInterpreter(fileName):
    
    # Open the log file to be read in
    logFile = open(fileName,"r")

    # Initialise storage arrays
    darkFrames = [] # All of the json objects (as dicts) that are dark frames
    realFrames = [] # All of the json objects (as dicts) that are actual measurements

    # Read in the first line to initialise
    currentLine = logFile.readline()

    # Begin to read through the log file line by line
    while currentLine:
    
        # Create the JSON object as a dict
        currentJSON = json.loads(currentLine)

        # Identify any dark frames and add them to darkFrames list, otherwise add to realFrames list
        darkIndex = currentLine.find('dark')
        if darkIndex > 0:
            darkFrames.append(currentJSON)

        else:
            realFrames.append(currentJSON)

        # Once the current line has been assigned as a dark frame or not,
        # read in the next line to continue
        currentLine = logFile.readline()

    # just a check to see it's working, should print the timestamps of the first and last
    # 'real' (non-dark) frames
    print(" ")
    print("Reading in JSON objects test (should be initial and final timestamps followed by number of frames):")
    print(realFrames[0].get("TimeStamp"))
    print(realFrames[-1].get("TimeStamp"))
    print(len(realFrames))
    print(" ")

    # Close the log file
    logFile.close()

    # in order to be able to plot particular variables with ease; create lists/arrays of
    # desired variables to be plotted;
    v = "Ibs" # This is the key being plotted, change here only
    x = [] # this will be the time axis (in seconds) from the start of measuring
    y = [] # this will be the variable axis
    counter = 0

    # initialise the time axis based on the timestamp
    tstring = realFrames[0].get("TimeStamp")
    tlist = tstring.split(' ') # split the timestamp string into a date and time string
    dstring = tlist[0]
    tstring = tlist[-1]
    
    # split the date string into year, month and day
    dlist = dstring.split('-') 
    yearI = int(dlist[0])
    monthI = int(dlist[1])
    dayI = int(dlist[2])

    # split the time string into hours, minutes and seconds
    tlist = tstring.split(':')
    hoursI = int(tlist[0])
    minutesI = int(tlist[1])
    secondsI = tlist[2]
    secondsL = secondsI.split('.')
    secondsI = int(secondsL[0])
    msecondsI = int(secondsL[1])

    # create the initial time as a datetime object
    tI = datetime.datetime(yearI,monthI,dayI,hoursI,minutesI,secondsI,msecondsI)

    # retreive the desired variable values from the realFrames list
    while counter < len(realFrames):

        # add the relevant value according to the key
        y.append(realFrames[counter].get(v))
        
        # get the time for the x axis
        time = realFrames[counter].get("TimeStamp")
        tlist = time.split(' ') # split the timestamp string into a date and time string
        dstring = tlist[0]
        tstring = tlist[-1]
    
        # split the date string into year, month and day
        dlist = dstring.split('-') 
        year = int(dlist[0])
        month = int(dlist[1])
        day = int(dlist[2])

        # split the time string into hours, minutes and seconds
        tlist = tstring.split(':')
        hours = int(tlist[0])
        minutes = int(tlist[1])
        seconds = tlist[2]
        secondsL = seconds.split('.')
        seconds = int(secondsL[0])
        mseconds = int(secondsL[1])

        # create the current time datetime object
        tF = datetime.datetime(year,month,day,hours,minutes,seconds,mseconds)

        # need to find the time in seconds from the start of the measuring keeping in mind new days/months etc.
        t = tF-tI # creates t as a timedelta object which calculates the time passage

        xval = t.total_seconds()

        x.append(xval)
        counter = counter+1

    # format and display the plot
    plt.plot(x,y)
    plt.xlabel('Time (seconds)')
    plt.ylabel(v)
    plt.title("Plot of " + v + " in seconds from first measurement")
    plt.show()
    
# =========================================================================================

# Here is the script that is being used to test the code

liveLogInterpreter('livelogfile.json')
