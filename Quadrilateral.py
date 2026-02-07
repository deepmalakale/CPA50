from tkinter import *
from tkinter import ttk
import sys

#Coordinate class
class Point2D: 
    def __init__(self, init_x:float, init_y:float): 
        acceptable_types = [int, float]
        if (type(init_x) not in acceptable_types or 
            type(init_y) not in acceptable_types):
            raise TypeError('Point coordinates must be a numerical data')
        self.x = init_x 
        self.y = init_y 

    def distance(self, other) -> float: 
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5



class Quadrilateral: 
    def __init__(self, A:Point2D, B:Point2D, C:Point2D, D:Point2D): 
        # Type Checking
        if (type(A) is not Point2D or 
            type(B) is not Point2D or 
            type(C) is not Point2D or 
            type(D) is not Point2D): 
            raise TypeError("Bad type for initial  data, all data must be Point2D objects")
        
        self.A = A 
        self.B = B 
        self.C = C 
        self.D = D 
        
        # Side distance calculation
        self.AB = A.distance(B)
        self.BC = B.distance(C)
        self.CD = C.distance(D) 
        self.DA = D.distance(A)

        # Make sure that the sides are +ve
        if (self.AB <= 0.0 or 
        self.BC <= 0.0 or 
        self.CD <= 0.0 or 
        self.DA <= 0.0): 
            raise ValueError('Input points do not form a valid quadrilateral: zero or negative side length')

        # Valid Quadrilater Checks
        if (
            (self.AB + self.BC + self.CD <= self.DA) or 
            (self.BC + self.CD + self.DA <= self.AB) or 
            (self.CD + self.DA + self.AB <= self.BC) or 
            (self.DA + self.AB + self.BC <= self.CD)
        ): 
            raise ValueError('Input points do not form a valid quadrilateral: sides violate triangle inequality')

    def perimeter(self) -> float: 
        return self.AB + self.BC + self.CD + self.DA 

    def area(self) -> float: 
        s = self.perimeter() / 2.0
        return ((s - self.AB) * (s - self.BC) * (s - self.CD) * (s - self.DA) ) ** 0.5



points = []
temp_line = None
canvas_handle = None
output_var = None


#All event handlers

def draw_point(p):
    r = 4
    # Draw red point
    canvas_handle.create_oval(
        p.x - r, p.y - r,
        p.x + r, p.y + r,
        fill="red", outline="red"
    )
    # Display coordinates next to the coordinates
    canvas_handle.create_text(
        p.x + 10, p.y - 10,
        text=f"({p.x},{p.y})",
        anchor=NW,
        fill="black",
        font=("Arial", 10, "bold")
    )

def onMouseClick(event):
    global points, temp_line

    if len(points) >= 4:
        return None

    p = Point2D(event.x, event.y)
    points.append(p)

    draw_point(p)

    if len(points) > 1:
        p1 = points[-2]
        p2 = points[-1]
        canvas_handle.create_line(p1.x, p1.y, p2.x, p2.y, fill="green", width=2)

    if len(points) == 4:
        canvas_handle.create_line(points[3].x, points[3].y, points[0].x, points[0].y, fill="green", width=2)

def onMouseMove(event):
    global temp_line

    if len(points) == 0 or len(points) >= 4:
        return None

    if temp_line is not None:
        canvas_handle.delete(temp_line)

    last_point = points[-1]
    temp_line = canvas_handle.create_line(last_point.x, last_point.y, event.x, event.y, dash=(4,2), fill="green")

def onPerimeter():
    global output_var
    try:
        if len(points) != 4:
            raise ValueError("Quadrilateral is not complete")
        Q = Quadrilateral(points[0], points[1], points[2], points[3])
        output_var.set(f"Perimeter = {Q.perimeter()}")
    except Exception as e:
        output_var.set(str(e))

def onArea():
    global output_var
    try:
        if len(points) != 4:
            raise ValueError("Quadrilateral not complete")
        Q = Quadrilateral(points[0], points[1], points[2], points[3])
        output_var.set(f"Area = {Q.area()}")
    except Exception as e:
        output_var.set(str(e))

def onClear():
    global points, temp_line, output_var
    canvas_handle.delete("all")
    points.clear()
    temp_line = None
    output_var.set("Output will be shown here")



def Quadrilateral_func():
    global canvas_handle, output_var

    root_window = Tk()
    root_window.title("Quadrilateral Drawer")

    main_frame = ttk.Frame(root_window, padding="3 3 12 12")
    main_frame.grid(row=1, column=1, sticky=(N,W,E,S))

    canvas_handle = Canvas(main_frame, width=600, height=400, bg="white")
    canvas_handle.grid(row=1, column=1, columnspan=3, sticky=(W,E))
    canvas_handle.bind("<Button-1>", onMouseClick)
    canvas_handle.bind("<Motion>", onMouseMove)

    button_frame = ttk.Frame(main_frame, padding="3 3 12 12")
    button_frame.grid(row=2, column=1, sticky=(W,E))

    perimeter_button = ttk.Button(button_frame, text="Perimeter", command=onPerimeter)
    perimeter_button.grid(row=1, column=1)

    area_button = ttk.Button(button_frame, text="Area", command=onArea)
    area_button.grid(row=1, column=2)

    clear_button = ttk.Button(button_frame, text="Clear", command=onClear)
    clear_button.grid(row=1, column=3)

    output_var = StringVar()
    output_var.set("Output will be shown here")
    output_label = ttk.Label(main_frame, textvariable=output_var)
    output_label.grid(row=3, column=1, sticky=(W,E))

    for widget in main_frame.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    root_window.mainloop()


def main():
    Quadrilateral_func()


main()
