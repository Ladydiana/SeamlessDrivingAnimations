import subprocess


def run_auto_generate_animation(blender_executable, script_file, log_file, n_runs):
    for i in range(n_runs):
        # Construct the command to run Blender in background mode
        command = [
            blender_executable,
            "--background",        # Run in background mode without UI
            "--python", script_file,  # Specify the Python script to run
        ]
        
        # Open the log file for appending
        with open(log_file, "a") as log:
            log.write(f"Run {i+1}/{n_runs}:\n")
            
            # Execute the command and redirect output to the log file
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)
            
            log.write("\n" + "-"*40 + "\n")  # Separate log entries for each run

# Parameters
blender_executable = r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"
script_file = r"auto_generate_animation.py"  
log_file = r"log.txt"  # The log file where the output will be saved
n_runs = 20  # Number of times to run the script

# Run the script multiple times
run_auto_generate_animation(blender_executable, script_file, log_file, n_runs)