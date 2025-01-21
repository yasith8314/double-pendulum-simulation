from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from functools import partial
from double_pendulum_formula import get_formaula, solve_formula, get_angles
from plot import animated_pendulum

#Main list to store user input values
slider_values = [0, 0, 0, 0, 0, 0, 0, 0]

def app():
    # Initialize the application with ttkbootstrap
    root = ttk.Window(themename="cyborg")
    root.title("Double Pendulum")
    root.state('zoomed')

    #Get width and height of screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    #Main Frame
    main = ttk.Frame(root, width=screen_width, height=screen_height)
    main.grid(row=0, column=0, sticky='nsew')

    #Tabs (Left)
    tab1 = ttk.Frame(main, width=int(screen_width * 0.75), height=screen_height)
    tab1.pack_propagate(False)
    tab1.grid(row=0, column=0, sticky='nsew') 

    #Tab (Right)
    tab2 = ttk.Frame(main, width=int(screen_width * 0.25), height=screen_height)
    tab2.grid(row=0, column=1, sticky='nsew')

    #Sliders
    slider_names = ["Start Angle 1:", "Start Angle 2:", "Length of rod 1:", "Length of rod 2:",
                    "Initial angular velocity of ball 1:", "Initial angular velocity of ball 2:", "Mass one:", "Mass two:"]
    slider_units= ['deg', 'deg', 'cm', 'cm', "deg/s", "deg/s", 'g', 'g']
   
    length_of_scales = [(0, 179), (0, 179), (10, 200), (10, 200), (-90, 90), (-90, 90), (1, 200), (1, 200)]
        

    padx = 40
    length = int(screen_width * 0.25) - 80

    global slider_values
    def update_label_and_value(value, lbl, index):
        # Update the value in the list
        slider_values[index] = round(float(value), 2) 

        # Update the label
        lbl.config(text=f"{slider_names[index]} {float(value):.2f}{slider_units[index]}") 

    # Add sliders with labels in the side panel
    for i in range(len(slider_names)):
        # Label to display slider value
        label = ttk.Label(tab2, text=f"{slider_names[i]} 0{slider_units[i]}", font=("Arial", 10), anchor="w")

        # Slider (Scale widget)
        slider = ttk.Scale( tab2, from_=length_of_scales[i][0], to=length_of_scales[i][1], orient="horizontal", command=partial(update_label_and_value, lbl=label, index=i), length=length)
        
        #Place item in the tab
        slider.grid(row=i * 2, column=0,sticky="ew", pady=(20, 0), padx=padx)
        label.grid(row=i * 2 + 1, column=0, sticky="w", pady=(0, 20), padx=padx)

    #Get main formulas to solve the problem
    f1, f2 = get_formaula()

    #Start button command
    def start_simulation():
        global slider_values
        nonlocal f1, f2, start, tab1

        #Check user inputs
        if 0 in slider_values[:4] + slider_values[6:]:
            return 

        #Disable buttons
        start.state(["disabled"])
        stop.state(["!disabled"])

        #Solve and get theta values
        a, b = solve_formula(f1, f2, slider_values)

        #Get cordinate values
        values = get_angles(slider_values[2], slider_values[3], a, b)

        #Make the animation
        fig, aimation = animated_pendulum(values, len(a))
        
        # Embed the Matplotlib figure in tab1
        canvas = FigureCanvasTkAgg(fig, tab1)
        canvas.draw()
        canvas.get_tk_widget().pack()

    #Stop button command
    def stop_animation():
        #Disable buttons
        start.state(["!disabled"])
        stop.state(["disabled"])

        #Destroy running animation
        for widget in tab1.winfo_children():
            widget.destroy()
        


    #Start Simulation Button
    start = ttk.Button(tab2, text="Start Simulation", command=start_simulation)
    start.grid(row=17, column=0)

    #Stop Simulation Button
    stop = ttk.Button(tab2, text="Stop Simulation", command=stop_animation, state='disabled')
    stop.grid(row=18, column=0, pady=15)
    
    #Start app
    root.mainloop()

if __name__ == "__main__":
    app()