import tkinter as tk
from tkinter import ttk
# Add a button to confirm the input
def confirm(popup, user_input):
    popup.result = user_input.get()  # Store the result in the popup object
    popup.destroy()  # Close the popup window

def new_name_popup(root):
    # Create a new Toplevel window
    popup = tk.Toplevel(root)
    popup.title("Popup Window")
    popup.geometry("300x200")  # Width x Height
    popup.grab_set()

    # Create a StringVar to store the user input
    user_input = tk.StringVar()

    # Add a label
    label = tk.Label(popup, text="Enter style name:", font=("Arial", 12))
    label.pack(pady=10)

    # Add an entry widget
    entry = tk.Entry(popup, textvariable=user_input, font=("Arial", 12))
    entry.pack(pady=10)
    entry.focus_set()

    confirm_button = ttk.Button(popup, text="Confirm", command=lambda: confirm(popup,user_input))
    confirm_button.pack(pady=10)

    # Wait for the popup window to close
    root.wait_window(popup)

    # Return the result after the popup is closed
    return getattr(popup, 'result', None)