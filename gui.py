# gui.py
# Main GUI window for the CPU Scheduler Simulator

import tkinter as tk
from tkinter import ttk, messagebox
from scheduler import fcfs, sjf, round_robin, priority_scheduling
from gantt import draw_gantt

# List to store all added processes
processes = []

def add_process():
    # Get values from input fields
    name = entry_name.get().strip()
    arrival = entry_arrival.get().strip()
    burst = entry_burst.get().strip()
    priority = entry_priority.get().strip()

    # Validate all fields are filled
    if not name or not arrival or not burst or not priority:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    # Validate numeric inputs
    try:
        arrival = int(arrival)
        burst = int(burst)
        priority = int(priority)
    except ValueError:
        messagebox.showerror("Error", "Numbers only!")
        return

    # Add process to list and display in table
    processes.append({"name": name, "arrival": arrival, "burst": burst, "priority": priority})
    tree.insert("", tk.END, values=(name, arrival, burst, priority))

    # Clear fields and prepare for next process
    entry_name.delete(0, tk.END)
    entry_arrival.delete(0, tk.END)
    entry_burst.delete(0, tk.END)
    entry_priority.delete(0, tk.END)
    entry_name.insert(0, f"P{len(processes)+1}")

def clear_processes():
    # Clear all processes from list and table
    processes.clear()
    for row in tree.get_children():
        tree.delete(row)

def show_quantum():
    # Show time quantum input only for Round Robin
    if algo_var.get() == "Round Robin":
        lbl_quantum.pack(side="left", padx=5)
        entry_quantum.pack(side="left", padx=5)
    else:
        lbl_quantum.pack_forget()
        entry_quantum.pack_forget()

def run_simulation():
    # Check processes exist
    if not processes:
        messagebox.showerror("Error", "Add at least one process!")
        return

    algo = algo_var.get()
    procs_copy = [dict(p) for p in processes]

    # Run selected algorithm and display results
    if algo == "FCFS":
        timeline, results = fcfs(procs_copy)
        draw_gantt(timeline, results, "First Come First Serve (FCFS)")
    elif algo == "SJF":
        timeline, results = sjf(procs_copy)
        draw_gantt(timeline, results, "Shortest Job First (SJF)")
    elif algo == "Round Robin":
        try:
            quantum = int(entry_quantum.get())
            if quantum <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Valid time quantum needed!")
            return
        timeline, results = round_robin(procs_copy, quantum)
        draw_gantt(timeline, results, f"Round Robin (Quantum={quantum})")
    elif algo == "Priority":
        timeline, results = priority_scheduling(procs_copy)
        draw_gantt(timeline, results, "Priority Scheduling")

# Create main window
root = tk.Tk()
root.title("Intelligent CPU Scheduler Simulator")
root.geometry("700x550")
root.configure(bg="#f5f5f5")

# Title label
tk.Label(root, text="Intelligent CPU Scheduler Simulator",
         font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#3C3489").pack(pady=15)

# Input frame for adding processes
input_frame = tk.LabelFrame(root, text="Add Process", font=("Arial", 10, "bold"),
                             bg="#f5f5f5", fg="#3C3489", padx=10, pady=10)
input_frame.pack(padx=20, fill="x")

# Column headers
tk.Label(input_frame, text="Name", bg="#f5f5f5").grid(row=0, column=0, padx=5)
tk.Label(input_frame, text="Arrival Time", bg="#f5f5f5").grid(row=0, column=1, padx=5)
tk.Label(input_frame, text="Burst Time", bg="#f5f5f5").grid(row=0, column=2, padx=5)
tk.Label(input_frame, text="Priority", bg="#f5f5f5").grid(row=0, column=3, padx=5)

# Input fields
entry_name = tk.Entry(input_frame, width=8)
entry_name.insert(0, "P1")
entry_name.grid(row=1, column=0, padx=5)

entry_arrival = tk.Entry(input_frame, width=8)
entry_arrival.grid(row=1, column=1, padx=5)

entry_burst = tk.Entry(input_frame, width=8)
entry_burst.grid(row=1, column=2, padx=5)

entry_priority = tk.Entry(input_frame, width=8)
entry_priority.grid(row=1, column=3, padx=5)

# Add and Clear buttons
btn_frame = tk.Frame(input_frame, bg="#f5f5f5")
btn_frame.grid(row=1, column=4, padx=10)

tk.Button(btn_frame, text="Add", bg="#7F77DD", fg="white",
          font=("Arial", 9, "bold"), command=add_process).pack(side="left", padx=3)
tk.Button(btn_frame, text="Clear All", bg="#D85A30", fg="white",
          font=("Arial", 9, "bold"), command=clear_processes).pack(side="left", padx=3)

# Process queue table
table_frame = tk.LabelFrame(root, text="Process Queue", font=("Arial", 10, "bold"),
                              bg="#f5f5f5", fg="#3C3489", padx=10, pady=10)
table_frame.pack(padx=20, pady=10, fill="both", expand=True)

cols = ("Name", "Arrival Time", "Burst Time", "Priority")
tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=6)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=140, anchor="center")
tree.pack(fill="both", expand=True)

# Algorithm selection
algo_frame = tk.LabelFrame(root, text="Algorithm", font=("Arial", 10, "bold"),
                            bg="#f5f5f5", fg="#3C3489", padx=10, pady=10)
algo_frame.pack(padx=20, fill="x")

algo_var = tk.StringVar(value="FCFS")
for algo in ["FCFS", "SJF", "Round Robin", "Priority"]:
    tk.Radiobutton(algo_frame, text=algo, variable=algo_var, value=algo,
                   bg="#f5f5f5", font=("Arial", 10),
                   command=show_quantum).pack(side="left", padx=15)

# Time quantum input (only for Round Robin)
lbl_quantum = tk.Label(algo_frame, text="Time Quantum:", bg="#f5f5f5")
entry_quantum = tk.Entry(algo_frame, width=5)
entry_quantum.insert(0, "2")

# Run button
tk.Button(root, text="Run Simulation", bg="#1D9E75", fg="white",
          font=("Arial", 12, "bold"), command=run_simulation).pack(pady=15)

root.mainloop()
