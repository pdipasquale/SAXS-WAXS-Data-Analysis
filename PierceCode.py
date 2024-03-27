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
import datetime # used to determine timing in experiment
import os # this is required for the reconstruction function

def liveLogInterpreter(fileName):
    
    # Open the log file to be read in
    logFile = open(fileName,"r")

    # Initialise storage arrays
    darkFrames = [] # All of the json objects (as dicts) that are dark frames
    realFrames = [] # All of the json objects (as dicts) that are actual measurements
    darkIndexes = [] # This stores the indexes of the dark frames, needed for the reconstruction process.
    c = 1 # This is the line number

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
            darkIndexes.append(c)

        else:
            realFrames.append(currentJSON)

        # Once the current line has been assigned as a dark frame or not,
        # read in the next line to continue
        currentLine = logFile.readline()
        c = c+1

    # just a check to see it's working, should print the timestamps of the first and last
    # 'real' (non-dark) frames
    print(" ")
    print("Reading in JSON objects test (should be initial and final timestamps followed by number of frames):")
    print(realFrames[0].get("TimeStamp"))
    print(realFrames[-1].get("TimeStamp"))
    print(len(realFrames))
    print("Indexes of dark frames:")
    print(darkIndexes)
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

# ========================================================================================================================

# Here is the script that is being used to test this code

liveLogInterpreter('livelogfile.json')
    
##################################################################################################################
    # TO DO LIST:
    # Need to add parts that align and reconstruct
    # add a part that takes tif images of the diffraction patterns and reconstructs them as needed
    # Paul will be adding diffraction patterns and code into the repository to do this
    # going to adjust the alignment method for the live script because it will take too long as is to
    # run real time analysis; going to take averages over 20 pixels per fringe at each energy, then align these
    # averages across the diffraction pattern. (see Paul explanation)
##################################################################################################################

# Begin the reconstruction code

# Need to begin by reading in the diffraction image data. Due to limitations with the detector, a spooling system was implemented
# to be able to temporarily store the diffraction image data. There are 3 scans per spool file (a .dat file. eg;
# Ni_Sample1_8232.../spool/SpoolDirectory0/SpoolData0.dat). As each scan is taken at a different energy the total number of
# measured energy points is number of spool_files*3. Additionally the dimensions of the detector are 2048 pixels x 2048 pixels.

# However, when the dimensions of the detector are changed there can be more or less scans fit into a spool file. As these
# parameters change the code will need to as well.

def liveReconstruction(ReconDir, pixdim, scansPerSpool):

    # First step is to collect all of the spool files data. how many there are as well as retrieving the diffraciton patterns and the frame number.
    # The current plan is to create a 2D data structure with one dimension as the frame number and the other dimension is the diffration pattern.
    # Once that is constructed, a third dimension can be added that will be the energy. Then the average/mean over the frame dimension to reduce down
    # to a 2D data structure of Energy in one dimension and the diffraction pattern in the other (see the reshape() function that Paul mentioned)

    # Collect all frames, taking into consideration files that are subject to the spooling structure, the last .dat file may be empty or only 1 or 
    # 2 scans, so need to adjust for the last .dat file to be able to take a different number of scans. Use the log file as reference as every
    # frame measured has a log. also need to omit dark frames from the construction. See daniels code for reading diffraction patterns and stuff from
    # the .dat files.

    # determine the number of spools
    numSpools = 0
    for path, currentDirectory, files in os.walk(ReconDir):
    for file in files:
        if file.startswith("SpoolDirectory"):
            numSpools+=1

    # refine the paths to the spool directories into a list
    spoolDir = os.listdir(ReconDir)
    spoolList = [word for word in spoolDir if word.startswith('SpoolDirectory')]

    # initialise structures to be taken
    diffPatterns = []

    # now go through and retrieve the diffraction patterns from the spool files, keeping in mind that we want to cut the run time down for the live
    # analysis. So instead of the entire diffraction pattern, we are taking a line across the pattern and creating an array per diffraction pattern
    # which contains the average intensities in a small area of each fringe along one direction. then alignment only needs to be undertaken in one 
    # axis, dramatically cutting down run time.

    

# This section runs the liveReconstruction() function

ReconDir = '' # this should be the absolute path upto the 'spool' directory (i.e not the 'SpoolDirectory') that corresponds to the log file e.g;
              # 'G:\SAXS-WAXS-Data-Analysis\Cu_foil_fdbkOff_8950_9450_5_1s_3f_160922_2100_run3\spool' when using the
              # Cu_foil_fdbkOff_8950_9450_5_1s_3f_160922_2100_run3 log file
scansPerSpool = 3 # this is the number of frames per spool .dat
pixdim = 2048 # this is the pixel dimensions of the detector
liveReconstruction(ReconDir)
