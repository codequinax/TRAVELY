import google.generativeai as genai
import customtkinter as ctk
import subprocess
import sys
import os
# Configure Google Generative AI
genai.configure(api_key="AIzaSyAhqhtFuk11c7uJSRgvEEHElOfrmzsr_tw")  # Replace with your actual API key
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])
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
def csv_to_list(csv_string):
    """Convert a CSV string to a list of lists."""
    rows = csv_string.strip().split('\n')
    result = [row.split(',') for row in rows]
    return result

def open_new_window():
    """Fetch tourist destinations based on user input."""
    city = my_entry.get()
    if not city.strip():
        ctk.CTkMessageBox.show_error("Input Error", "Please enter a valid city name.")
        return

    response =chat_session.send_message(f"Plain text without clarification or additional information, give me a csv like list of major(the top 10 or 12) tourist destinations of {city}. String for name of the place and float and integers for rating and budget in INR")
  

    # Process and display the response
    destinations = csv_to_list(response.text)

    # Check if we received valid data
    if not destinations or len(destinations) < 2:
        ctk.CTkMessageBox.show_error("Error", "No valid destinations found. Please try again.")
        return

    output_text = ""
    for destination in destinations[1:]:  # Start from 1 to skip header
        if len(destination) < 3:
            continue  # Skip any invalid entries
        name, rating, price = destination[0], destination[1], destination[2]  # Unpacking
        output_text += f"{name} - Rating: {rating}, Price: {price} INR\n"

    # Update output label with results
    output_label.configure(text=output_text.strip() if output_text else "No valid destinations found.")


# Create the main application window
ctk.set_appearance_mode("light")  # Modes: "system" (default), "light", "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"
root = ctk.CTk()
root.title("TRAVELy")
def close_app():
    root.destroy()
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
return_frame = ctk.CTkFrame(root,fg_color="transparent", width=50, height=30)
return_frame.pack(side="top", anchor="ne", padx=10, pady=12)
button1 = ctk.CTkButton(
    return_frame,
    text="RETURN",
    text_color="white",
    width=50,
    height=25,
    command=lambda: run_script("main hackfest.py"),  # Replace with your script
    fg_color="DarkOliveGreen3",
    hover_color="#45a049",
font=("Arial", 12))
button1.pack(pady=20)

# Create a title label
title_label = ctk.CTkLabel(root, text="Tourist Destination Finder",fg_color="light steel blue",text_color="steel blue",font=("Helvetica", 80, "bold"),corner_radius=15)
title_label.pack(pady=(20, 10))

# Create an entry widget for user input
my_entry = ctk.CTkEntry(root, placeholder_text="Enter city name here", height=40, width=400)
my_entry.pack(pady=10)

# Create a submit button
submit_button = ctk.CTkButton(root,font=("Ariel",30),fg_color="cyan3",hover_color="cyan4", text="Find Destinations", command=open_new_window)
submit_button.pack(pady=10)

# Create an output label to display results
output_label = ctk.CTkLabel(root, text="", font=("Helvetica", 16), wraplength=400)
output_label.pack(pady=(10, 20))

# Start the main event loop
root.mainloop()
