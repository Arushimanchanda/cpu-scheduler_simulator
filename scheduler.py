# scheduler.py
# Contains all 4 CPU scheduling algorithms

def fcfs(processes):
    # First Come First Serve - processes run in order of arrival
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    results = []
    timeline = []
    for p in processes:
        if time < p['arrival']:
            time = p['arrival']  # CPU idle until process arrives
        start = time
        end = time + p['burst']
        waiting = start - p['arrival']
        turnaround = end - p['arrival']
        timeline.append({'name': p['name'], 'start': start, 'end': end})
        results.append({'name': p['name'], 'waiting': waiting, 'turnaround': turnaround})
        time = end
    return timeline, results


def sjf(processes):
    # Shortest Job First - picks the process with smallest burst time
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    results = []
    timeline = []
    remaining = processes.copy()
    while remaining:
        available = [p for p in remaining if p['arrival'] <= time]
        if not available:
            time += 1
            continue
        p = min(available, key=lambda x: x['burst'])  # pick shortest job
        start = time
        end = time + p['burst']
        waiting = start - p['arrival']
        turnaround = end - p['arrival']
        timeline.append({'name': p['name'], 'start': start, 'end': end})
        results.append({'name': p['name'], 'waiting': waiting, 'turnaround': turnaround})
        time = end
        remaining.remove(p)
    return timeline, results


def round_robin(processes, quantum):
    # Round Robin - each process gets a fixed time slot (quantum)
    time = 0
    results = []
    timeline = []
    remaining = [dict(p, rem=p['burst']) for p in sorted(processes, key=lambda x: x['arrival'])]
    queue = []
    i = 0

    # Add processes that have arrived at time 0
    while i < len(remaining) and remaining[i]['arrival'] <= time:
        queue.append(remaining[i])
        i += 1

    if not queue and remaining:
        time = remaining[0]['arrival']
        queue.append(remaining[0])
        i += 1

    while queue:
        p = queue.pop(0)
        run = min(p['rem'], quantum)  # run for quantum or remaining time
        timeline.append({'name': p['name'], 'start': time, 'end': time + run})
        time += run
        p['rem'] -= run

        # Add newly arrived processes to queue
        while i < len(remaining) and remaining[i]['arrival'] <= time:
            queue.append(remaining[i])
            i += 1

        if p['rem'] > 0:
            queue.append(p)  # put back in queue if not finished
        else:
            waiting = time - p['arrival'] - p['burst']
            turnaround = time - p['arrival']
            results.append({'name': p['name'], 'waiting': max(0, waiting), 'turnaround': turnaround})
    return timeline, results


def priority_scheduling(processes):
    # Priority Scheduling - picks process with highest priority (lowest number)
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    results = []
    timeline = []
    remaining = processes.copy()
    while remaining:
        available = [p for p in remaining if p['arrival'] <= time]
        if not available:
            time += 1
            continue
        p = min(available, key=lambda x: x['priority'])  # pick highest priority
        start = time
        end = time + p['burst']
        waiting = start - p['arrival']
        turnaround = end - p['arrival']
        timeline.append({'name': p['name'], 'start': start, 'end': end})
        results.append({'name': p['name'], 'waiting': waiting, 'turnaround': turnaround})
        time = end
        remaining.remove(p)
    return timeline, results
