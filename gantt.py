import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

COLORS = ['#7F77DD', '#1D9E75', '#D85A30', '#378ADD', '#BA7517', '#D4537E', '#639922', '#888780']

def draw_gantt(timeline, results, algo_name):
    if not timeline:
        print("No timeline data!")
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    fig.suptitle(f'CPU Scheduling — {algo_name}', fontsize=14, fontweight='bold')

    process_names = list(dict.fromkeys([t['name'] for t in timeline]))
    color_map = {name: COLORS[i % len(COLORS)] for i, name in enumerate(process_names)}

    max_time = max(seg['end'] for seg in timeline)

    ax1.set_title('Gantt Chart', fontsize=11)
    ax1.set_ylim(0, 2)
    ax1.set_xlim(0, max_time + 1)
    ax1.set_yticks([])
    ax1.set_xlabel('Time')

    for seg in timeline:
        color = color_map[seg['name']]
        width = seg['end'] - seg['start']
        ax1.broken_barh([(seg['start'], width)], (0.7, 0.6),
                        facecolors=color, edgecolors='white', linewidth=1.5)
        ax1.text((seg['start'] + seg['end']) / 2, 1.0,
                 seg['name'], ha='center', va='center',
                 fontsize=9, fontweight='bold', color='white')

    ticks = sorted(set([seg['start'] for seg in timeline] + [seg['end'] for seg in timeline]))
    ax1.set_xticks(ticks)

    legend_patches = [mpatches.Patch(color=color_map[n], label=n) for n in process_names]
    ax1.legend(handles=legend_patches, loc='upper right', fontsize=8)

    names = [r['name'] for r in results]
    waiting_times = [r['waiting'] for r in results]
    turnaround_times = [r['turnaround'] for r in results]
    x = list(range(len(names)))

    ax2.set_title('Waiting Time vs Turnaround Time', fontsize=11)
    bars1 = ax2.bar([i - 0.2 for i in x], waiting_times, width=0.4,
                    label='Waiting Time', color='#7F77DD')
    bars2 = ax2.bar([i + 0.2 for i in x], turnaround_times, width=0.4,
                    label='Turnaround Time', color='#1D9E75')
    ax2.set_xticks(x)
    ax2.set_xticklabels(names)
    ax2.set_ylabel('Time units')
    ax2.legend(fontsize=9)

    for bar in bars1:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 str(int(bar.get_height())), ha='center', fontsize=8)
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 str(int(bar.get_height())), ha='center', fontsize=8)

    avg_wt = sum(waiting_times) / len(waiting_times)
    avg_tat = sum(turnaround_times) / len(turnaround_times)
    fig.text(0.5, 0.01,
             f'Avg Waiting Time: {avg_wt:.2f}   |   Avg Turnaround Time: {avg_tat:.2f}',
             ha='center', fontsize=10, color='#534AB7')

    plt.tight_layout()
    plt.show()