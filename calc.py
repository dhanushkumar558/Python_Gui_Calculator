import tkinter as tk
from tkinter import messagebox
from math import sqrt

# Function to evaluate the expression
def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception as e:
        messagebox.showerror("Error", "Invalid Expression")

# Function to append text to the entry
def append_to_entry(text):
    entry.insert(tk.END, text)

# Function to clear the last character
def clear_last():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current[:-1])

# Function to clear the entry entirely
def clear_entry():
    entry.delete(0, tk.END)

# Function to calculate square root
def calculate_sqrt():
    try:
        result = sqrt(float(entry.get()))
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except ValueError:
        messagebox.showerror("Error", "Invalid Input for Square Root")

# Function to calculate square
def calculate_square():
    try:
        result = float(entry.get()) ** 2
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except ValueError:
        messagebox.showerror("Error", "Invalid Input for Squaring")

# Create the main window
root = tk.Tk()
root.title("Enhanced Calculator")
root.geometry("400x500")
root.resizable(False, False)

# Entry widget for the display
entry = tk.Entry(root, font=("Arial", 24), bd=5, relief=tk.RIDGE, justify="right")
entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

# Button text layout
buttons = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('C', '0', '=', '+'),
    ('√', '^2', '<-', 'AC')
]

# Button configurations
button_config = {
    'font': ("Arial", 18),
    'bd': 3,
    'relief': tk.RAISED,
    'height': 2,
    'width': 5
}

# Add buttons to the grid
for row, btn_row in enumerate(buttons, 1):
    for col, btn_text in enumerate(btn_row):
        if btn_text == "=":
            btn = tk.Button(root, text=btn_text, bg="#4CAF50", fg="white", **button_config, command=calculate)
        elif btn_text == "C":
            btn = tk.Button(root, text=btn_text, bg="#f0ad4e", fg="black", **button_config, command=clear_entry)
        elif btn_text == "AC":
            btn = tk.Button(root, text=btn_text, bg="#d9534f", fg="white", **button_config, command=clear_entry)
        elif btn_text == "<-":
            btn = tk.Button(root, text=btn_text, bg="#5bc0de", fg="black", **button_config, command=clear_last)
        elif btn_text == "√":
            btn = tk.Button(root, text=btn_text, bg="#9C27B0", fg="white", **button_config, command=calculate_sqrt)
        elif btn_text == "^2":
            btn = tk.Button(root, text=btn_text, bg="#FFC107", fg="black", **button_config, command=calculate_square)
        else:
            btn = tk.Button(root, text=btn_text, bg="#e7e7e7", fg="black", **button_config, command=lambda x=btn_text: append_to_entry(x))
        btn.grid(row=row, column=col, padx=5, pady=5)

# Configure row and column weights
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Run the main event loop
root.mainloop()
