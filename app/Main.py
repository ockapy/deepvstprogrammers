import tkinter as tk
import subprocess
import os
from tkinter import ttk
from functools import partial

row = 3

def destroy_process(self,text,progress_bar,process):
    text.destroy()
    progress_bar.destroy()
    process.kill()
    self.destroy()

def start_new_process(command,algo,size):
    global row
    
    process = subprocess.Popen(command)
    
    text = ttk.Label(root,text=size+" "+algo)
    text.grid(row=row,column=0)
    
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode="indeterminate")
    progress_bar.grid(row=row, column=1)
    progress_bar.start(10)

    button_stop = ttk.Button(root,text="Stopper")
    button_stop.config(command=partial(destroy_process,button_stop,text,progress_bar,process))
    button_stop.grid(row=row,column=2, padx=0, pady=10)
    
    row+=1
    


def run_algorithm():
    
    script_command = ""
    test_size = ""
    
    algorithm = algorithm_var.get()
    test_size = test_size_var.get()
    script_path = os.path.dirname(__file__)
    
    if algorithm == "Hill Climber":
        script_path += "/HillClimber.py"
    elif algorithm == "Genetique":
        script_path += "/Genetic.py"
    elif algorithm == "Réseau de neuronnes":
        script_path += "/MLP.py"
    
    
    # Add test size as an argument if needed
    if test_size == "Petit":
        script_command = ["python", script_path, "--small"]
    elif test_size == "Moyen":
        script_command = ["python", script_path, "--medium"]
    elif test_size == "Grand":
        script_command = ["python", script_path, "--large"]
    

    
    if (script_command != "" and test_size != ""):
        start_new_process(script_command,algorithm,test_size)
    else:
        print("Paramètres manquants")

# Create the main window
root = tk.Tk()
root.title("Selection de l'algorithme")

# Algorithm selection
algorithm_label = ttk.Label(root, text="choisir un algorithme:")
algorithm_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
algorithms = ["Hill Climber", "Genetique", "Réseau de neuronnes"]
algorithm_var = tk.StringVar()
algorithm_dropdown = ttk.Combobox(root, textvariable=algorithm_var, values=algorithms,state="readonly")
algorithm_dropdown.grid(row=0, column=1, padx=10, pady=5)

# Test size selection
test_size_label = ttk.Label(root, text="Choisissez la taille du test:")
test_size_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
test_sizes = ["Petit", "Moyen", "Grand"]
test_size_var = tk.StringVar()
test_size_dropdown = ttk.Combobox(root, textvariable=test_size_var, values=test_sizes,state="readonly")
test_size_dropdown.grid(row=1, column=1, padx=10, pady=5)

# Run button
run_button = ttk.Button(root, text="Lancer l'algorithme", command=run_algorithm)
run_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()
