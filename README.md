A massive thank you to Tala Sohrabi (@Talaa202) for teaching me and helping me write this code and to the Balsam-Simpson Lab at the New York State Psychiatric Institute for letting me borrow their Med Associate operant boxes!

## Differential Reinforcement of High Rate (DRH)
### Task Details
In the Differential Reinforcement of Higher Rate (DRH) task, the mice are trained to make two lever presses within a specific time limit starting at 1s and decreasing by 0.2s every three sessions. Each session ends at 1 hour or 60 rewards
### Apparatus Information
The operant boxes were from Med Associates Inc. (Model 1820; Med Associates, St. Albans, VT) and MedScripts were used to run the program (Ward et al., 2015).

### Script Outputs

**DRL.py**

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
- Rate: rate of lever presses per second
- Reward Efficiency: presses per reward
- Burst: lever press latencies less than or equal to 1 second
- binned latencies: binned latencies from 0 to 1 second with a width of 0.1 seconds
- all latency: a list of all latencies in the program

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

