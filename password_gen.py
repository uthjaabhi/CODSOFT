import tkinter as tk
import random
import string

def generate_password(length, complexity):
    characters = string.ascii_letters  # will include letters
    if complexity >= 2:
        characters += string.digits  # will include digits
    if complexity >= 3:
        characters += string.punctuation  # will include special characters

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def on_generate():
    try:
        length = int(length_entry.get())
        complexity = complexity_var.get()
        if length <= 0:
            raise ValueError("Length must be a positive integer.")
        password = generate_password(length, complexity)
        password_label.config(text=password)
    except ValueError as e:
        password_label.config(text="Error: " + str(e))

# creating a main window
root = tk.Tk()
root.title("Password Generator")

# create and place the widgets
length_label = tk.Label(root, text="Password Length:")
length_label.pack()

length_entry = tk.Entry(root)
length_entry.pack()

complexity_var = tk.IntVar(value=1)
complexity_label = tk.Label(root, text="Complexity Level (1-3):")
complexity_label.pack()

complexity_scale = tk.Scale(root, from_=1, to=3, orient=tk.HORIZONTAL, variable=complexity_var)
complexity_scale.pack()

generate_button = tk.Button(root, text="Generate Password", command=on_generate)
generate_button.pack()

password_label = tk.Label(root, text="", font=("Helvetica", 16))
password_label.pack()

# start the GUI event loop
root.mainloop()
