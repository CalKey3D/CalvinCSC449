import tkinter as tk

window = tk.Tk()

window.title("GUI Practice")

# Grey Line
canvas = tk.Canvas(window, height=10, bg="grey", bd=0, highlightthickness=0)
canvas.pack(fill=tk.X)

# Text at top
greeting = tk.Label(text="Hello")
greeting.pack()

# Grey Line
canvas = tk.Canvas(window, height=10, bg="grey", bd=0, highlightthickness=0)
canvas.pack(fill=tk.X)

# Fun little useless button
button = tk.Button(
    text="Click me please, I'm lonely",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)

button.pack()

# Grey Line
canvas = tk.Canvas(window, height=10, bg="grey", bd=0, highlightthickness=0)
canvas.pack(fill=tk.X)

# Function to change color with the below radio button
def change_color(color):
    window.config(bg=color)

# Define the color options and store the selected color
colors = ["red", "green", "blue", "yellow"]
selected_color = tk.StringVar(value=colors[0])

# Create and place radio buttons
for color in colors:
    radio_button = tk.Radiobutton(window, text=color.capitalize(), value=color, variable=selected_color, command=lambda: change_color(selected_color.get()))
    radio_button.pack(anchor="w")

# Grey Line
canvas = tk.Canvas(window, height=10, bg="grey", bd=0, highlightthickness=0)
canvas.pack(fill=tk.X)

# Variable to store the state of the checkbox
favorite_number_var = tk.BooleanVar()

# Checkbox
checkbox = tk.Checkbutton(window, text="I like turtles", variable=favorite_number_var)
checkbox.pack(padx=20, pady=20)

# Grey Line
canvas = tk.Canvas(window, height=10, bg="grey", bd=0, highlightthickness=0)
canvas.pack(fill=tk.X)

window.mainloop()