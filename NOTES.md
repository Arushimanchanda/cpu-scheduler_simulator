# Project Notes

## Algorithm Explanations

### 1. First Come First Serve (FCFS)
- Simplest scheduling algorithm
- Processes execute in order of arrival
- Non-preemptive
- Problem: Long processes can block shorter ones (convoy effect)

### 2. Shortest Job First (SJF)
- Picks the process with smallest burst time
- Non-preemptive
- Gives minimum average waiting time
- Problem: Long processes may never get CPU (starvation)

### 3. Round Robin (RR)
- Each process gets a fixed time slot called quantum
- Preemptive - process is interrupted after quantum expires
- Fair to all processes
- Performance depends on quantum size

### 4. Priority Scheduling
- Each process has a priority number
- Lower number = higher priority
- Non-preemptive
- Problem: Low priority processes may starve

## Performance Metrics
- Waiting Time = Start Time - Arrival Time
- Turnaround Time = Completion Time - Arrival Time
- Average Waiting Time = Sum of all waiting times / Number of processes
- Average Turnaround Time = Sum of all turnaround times / Number of processes

## Team
- Group 1
- Course: CSE316 - Operating Systems
- University: Lovely Professional University
