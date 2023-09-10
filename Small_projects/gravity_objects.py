from tkinter import *
import math


class GravityObject:

    def __init__(self, x, y, size, charge, is_still):
        self.size = size

        self.x = x
        self.y = y

        self.charge = charge
        self.is_still = is_still

        self.xs = 0
        self.ys = 0

        self.ax = 0
        self.ay = 0

        if self.charge == "Positive":
            self.c = "blue"
        elif self.charge == "Negative":
            self.c = "red"
        elif self.charge == "Neutral":
            self.c = "grey"

        self.ball = canvas.create_oval(self.x - (self.size / 2), self.y - (self.size / 2), self.x + (self.size / 2),
                                       self.y + (self.size / 2), fill=self.c, outline="black")

        self.force_line = canvas.create_line(self.x, self.y, self.x + self.xs, self.y + self.ys, fill=self.c)

    def move(self):
        for i in objArray:
            if self != i:
                distance = math.sqrt(math.pow(abs(self.y - i.y), 2) + math.pow(abs(self.x - i.x), 2))

                if distance == 0:
                    force = 0
                else:
                    force = forceConst * (self.size * i.size) / math.pow(distance, 2)

                self.ax = force / self.size
                self.ay = force / self.size

                if self.charge == i.charge:
                    if self.x < i.x:
                        self.xs -= self.ax
                    elif self.x > i.x:
                        self.xs += self.ax
                    if self.y < i.y:
                        self.ys -= self.ay
                    elif self.y > i.y:
                        self.ys += self.ay
                else:
                    if self.x < i.x:
                        self.xs += self.ax
                    elif self.x > i.x:
                        self.xs -= self.ax
                    if self.y < i.y:
                        self.ys += self.ay
                    elif self.y > i.y:
                        self.ys -= self.ay

        canvas.move(self.ball, self.xs, self.ys)
        canvas.coords(self.force_line, self.x, self.y, self.x + (self.xs * forceVec), self.y + (self.ys * forceVec))

        self.x += self.xs
        self.y += self.ys

    def is_outside(self):
        if self.x < 0 or self.x > canWidth or self.y < 0 or self.y > canHeight:
            return True
        else:
            return False


def canvas_motion(event):
    x = event.x
    y = event.y
    statusBar.config(text="(" + str(x) + ", " + str(y) + ")")


def animation():
    if len(objArray) > 0:
        for i in objArray:
            if not i.is_still:
                i.move()

            if i.is_outside():
                print("del")

        canvas.update()

    canvas.after(10, animation)


def button_add():
    x = int(xInput.get())
    y = int(yInput.get())
    add_object(x, y)


def clear():
    global objArray
    canvas.delete("all")
    objArray = []


def motion_add(event):
    x = event.x
    y = event.y
    add_object(x, y)


def add_object(x, y):
    size = int(sizeScale.get())
    charge = chargeLabel.get()
    is_still = stillVar.get()

    if charge != "Charge":
        new_obj = GravityObject(x, y, size, charge, is_still)

        objArray.append(new_obj)
    else:
        print("Please assign a charge.")


# **** Globals ****
forceConst = 0.6
forceVec = 100
objArray = []
canWidth = 500
canHeight = 500

root = Tk()

# root.state('zoomed')

# ************ MENU **********

menu = Menu(root)
root.config(menu=menu)

fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Quit", command=root.destroy)
fileMenu.add_command(label="Clear", command=clear)

addMenu = Menu(menu)
menu.add_cascade(label="Add", menu=addMenu)

# ******* Toolbar ******

toolBar = Frame(root, bg="grey")

xFrame = Frame(toolBar)
xLabel = Label(xFrame, text="X")
xLabel.pack()
xInput = Entry(xFrame)
xInput.pack(padx=2)
xFrame.pack(side=LEFT, padx=2, pady=5)

yFrame = Frame(toolBar)
yLabel = Label(yFrame, text="Y")
yLabel.pack()
yInput = Entry(yFrame)
yInput.pack(padx=2)
yFrame.pack(side=LEFT, padx=2, pady=5)

sizeFrame = Frame(toolBar)
sizeLabel = Label(sizeFrame, text="Size")
sizeLabel.pack()
sizeScale = Scale(sizeFrame, from_=1, to=100, orient=HORIZONTAL)
sizeScale.set(20)
sizeScale.pack()
sizeFrame.pack(side=LEFT, padx=2, pady=5)

chargeLabel = StringVar(toolBar)
chargeLabel.set("Charge")
chargeMenu = OptionMenu(toolBar, chargeLabel, "Positive", "Negative", "Neutral")
chargeMenu.pack(side=LEFT, padx=2, pady=5)

stillVar = IntVar()
stillCheck = Checkbutton(toolBar, text="Stationary", variable=stillVar)
stillCheck.pack(side=LEFT, padx=2, pady=5)

drawButton = Button(toolBar, text="Add", command=button_add)
drawButton.pack(side=LEFT, padx=2, pady=5)

toolBar.pack(side=TOP, fill=X)

# ********** CANVAS ***********

canvas = Canvas(root, width=canWidth, height=canHeight, bd=1, relief=SOLID)
canvas.pack()

# *********** STATUS BAR **********

canvas.bind("<Button-1>", motion_add)
canvas.bind('<Motion>', canvas_motion)
statusBar = Label(root, text="(" + str(0) + ", " + str(0) + ")", bd=1, relief=SUNKEN, anchor=W)

statusBar.pack(side=BOTTOM, fill=X)

# ***** Animation *******'
animation()

root.mainloop()
