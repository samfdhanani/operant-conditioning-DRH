import os
import pandas as pd
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

# declaring empty list
filelist = []
pathslist = []

datapath = os.path.normpath("/Users/samdhanani/Dropbox/Muhle Lab/Mouse_files/Cohort F (operant)/DRH/Raw_Operant_Data/CohF_DRH") #add filepath here
IDList = [1, 2, 3, 4] 
# list of subject IDs as labelled in MED-PC

# walks through the filepath, filelist contains a list of all files and pathslist contains datapaths for subfolders
for subdir, dirs, files in sorted(os.walk(datapath)):
    filelist.append(files)
    pathslist.append(subdir)

filelist.pop(0) # get rid of elements in index zero
pathslist.pop(0) # get rid of elements in index zero

# this function is used to isolate and analyze a specific folder/date from the data; run at the botton of this script
def query(pathslist, querydate): 
    folderdates = []
    for x in pathslist:
        folderdates.append(os.path.basename(os.path.normpath(x))) # extracts the date from the filepath

    querypaths = []

    for i in range(0, len(folderdates)):
        if folderdates[i] == querydate: # 
            querypaths.append(pathslist[i]) # pull specific date

    return(querypaths)

# this function extracts data from each specific data file by ID 
def data_pull(datapath, ID):
    df = []
    progline = None
    
    for subdir, dirs, files in sorted(os.walk(datapath)): # 
        for file in files:
            temp = file.split('.') # split string by '.', in this case the string is split into the sesion date (0) and Subject ID (1)
            sub = temp[1] # Subject ID
            if ID == sub:
                x = os.path.join(subdir, file) # specific file
                df = pd.read_csv(x, sep="[:\s]{1,}", skiprows=15, header=None, engine="python") # skips 15 rows to where the data actually starts
                progline = pd.read_csv(x, skiprows=12, nrows = 1, header = None, engine="python") # reads only 1 row, the program line in the 12th row
                progline = progline.values.tolist()
                progline = progline[0][0].split(" ") 
                if "_" in progline[1]:
                    progline = progline[1].split("_", 1) # splits up program name if an underscore is present
                progline = progline[1]
                df = df.drop(0,axis=1) # cleaning up the data
                df = df.stack() 
                df = df.to_frame() 
                df = df.to_numpy() # dataframe should be an array of each line containing the data, removed the row labels from the data file 
    return(df, progline)   

# this function uses event and timestamp data to output various metrics describing behavior
def data_construct(data): 

    events = np.remainder(data,10000) # use division to isolate event code
    times = data - events # subtract event code from full code

    StartTrial = times[np.where(events == 111)] # all event codes come from the MED-PC Medscript
    StartSess = times[np.where(events == 113)]
    EndSess = times[np.where(events == 114)]

    Sess_time = np.divide(np.subtract(EndSess, StartSess), 10000000)
    Sess_time = Sess_time.tolist() # turn into list
    Sess_time = Sess_time[0] # points to specific info we need

    LLever = times[np.where(events == 27)] # command for when the lever is on
    RLever = times[np.where(events == 28)]

    DipOn = times[np.where(events == 25)] # event codes for the dipper turning on and off
    DipOff = times[np.where(events == 26)]
    DipOff = DipOff.tolist()
    DipOff = DipOff[0]

    Lever_extensions = np.concatenate((LLever, RLever), axis = 0) # total time a lever was extended
    Lever_extensions = np.unique(Lever_extensions) # makes sure each time is only recorded once

    LLever_off = times[np.where(events == 29)]
    RLever_off = times[np.where(events == 30)]

    Reward = times[np.where(events == 25)]

    LPress = times[np.where(events == 1015)]
    RPress = times[np.where(events == 1016)]

    LeverPress = np.concatenate((LPress, RPress),axis=0)
    LeverPress = sorted(LeverPress) # combine lever presses into one list and keep them sorted
    LeverPress = np.unique(LeverPress) # makes sure each lever press is only recorded once

# number of missed headpoke code
    headpoke_count = 0 # counts the number of headpokes
    within_dipper = False # tracks if dipper is active
    headpoke_occurred = False # tracks if headpoke happens

    for event in events:
        if event == 25:  # DipOn
            within_dipper = True 
        elif event == 26:  # DipOff
            within_dipper = False
            headpoke_occurred = False

        if within_dipper and event == 1011 and not headpoke_occurred:
            headpoke_count += 1
            headpoke_occurred = True

    no_headpoke_count = len(DipOn) - headpoke_count
    
# calculating the rate of lever presses per second
    rate = np.divide(len(LeverPress), Sess_time)
    rate = rate.tolist()
    x = 0

# calculating the latency array by finding the time in between lever presses until the last one when LeverPress[i+1] doesn't exist
    LA = [] # stores individual latencies

    for i in range (0, len(LeverPress)):
        p1 = np.divide(LeverPress[i], 10000000)
        try:
            p2 = np.divide(LeverPress[i+1], 10000000)
        except IndexError:
            break
        else:
            latency = p2 - p1 # next lever press - current lever press
        LA.append(latency) # add latency to LA
    
        def average_LA(LA_list):
            total = 0 # stores sum of all latencies
            for i in LA_list:
                total += i # adds latencies values to total
            return total/len(LA_list) # returns the avg by dividing the total by the number of latencies recorded

# calculates an array for a raster plot, all the latency timepoints in the session              
    plot = [latency + sum(LA[:i+1]) for i in range(len(LA))]

# formats data as strings removing brackets and punctuation for easier downstream data processing
    LA_array = np.array(LA)
    LA_array = str(LA_array)[1:-1] # removes brackets surrounding the string
    LA_array = LA_array.replace('\n', ' ') # format array as a single line
    LA_array = ' '.join(LA_array.split()) # ensures all values are separated by a single space

    plot_array = str(plot)[1:-1] # removes brackets surrounding the string
    plot_array = plot_array.replace('\n', ' ') # format array as a single line
    plot_array = plot_array.replace(',',' ') # removes commas from array
    plot_array = ' '.join(plot_array.split()) # ensures all values are separated by a single space

# calculating the accuracy of lever presses within specific times
    lever_press_times = [] # stores the lever press timestamps in seconds
    for i in range(len(LeverPress)): 
        timestamp = LeverPress[i] / 10000000  
        lever_press_times.append(timestamp)

    lever_press_times.sort()

# checks for accuracy of presses made within 2 seconds 
    lever_press_within_2s = 0 # keeps track of number of lever presses
    for i in range(1, len(lever_press_times)): # loops through lever presses, starts at the second press
        time_diff = lever_press_times[i] - lever_press_times[i - 1] # calculates time difference using the current and previous lever press
        if time_diff <= 2: # checks if time difference is less than or equal to 2 seconds
            lever_press_within_2s += 1 # if above is true add 1 to lever press counter 
    Accuracy_2s = np.divide(lever_press_within_2s, len(LeverPress))
    Accuracy_2s = Accuracy_2s.tolist()
    x = 0
# checks for accuracy of presses made within 1 second
    lever_press_within_1s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 1:
            lever_press_within_1s += 1
    Accuracy_1s = np.divide(lever_press_within_1s, len(LeverPress))
    Accuracy_1s = Accuracy_1s.tolist()
    x = 0
# checks for accuracy of presses made within 0.8 seconds
    lever_press_within_08s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.8:
            lever_press_within_08s += 1
    Accuracy_08s = np.divide(lever_press_within_08s, len(LeverPress))
    Accuracy_08s = Accuracy_08s.tolist()
    x = 0
# checks for accuracy of presses made within 0.6 seconds
    lever_press_within_06s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.6:
            lever_press_within_06s += 1
    Accuracy_06s = np.divide(lever_press_within_06s, len(LeverPress))
    Accuracy_06s = Accuracy_06s.tolist()
    x = 0
# checks for accuracy of presses made within 0.4 seconds
    lever_press_within_04s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.4:
            lever_press_within_04s += 1
    Accuracy_04s = np.divide(lever_press_within_04s, len(LeverPress))
    Accuracy_04s = Accuracy_04s.tolist()
    x = 0
# checks for accuracy of presses made within 0.2 seconds
    lever_press_within_02s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.2:
            lever_press_within_02s += 1
    Accuracy_02s = np.divide(lever_press_within_02s, len(LeverPress))
    Accuracy_02s = Accuracy_02s.tolist()
    x = 0
# checks for accuracy of presses made within 0.1 seconds
    lever_press_within_01s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.1:
            lever_press_within_01s += 1
    Accuracy_01s = np.divide(lever_press_within_01s, len(LeverPress))
    Accuracy_01s = Accuracy_01s.tolist()
    x = 0

# calculates the number of presses made per reward
    Reward_Efficiency = np.divide(len(LeverPress), len(Reward))
    Reward_Efficiency = Reward_Efficiency.tolist()
    x = 0

    average = average_LA(LA)
    print("The average of LA is:", average)
    print('Mouse - ', Full_ID)
    print("Rewards - ", len(Reward))
    print("Headpoke - ", no_headpoke_count)
    print("Lever presses within 1 second:", lever_press_within_1s)

    return(latency, average, Sess_time, len(Reward), no_headpoke_count,len(LeverPress), lever_press_within_2s, lever_press_within_1s, lever_press_within_08s, lever_press_within_06s, lever_press_within_04s, lever_press_within_02s, lever_press_within_01s, Accuracy_2s, Accuracy_1s, Accuracy_08s, Accuracy_06s, Accuracy_04s, Accuracy_02s, Accuracy_01s, Reward_Efficiency, rate, LA_array, plot_array)

# assigns a label for genotype to the subject
def genotype(sub):
    # 1 = WT and 2 = Het
    g_type = None
    if sub == 1 or sub == 2:
        g_type = 'WT'
    elif sub == 3 or sub == 4:
        g_type = 'Het'

    return g_type

# assigns a label for sex to the subject
def sex(sub):
    s_type = None
    if sub == 1 or sub == 3:
        s_type = 'M'
    elif sub == 2 or sub == 4:
        s_type = 'F'

    return s_type

# uncomment the line below to analyze one specific day in the data, date must match folder name
# pathslist = query(pathslist, '6-14-22')

df_ind = 0 # index variable, add one everytime we run through a subject

# comment the line below when running the script for one day only 
DRH_df = pd.DataFrame(columns = ['Date', 'Subject', 'Genotype', 'Sex', 'First Latency', 'Average Latency', 'Session Time', 'Program', 'Number Of Rewards', 'Missed Headpokes','Lever Press', 'Presses <2s','Presses <1s', 'Presses <0.8s', 'Presses <0.6s', 'Presses <0.4s','Presses <0.2s','Presses <0.1s','Accuracy 2s','Accuracy 1s', 'Accuracy 0.8s','Accuracy 0.6s', 'Accuracy 0.4s', 'Accuracy 0.2s', 'Accuracy 0.1s','Reward_Efficiency', 'Rate of Lever Press per Second', 'All Latencies','Raster Plot Values'])

def new_func(session_type, ID, progline):
    sess_type = session_type(progline, ID)
    return sess_type
def get_genotype(ID): # defines a function using ID and stores the genotype labels in g_type 
    g_type = genotype(ID)
    return g_type
def get_sex(ID): # defines a function using ID and stores the sex labels in s_type
    s_type = sex(ID)
    return s_type

for dirs in pathslist:

    date = os.path.basename(os.path.normpath(dirs))
    # uncomment the line below to analyze one specific day in the data
    # DRH_df = pd.DataFrame(columns = ['Date', 'Subject', 'Genotype', 'Sex', 'First Latency', 'Average Latency', 'Session Time', 'Program', 'Number Of Rewards', 'Missed Headpokes','Lever Press', 'Presses <2s','Presses <1s', 'Presses <0.8s', 'Presses <0.6s', 'Presses <0.4s','Presses <0.2s','Presses <0.1s','Accuracy 2s','Accuracy 1s', 'Accuracy 0.8s','Accuracy 0.6s', 'Accuracy 0.4s', 'Accuracy 0.2s', 'Accuracy 0.1s','Reward_Efficiency', 'Rate of Lever Press per Second', 'All Latencies','Raster Plot Values'])
    
    for ID in IDList: # run through ID list one by one, add 'Subject' to this to prevent confusion
        Full_ID = "Subject " + str(ID)
        data, progline = data_pull(dirs, Full_ID) # calling datapull and putting it through dirs
        if len(data) == 0:
            continue
        latency, num_average, Sess_time, num_Rewards, no_headpoke_count, num_LeverPress, lever_press_within_2s, lever_press_within_1s, lever_press_within_08s, lever_press_within_06s, lever_press_within_04s, lever_press_within_02s, lever_press_within_01s, Accuracy_2s, Accuracy_1s, Accuracy_08s, Accuracy_06s, Accuracy_04s, Accuracy_02s, Accuracy_01s, Reward_Efficiency, rate_LP, LA_array, plot_array = data_construct(data) #data construct, putting that all here
        g_type = genotype(ID)
        s_type = sex(ID)
        # comment the line below to analyze one specific day in the data
        DRH_df.loc[df_ind] = [date, Full_ID, progline, g_type, s_type, latency, num_average, Sess_time, num_Rewards, no_headpoke_count, num_LeverPress, lever_press_within_2s, lever_press_within_1s, lever_press_within_08s, lever_press_within_06s, lever_press_within_04s, lever_press_within_02s, lever_press_within_01s, Accuracy_2s, Accuracy_1s, Accuracy_08s, Accuracy_06s, Accuracy_04s, Accuracy_02s, Accuracy_01s, Reward_Efficiency, rate_LP, LA_array, plot_array] #assigning variables one by one
        df_ind += 1 # location zero is populated with variables above, add one each time for it to be sequential

    # uncomment the line below to analyze one specific day in the data
    # DRH_df.to_csv(dirs + csv_name)

# comment the line below to analyze one specific day in the data
DRH_df.to_csv(datapath + "_DATE.csv")
