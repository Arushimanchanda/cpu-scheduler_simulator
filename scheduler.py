def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    results = []
    timeline = []

    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        start = time
        end = time + p['burst']
        waiting = start - p['arrival']
        turnaround = end - p['arrival']
        timeline.append({'name': p['name'], 'start': start, 'end': end})
        results.append({'name': p['name'], 'waiting': waiting, 'turnaround': turnaround})
        time = end

    return timeline, results


def sjf(processes):
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
        p = min(available, key=lambda x: x['burst'])
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
    time = 0
    results = []
    timeline = []
    remaining = [dict(p, rem=p['burst']) for p in sorted(processes, key=lambda x: x['arrival'])]
    queue = []
    i = 0

    while i < len(remaining) and remaining[i]['arrival'] <= time:
        queue.append(remaining[i])
        i += 1

    if not queue and remaining:
        time = remaining[0]['arrival']
        queue.append(remaining[0])
        i += 1

    while queue:
        p = queue.pop(0)
        run = min(p['rem'], quantum)
        timeline.append({'name': p['name'], 'start': time, 'end': time + run})
        time += run
        p['rem'] -= run

        while i < len(remaining) and remaining[i]['arrival'] <= time:
            queue.append(remaining[i])
            i += 1

        if p['rem'] > 0:
            queue.append(p)
        else:
            waiting = time - p['arrival'] - p['burst']
            turnaround = time - p['arrival']
            results.append({
                'name': p['name'],
                'waiting': max(0, waiting),
                'turnaround': turnaround
            })

    return timeline, results


def priority_scheduling(processes):
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
        p = min(available, key=lambda x: x['priority'])
        start = time
        end = time + p['burst']
        waiting = start - p['arrival']
        turnaround = end - p['arrival']
        timeline.append({'name': p['name'], 'start': start, 'end': end})
        results.append({'name': p['name'], 'waiting': waiting, 'turnaround': turnaround})
        time = end
        remaining.remove(p)

    return timeline, results