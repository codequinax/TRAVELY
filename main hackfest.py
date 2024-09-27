import customtkinter as ctk
import subprocess
import sys
import os

# Function to run a Python script without showing a command prompt
def run_script(script_path):
    if not os.path.isfile(script_path):
        print(f"Script {script_path} does not exist.")
        return

    try:
        subprocess.Popen(
            [sys.executable, script_path],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
    except Exception as e:
        print(f"Failed to run script {script_path}: {e}")

# Function to close the application
def close_app():
    root.destroy()

# Create the main window
ctk.set_appearance_mode("light")  # Set the appearance mode
ctk.set_default_color_theme("blue")  # Set the default color theme

root = ctk.CTk()
root.title("TRAVELy")
root.geometry("700x600")

# Create a frame for the close button at the top-right corner
close_frame = ctk.CTkFrame(root, width=50, height=30)
close_frame.pack(side="top", anchor="ne", padx=10, pady=10)

# Create the close button
close_button = ctk.CTkButton(
    close_frame,
    text="CLOSE",
    width=50,
    height=25,
    fg_color="red",
    hover_color="red2",
    command=close_app,
    font=("Arial", 12)
)
close_button.pack()

label = ctk.CTkLabel(root,fg_color="light blue",text_color="yellow",height=100,width=200,font=("Heritage",80), text="TRAVELy",corner_radius=12)
label.pack(pady=40)

# Button 1: Run script1.py
button1 = ctk.CTkButton(
    root,
    text="Explore",
    text_color="white",
    width=200,
    height=50,
    command=lambda: run_script("newfile.py"),  # Replace with your script
    fg_color="DarkOliveGreen3",
    hover_color="#45a049",
font=("Arial", 30))
button1.pack(pady=20)
# Button 2: Run script2.py
button2 = ctk.CTkButton(
    root,
    text="Budget",
    text_color="white",
    width=200,
    height=50,
    command=lambda: run_script("budget.py"),  # Replace with your script         
    fg_color="khaki3",
    hover_color="khaki4",
font=("Arial",30))
button2.pack(pady=20)

# Start the GUI event loop
root.mainloop()
