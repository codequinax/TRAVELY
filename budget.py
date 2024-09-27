import os
import google.generativeai as genai
import tkinter as tk
import subprocess
import sys
import os

import customtkinter as ctk
from tkinter import messagebox, scrolledtext
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
    rows = csv_string.strip().split('\n')
    result = [row.split(',') for row in rows]
    return result

def maximize_rating_with_names(places, budget):
    n = len(places)

    # DP array to store max rating for each budget
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # To store the selected places' names
    selected_places = [[[] for _ in range(budget + 1)] for _ in range(n + 1)]

    # Dynamic programming to fill dp table
    for i in range(1, n + 1):
        name, rating, price = places[i - 1][0], float(places[i - 1][1]), int(places[i - 1][2])
        for b in range(budget + 1):
            if price <= b:
                # Option 1: Do not take this place
                dp[i][b] = dp[i - 1][b]
                selected_places[i][b] = selected_places[i - 1][b][:]

                # Option 2: Take this place (if it improves the rating score)
                if dp[i - 1][b - price] + rating > dp[i][b]:
                    dp[i][b] = dp[i - 1][b - price] + rating
                    selected_places[i][b] = selected_places[i - 1][b - price][:]
                    selected_places[i][b].append(name)
            else:
                # If we can't afford this place, just carry forward the previous values
                dp[i][b] = dp[i - 1][b]
                selected_places[i][b] = selected_places[i - 1][b][:]

    # Maximum rating score is dp[n][budget]
    max_rating = dp[n][budget]
    places_to_visit = selected_places[n][budget]

    return places_to_visit

def get_places():
    city = city_entry.get()
    budget = budget_entry.get()

    if not city or not budget.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid city and budget.")
        return

    budget = int(budget)
    genai.configure(api_key="AIzaSyAhqhtFuk11c7uJSRgvEEHElOfrmzsr_tw")
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
    response = chat_session.send_message(f"Plain text without clarification or additional information, give me a csv like list of major (the top 10 or 12) tourist destinations of {city}. String for name of the place and float and integers for rating and budget in INR")
    locations = csv_to_list(response.text)
    places = maximize_rating_with_names(locations[1:], budget)
    
    result_text.delete(1.0, tk.END)  # Clear previous results
    result_text.insert(tk.END, "\n".join(places))

# Create the main window
window = ctk.CTk()
window.title("TRAVELy")
ctk.set_appearance_mode("light")  # Set the appearance mode
ctk.set_default_color_theme("blue")

# Create and place labels and entry fields
ctk.CTkLabel(window,font=("Ariel",30), text="Enter the city you want to visit:").grid(row=0, column=0, padx=10, pady=10)
city_entry = ctk.CTkEntry(window,width=400,height=30)
city_entry.grid(row=0, column=1, padx=10, pady=10)
def close_app():
    window.destroy()
# Create a frame for the close button at the top-right corner
close_frame = ctk.CTkFrame(window, width=50, height=30)
close_frame.grid(row=0, column=10, padx=10, pady=10)

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
return_frame = ctk.CTkFrame(window,fg_color="transparent", width=50, height=30)
return_frame.grid(row=1, column=10, padx=10, pady=12)
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

ctk.CTkLabel(window,font=("Ariel",30), text="Enter your budget (INR):").grid(row=1, column=0, padx=10, pady=10)
budget_entry = ctk.CTkEntry(window,width=400,height=30)
budget_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place a button
search_button = ctk.CTkButton(window,fg_color="springgreen3",hover_color="springgreen4",font=("Ariel",20), text="Find Places", command=get_places)
search_button.grid(row=2, columnspan=2, padx=10, pady=10)

# Create a text area to display results
result_text = scrolledtext.ScrolledText(window,font=("Ariel",30), width=80, height=50)
result_text.grid(row=3, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
window.mainloop()
