import tkinter as tk
from tkinter import ttk
import subprocess
import os
import threading

def run_algorithm():
    algorithm = algorithm_var.get()
    test_size = test_size_var.get()
    script_path = os.path.dirname(__file__)
    
    if algorithm == "Hill Climber":
        script_path += "/HillClimber.py"
    # elif algorithm == "Algorithm 2":
    #     script_path = "algorithm2.py"
    # elif algorithm == "Algorithm 3":
    #     script_path = "algorithm3.py"
    
    # Add test size as an argument if needed
    if test_size == "Petit(2-5 minutes)":
        script_command = ["python", script_path, "--small"]
    elif test_size == "Moyen(10-20 minutes)":
        script_command = ["python", script_path, "--medium"]
    elif test_size == "Grand(+20 minutes)":
        script_command = ["python", script_path, "--large"]
    
    progress_bar.config(mode="indeterminate")    
    progress_bar.start(10)
    
    subprocess.Popen(script_command)

# Create the main window
root = tk.Tk()
root.title("Selection de l'algorithme")

# Algorithm selection
algorithm_label = ttk.Label(root, text="choisir un algorithme:")
algorithm_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
algorithms = ["Hill Climber", "Genetique", "Réseau de neuronnes"]
algorithm_var = tk.StringVar()
algorithm_dropdown = ttk.Combobox(root, textvariable=algorithm_var, values=algorithms)
algorithm_dropdown.grid(row=0, column=1, padx=10, pady=5)

# Test size selection
test_size_label = ttk.Label(root, text="Choisissez la taille du test:")
test_size_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
test_sizes = ["Petit(2-5 minutes)", "Moyen(10-20 minutes)", "Grand(+20 minutes)"]
test_size_var = tk.StringVar()
test_size_dropdown = ttk.Combobox(root, textvariable=test_size_var, values=test_sizes)
test_size_dropdown.grid(row=1, column=1, padx=10, pady=5)

# Run button
run_button = ttk.Button(root, text="Lancer l'algorithme", command=run_algorithm)
run_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Example of updating progress (replace this with your loop progress)

def update_progress(progress):
    progress_bar['value'] = progress
    root.update_idletasks()  # Mettre à jour l'interface utilisateur


root.mainloop()
