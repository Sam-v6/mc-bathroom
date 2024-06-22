# Module imports
import numpy as np
import random
import datetime
import matplotlib.pyplot as plt

# Create pee and poo schedules
def create_schedule(MEN_COUNT):
    """
    Generates schedule of when people pee and poo

    :param MEN_COUNT: Number of men to generate schedules for.
    :return: Sorted list of "pee" events with each index containing time of pee and remaining_duration of pee.
    :return: Sorted list of "poo" events with each index containing time of pee and remaining_duration of pee.
    :return: List of each person's schedule (containing their individual pee and poo lists if applicable).
    """ 

    # Input
    possible_times = [9,10,11,12,13,14,15,16] # 9-10, 10-11, 11-12, 12-1, 1-2, 2-3, 3-4, 4-5
    poo_event_weights = [0.6,0.4]
    poo_time_weights = [1,2,2,2,1,1,1,1]

    # Init
    pee_schedule = []
    poo_schedule = []
    person_schedule = []

    # Create schedule for each male
    for i in range(0,MEN_COUNT):

        # Determine count of pee and poo events
        pee_count = random.randint(1, 3)
        poo_count = random.choices([0, 1], poo_event_weights)[0]

        # Determine time of pee events
        pee_list = []
        for j in range(0,pee_count):
            pee_hour = random.randint(9,16)
            pee_minute = random.randint(0,59)
            pee_sec = random.randint(0,59)
            pee_time = datetime.datetime(2024,1,1,pee_hour,pee_minute,pee_sec)
            pee_remaining_duration = random.randint(30,60) # seconds
            pee_list.append(["pee",pee_time,pee_remaining_duration])
            pee_schedule.append([pee_time,pee_remaining_duration])
        
        # Determine time of poo event
        poo_list = []
        if poo_count == 1:
            poo_hour = random.choices(possible_times,poo_time_weights)[0]
            poo_minute = random.randint(0,59)
            poo_sec = random.randint(0,59)
            poo_time = datetime.datetime(2024,1,1,poo_hour,poo_minute,poo_sec)
            poo_remaining_duration = random.randint(3,30)  # minutes
            poo_list.append(["poo",poo_time,poo_remaining_duration])
            poo_schedule.append([poo_time,poo_remaining_duration])
        else:
            poo_list = ["no-poo","no","no"]
        
        # Add times to schedule
        person_schedule.append([i,pee_list,poo_list])

        # Sort pee and poo lists
        pee_schedule = sorted(pee_schedule, key=lambda x: x[0])
        poo_schedule = sorted(poo_schedule, key=lambda x: x[0])

    # Return
    return pee_schedule,poo_schedule,person_schedule

# Create time list
def create_time_list():
    """Returns list of times from 9am to 5pm at second interval."""

    # Create time_list
    start_time = datetime.datetime(2024,1,1,9,0,0)
    end_time = datetime.datetime(2024,1,1,17,0,0)
    current_time = start_time
    time_list = []
    while current_time <= end_time:
        time_list.append(current_time)
        current_time = current_time + datetime.timedelta(seconds=1)

    # Return
    return time_list



#----------Main--------------

# Flow
# Generate a schedule of people's pee and poo times
# Sort that list 

# Constants
SIMULATIONS = 1
MEN_COUNT = 5
URINAL_COUNT = 7
STALL_COUNT = 6
PRINT_SCHEDULE = True

# Exec simulations
for sim in range(0,SIMULATIONS): 

    # Generate schedules
    pee_schedule,poo_schedule,person_schedule = create_schedule(MEN_COUNT)

    # Optional prints
    if PRINT_SCHEDULE:
        print("Pee Schedule")
        for item in pee_schedule:
            print(item)

        print("Poo Schedule")
        for poo in poo_schedule:
            print(poo)

    # Generate time list
    time_list = create_time_list()

    # Set up urinals
    urinal_status = {}
    for i in range(1,URINAL_COUNT+1):
        urinal_status[i] = {'status': 0, 'remaining_duration': 0, "sum": 0}

    # Fill ems
    urinal_que = []
    urinal_history = []
    for i in range(0,len(time_list)):

        # Local variables
        current_time = time_list[i]

        # Update urinal status
        for urinal in urinal_status:

            # If the urinal is occupied, subtract one second
            if urinal_status[urinal]["remaining_duration"] != 0:                                      
                urinal_status[urinal]["remaining_duration"] = urinal_status[urinal]["remaining_duration"] - 1  

            # Check if we need to empty the urinal
            if urinal_status[urinal]["remaining_duration"] == 0:
                urinal_status[urinal]["status"] = 0

        # Update the que
        for pee_event in pee_schedule:

            # Local variables
            pee_time = pee_event[0]
            pee_remaining_duration = pee_event[1]

            # Someone wants to pee, add them to the que with how long they want to pee
            if time_list[i] == pee_time:
                urinal_que.append(pee_remaining_duration)

        # Assign the urinals
        if urinal_que:
           # print(urinal_que)
            for person_waiting_index in range(0,len(urinal_que)):
                for urinal in urinal_status:
                    # If the urinal is empty then fill it, remove that person from the que, and break
                    if urinal_status[urinal]["status"] == 0:                                 # if the current urinal status is empty
                        urinal_status[urinal]["status"] = 1                                  # fill it 
                        print(person_waiting_index, len(urinal_que))
                        urinal_status[urinal]["remaining_duration"] = urinal_que[person_waiting_index] # assign the remaining_duration of how long they want to pee
                        urinal_que.pop(person_waiting_index)                                 # remove them from the que
                        print("occupied")

        # Update the urinal history for tracking/debugging purposes
        second_history = []
        for urinal in urinal_status:
            second_history.append(urinal_status[urinal]["remaining_duration"])
        urinal_history.append(second_history)

        