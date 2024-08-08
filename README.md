A massive thank you to Tala Sohrabi (@Talaa202) for teaching me and helping me write this code and to the Balsam-Simpson Lab at the New York State Psychiatric Institute for letting me borrow their Med Associate operant boxes!

## Differential Reinforcement of High Rate (DRH)

### Task Details

In the Differential Reinforcement of Higher Rate (DRH) task, the mice are trained to make two lever presses within a specific time limit. We started with a time limit of 1 second and decreased this time by 0.2 seconds every three session until we reached 0.2 seconds as the time limit. Each session ends at 1 hour or 60 rewards

### Apparatus Information

The operant boxes were from Med Associates Inc. (Model 1820; Med Associates, St. Albans, VT) and MedScripts were used to run the program (Ward et al., 2015).

### Script Outputs

**DRH.py**

- Date: date of session
- Subject: subject number from the Med Associates data file
- Program: program name from the Med Associates data file
- Genotype: assigns a value to the subject based on a list defined by the user
- Sex: assigns a value to the subject based on a list defined by the user
- FirstLatency: the first lever press can be made within any time interval and is excluded in the rest of the latency measures
- AverageLatency: average latency between lever presses 
- SessionTime: total session time
- NumberOfRewards: number of rewards achieved
- Lever Press: total number of lever presses
- press <2s: total number of lever presses made under 2 seconds
- press <1s: total number of lever presses made under 1 seconds
- press <0.8s: total number of lever presses made under 0.8 seconds
- press <0.6s: total number of lever presses made under 0.6 seconds
- press <0.4s: total number of lever presses made under 0.4 seconds
- press <0.2s: total number of lever presses made under 0.2 seconds
- Accuracy 2s: the number of lever presses made under 2s divided by the total number of lever presses within the session
- Accuracy 1s: the number of lever presses made under 1s divided by the total number of lever presses within the session
- Accuracy 0.8s: the number of lever presses made under 0.8s divided by the total number of lever presses within the session
- Accuracy 0.6s: the number of lever presses made under 0.6s divided by the total number of lever presses within the session
- Accuracy 0.4s: the number of lever presses made under 0.4s divided by the total number of lever presses within the session
- Accuracy 0.2s: the number of lever presses made under 0.2s divided by the total number of lever presses within the session
- Reward Efficiency: presses per reward
- Rate of Lever Press per Second: rate of lever presses per second
- all latency: a list of all latencies in the program
- plot: a list of the timestamps of latencies in seconds

**BurstAnalysis.py**

- Date: date of session
- Subject: subject number from the Med Associates data file
- Genotype: assigns a value to the subject based on a list defined by the user
- Sex: assigns a value to the subject based on a list defined by the user
- FirstLatency: the first lever press can be made within any time interval and is excluded in the rest of the latency measures
- AverageLatency: average latency between lever presses 
- SessionTIme: total session time
- Program: program name from the Med Associates data file
- NumberOfRewards: number of rewards achieved
- no headpoke count: number of headpokes not made when a dipper was presented
- Lever Press: total number of lever presses
- Reward Rate: presses per reward
- lever press no reward: lever presses made within the designated time interval
- Rate (LP/SessTime): total lever presses divided by total session time
- all latency: a list of all latencies in the program
- plot: a list of the timestamps of latencies in seconds
- bursts: list of latencies under a certain time defined by the user
- number of bursts: number of bursts (defined as 2 or more presses under a time defined by a user)
- burst sums: total amount of time in each burst group
- average burst time: average of burst sums
- sum of all bursts: total bursting time
- average_burst_press_count: average presses in a burst

**BurstAnalysisAVG.py**

- calculates the average value across multiple session per subject
- calculates the averages for: the number of bursts, sum of all bursts, average burst time, average_burst_press_count

**Raster_All_GTandSex.py**
- creates a raster plot of all the lever presses made during a session
- creates raster plots based on date of the session and make sure to change the max_x_value based on your session time

