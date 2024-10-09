from tkinter import *

root = Tk()
width=800
height=600
root.geometry(f"800x600")

canvas = Canvas(root, width=width, height=height - 65)
canvas.pack()
def draw_grid():
    canvas.delete("all")
    for row in range((height - 65) // 10):
        for col in range(width // 10):
            x1 = col * 10
            y1 = row * 10
            x2 = x1 + 10
            y2 = y1 + 10
            #! make a if condition if(1) fill=yello else fill=white
            canvas.create_rectangle(x1, y1, x2, y2, fill="white")

def resize():
    width = int(width_entry.get())
    height = int(height_entry.get())
    canvas.config(width=width, height=height - 65)
    draw_grid()

def update_speed(value):
    speed_label.config(text=f"Speed: {value}")

controls_frame = Frame(root)
controls_frame.pack(side=BOTTOM, pady=10)

#todo --------> width
Label(controls_frame, text="Width:").grid(row=0, column=0)
width_entry = Entry(controls_frame, width=5)
width_entry.grid(row=0, column=1)
width_entry.insert(0, str(width))

#todo --------> height
Label(controls_frame, text="Height:").grid(row=0, column=2)
height_entry = Entry(controls_frame, width=5)
height_entry.grid(row=0, column=3)
height_entry.insert(0, str(height))

#todo --------> speed
speed_scale = Scale(controls_frame, from_=0, to=100, orient=HORIZONTAL, command=update_speed)
speed_scale.grid(row=0, column=5, ipady=7)
speed_label = Label(controls_frame, text="Speed: 0")
speed_label.grid(row=0, column=6)

#todo --------> update botton
resize_button = Button(controls_frame, text="Update", padx=10,command=resize)
resize_button.grid(row=0, column=4)

draw_grid() 
root.mainloop()
