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
    temp = realFrames[0].get("TimeStamp")
    print(temp)
    print(realFrames[5339].get("TimeStamp"))

    # Close the log file
    logFile.close()

    # in order to be able to plot particular variables with ease; create lists/arrays of
    # desired variables to be plotted;
    v = "Ibs"
    x = []
    y = []

    # retreive the desired variable values from the realFrames list
    for i in realFrames:
        y.append(realFrames[i].get(v))
        x.append(i)

    # format and display the plot
    plt.plot(x,y)
    plt.xlabel()
    plt.ylabel(v)
    plt.show()
    
# =========================================================================================

# Here is the script that is being used to test the code

liveLogInterpreter('livelogfile.json')