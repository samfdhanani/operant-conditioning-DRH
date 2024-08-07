import os
import pandas as pd
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt


filelist = []
pathslist = []

datapath = os.path.normpath("/Users/samdhanani/Desktop/MuhleLab/Operant_Data_Folders/CohF_DRH")
IDList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

for subdir, dirs, files in sorted(os.walk(datapath)):
    filelist.append(files)
    pathslist.append(subdir)

filelist.pop(0)
pathslist.pop(0)

def query(pathslist, querydate):  
    folderdates = []
    for x in pathslist:
        folderdates.append(os.path.basename(os.path.normpath(x))) #

    querypaths = []

    for i in range(0, len(folderdates)):
        if folderdates[i] == querydate:
            querypaths.append(pathslist[i]) 

    return(querypaths)

def data_pull(datapath, ID):
    
    for subdir, dirs, files in sorted(os.walk(datapath)):
        for file in files:
            temp = file.split('.')  
            sub = temp[1] 
            if ID == sub:
                x = os.path.join(subdir, file) 
                df = pd.read_csv(x, sep="[:\s]{1,}", skiprows=15, header=None, engine="python") 
                progline = pd.read_csv(x, skiprows=12, nrows = 1, header = None, engine="python")
                progline = progline.values.tolist()
                progline = progline[0][0].split(" ")
                if "_" in progline[1]:
                    progline = progline[1].split("_", 1) 
                progline = progline[1]
                df = df.drop(0,axis=1)
                df = df.stack()
                df = df.to_frame()
                df = df.to_numpy()

    try:
        return(df, progline) 
    except UnboundLocalError:
        df = []
        progline = None
        return(df, progline)   

def data_construct(data):

    events = np.remainder(data,10000) 
    times = data - events 

    StartTrial = times[np.where(events == 111)] 
    StartSess = times[np.where(events == 113)]
    EndSess = times[np.where(events == 114)]

    Sess_time = np.divide(np.subtract(EndSess, StartSess), 10000000)
    Sess_time = Sess_time.tolist() 
    Sess_time = Sess_time[0] 

    LLever = times[np.where(events == 27)]
    RLever = times[np.where(events == 28)]

    DipOn = times[np.where(events == 25)]
    DipOff = times[np.where(events == 26)]
    DipOff = DipOff.tolist()
    if DipOff:
        DipOff = DipOff[0]
    else:
        DipOff = 0  # 

    HeadPoke = times[np.where(events == 1011)]


    Lever_extensions = np.concatenate((LLever, RLever), axis = 0) 
    Lever_extensions = np.unique(Lever_extensions)  

    LLever_off = times[np.where(events == 29)]
    RLever_off = times[np.where(events == 30)]

    Reward = times[np.where(events == 25)]


    LPress = times[np.where(events == 1015)]
    RPress = times[np.where(events == 1016)]

    LeverPress = np.concatenate((LPress, RPress),axis=0)
    LeverPress = sorted(LeverPress)
    LeverPress = np.unique(LeverPress)

    headpoke_count = 0
    within_dipper = False
    headpoke_occurred = False

    for event in events:
        if event == 25:  # DipOn
            within_dipper = True
        elif event == 26:  # DipOff
            within_dipper = False
            headpoke_occurred = False

        if within_dipper and event == 1011 and not headpoke_occurred:  # HeadPoke
            headpoke_count += 1
            headpoke_occurred = True

    no_headpoke_count = len(DipOn) - headpoke_count

    ############################# Latency Calculations:
    
    
    rate_LP = np.divide(len(LeverPress), Sess_time)
    rate_LP = rate_LP.tolist()
    x = 0

    # looking when press starts
    # find duration, subtraction--go through array with inex
    # presses [i]-presses [i+1]
    #compare presses I timestamp
    # if timestamp is in the dipper, you can include the 5 sec in calculation
    #p1 and 2 in for loop

    #u = np.unique(events)
    LA = []


    for i in range (0, len(LeverPress)):
        p1 = np.divide(LeverPress[i], 10000000)
        try:
            p2 = np.divide(LeverPress[i+1], 10000000)
        except IndexError:
            break
        else:
            latency = p2 - p1
        LA.append(latency)
    
        def average_LA(LA_list):
            total = 0
            for i in LA_list:
                total += i
            return total/len(LA_list)
                
    plot = [latency + sum(LA[:i+1]) for i in range(len(LA))]

    LA_array = np.array(LA)
    LA_array = str(LA_array)[1:-1]
    LA_array = LA_array.replace('\n', ' ')
    LA_array = ' '.join(LA_array.split())

    plot_array = np.array(plot)

    lever_press_times = []
    for i in range(len(LeverPress)):
        timestamp = LeverPress[i] / 10000000  # Convert timestamp to seconds
        lever_press_times.append(timestamp)

    lever_press_times.sort()

    lever_press_within_2s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 2:
            lever_press_within_2s += 1

    lever_press_within_1s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 1:
            lever_press_within_1s += 1

    lever_press_within_08s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.8:
            lever_press_within_08s += 1

    lever_press_within_06s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.6:
            lever_press_within_06s += 1

    lever_press_within_04s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.4:
            lever_press_within_04s += 1
    
    lever_press_within_02s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.2:
            lever_press_within_02s += 1

    lever_press_within_01s = 0
    for i in range(1, len(lever_press_times)):
        time_diff = lever_press_times[i] - lever_press_times[i - 1]
        if time_diff <= 0.1:
            lever_press_within_01s += 1

    Accuracy_2s = np.divide(lever_press_within_2s, len(LeverPress))
    Accuracy_2s = Accuracy_2s.tolist()
    x = 0        
   
    Accuracy_1s = np.divide(lever_press_within_1s, len(LeverPress))
    Accuracy_1s = Accuracy_1s.tolist()
    x = 0

    Accuracy_08s = np.divide(lever_press_within_08s, len(LeverPress))
    Accuracy_08s = Accuracy_08s.tolist()
    x = 0

    Accuracy_06s = np.divide(lever_press_within_06s, len(LeverPress))
    Accuracy_06s = Accuracy_06s.tolist()
    x = 0

    Accuracy_04s = np.divide(lever_press_within_04s, len(LeverPress))
    Accuracy_04s = Accuracy_04s.tolist()
    x = 0

    Accuracy_02s = np.divide(lever_press_within_02s, len(LeverPress))
    Accuracy_02s = Accuracy_02s.tolist()
    x = 0

    Accuracy_01s = np.divide(lever_press_within_01s, len(LeverPress))
    Accuracy_01s = Accuracy_01s.tolist()
    x = 0

    Reward_Efficiency = np.divide(len(LeverPress), len(Reward))
    Reward_Efficiency = Reward_Efficiency.tolist()
    x = 0

   
    

    average = average_LA(LA)
    print("The average of LA is:", average)
    print('Mouse - ', Full_ID)
    print("Rewards - ", len(Reward))
    print("Headpoke - ", no_headpoke_count)
    print("Lever presses within 1 second:", lever_press_within_1s)


    return(latency, average, Sess_time, len(Reward), no_headpoke_count,len(LeverPress), lever_press_within_2s, lever_press_within_1s, lever_press_within_08s, lever_press_within_06s, lever_press_within_04s, lever_press_within_02s, lever_press_within_01s, Accuracy_2s, Accuracy_1s, Accuracy_08s, Accuracy_06s, Accuracy_04s, Accuracy_02s, Accuracy_01s, Reward_Efficiency, rate_LP, LA, plot)


def genotype(sub):
    # 1 = WT and 2 = Het
    g_type = None
    if sub == 4 or sub == 5 or sub == 7 or sub == 8 or sub == 9 or sub == 11 or sub == 12 or sub == 13 or sub == 17 or sub == 19 or sub == 21 or sub == 22 or sub == 25 or sub == 28 or sub == 29 or sub == 31:
        g_type = 1
    elif sub == 1 or sub == 2 or sub == 3 or sub == 6 or sub == 10 or sub == 14 or sub == 15 or sub == 16 or sub == 18 or sub == 20 or sub == 23 or sub == 24 or sub == 26 or sub == 27 or sub == 30 or sub == 32:
        g_type = 2

    return g_type

def sex(sub):
    s_type = None
    if sub == 1 or sub == 2 or sub == 3 or sub == 4 or sub == 5 or sub == 6 or sub == 7 or sub == 8 or sub == 9 or sub == 10 or sub == 11 or sub == 12 or sub == 13 or sub == 14 or sub == 15 or sub == 16:
        s_type = 'M'
    elif sub == 17 or sub == 18 or sub == 19 or sub == 20 or sub == 21 or sub == 22 or sub == 23 or sub == 24 or sub == 25 or sub == 26 or sub == 27 or sub == 28 or sub == 29 or sub == 30 or sub == 31 or sub == 32:
        s_type = 'F'

    return s_type

# pathslist = query(pathslist, '7-2
# 0-22')
df_ind = 0 #index varibale, add one everytime we run through a subj
sus_attn_df = pd.DataFrame(columns = ['Date', 'Subject', 'Genotype', 'Sex', 'FirstLatency', 'AverageLatency', 'SessionTime', 'Program', 'NumberOfRewards', ' no headpoke count','Lever Press', 'press <2s','press <1s', 'press <0.8s', 'press <0.6s', 'press <0.4s','press <0.2s','press <0.1s','Accuracy 2s','Accuracy 1s', 'Accuracy 0.8s','Accuracy 0.6s', 'Accuracy 0.4s', 'Accuracy 0.2s', 'Accuracy 0.1s','Reward_Efficiency', 'Rate of Lever Press per Second', 'all latency','plot'])
def new_func(session_type, ID, progline):
    sess_type = session_type(progline, ID)
    return sess_type
def new_func(g_type, ID):
    g_type = genotype(ID)
    return g_type
def new_func(s_type, ID):
    s_type = sex(ID)
    return s_type

for dirs in pathslist:

    date = os.path.basename(os.path.normpath(dirs))
    # sus_attn_df = pd.DataFrame(columns = ['Date', 'Subject', 'PercentChoiceTrials', 'PercentChoiceCorrect', 'AverageLatency', 'TimedOutTrials', 'SessionTime', 'SessionType'])
    csv_name = "\\" + date + ".csv"
    # print(date)
    
    for ID in IDList: #run througb ID list one by one, add subj to this to prevent confusion
        Full_ID = "Subject " + str(ID)
        data, progline = data_pull(dirs, Full_ID) #calling datapull and putting it through dirs
        if len(data) == 0:
            continue
        latency, num_average, Sess_time, num_Rewards, no_headpoke_count, num_LeverPress, lever_press_within_2s, lever_press_within_1s, lever_press_within_08s, lever_press_within_06s, lever_press_within_04s, lever_press_within_02s, lever_press_within_01s, Accuracy_2s, Accuracy_1s, Accuracy_08s, Accuracy_06s, Accuracy_04s, Accuracy_02s, Accuracy_01s, Reward_Efficiency, rate_LP, LA, plot = data_construct(data) #data construct, putting that all here
        g_type = genotype(ID)
        s_type = sex(ID)


        sus_attn_df.loc[df_ind] = [date, Full_ID, g_type, s_type, latency, num_average, Sess_time, progline, num_Rewards, no_headpoke_count , num_LeverPress, lever_press_within_2s, lever_press_within_1s, lever_press_within_08s, lever_press_within_06s, lever_press_within_04s, lever_press_within_02s, lever_press_within_01s, Accuracy_2s, Accuracy_1s, Accuracy_08s, Accuracy_06s, Accuracy_04s, Accuracy_02s, Accuracy_01s, Reward_Efficiency, rate_LP, LA, plot ] #assigning variables one by one
        df_ind += 1 #location zero is populated with variables above, add one each time for it to be sequential

    # sus_attn_df.to_csv(dirs + csv_name)

sus_attn_df.to_csv(datapath + "030524.csv")