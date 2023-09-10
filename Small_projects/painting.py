from tkinter import *

rectangleElements = ["x", "y", "width", "height", "color"]
circleElements = ["x1", "y1", "x2", "y2", "color"]
crCircleElements = ["x", "y", "r", "color"]
lineElements = ["x1", "y1", "x2", "y2", "color"]

objInfo = []
newObj = False
activeObj = ""


class NewApp:

        def __init__(self, labelArr, obj):
            self.newRoot = Tk()
            self.inputs = []
            self.obj = obj

            for i in range(len(labelArr)):
                label = Label(self.newRoot, text=labelArr[i])
                label.grid(row=i, column=0)
                self.a1 = Entry(self.newRoot)
                self.a1.grid(row=i, column=1)
                self.inputs.append(self.a1)

            button = Button(self.newRoot, text="Add", command=self.quit)
            button.grid(columnspan=2)
            self.newRoot.mainloop()

        def quit(self):
            global activeObj
            global objInfo
            global newObj
            activeObj = self.obj
            objInfo = []
            for i in range(len(self.inputs)):
                objInfo.append(self.inputs[i].get())

            newObj = True
            print(newObj)
            self.newRoot.destroy()


class MainApp:

    def draw_obj(self):
        if activeObj == "rectangle":
            self.canvas.create_rectangle(objInfo[0], objInfo[1], objInfo[2], objInfo[3],
                                         fill=objInfo[4], outline=objInfo[4])
        elif activeObj == "circle":
            self.canvas.create_oval(objInfo[0], objInfo[1], objInfo[2], objInfo[3],
                                    fill=objInfo[4], outline=objInfo[4])
        elif activeObj == "line":
            self.canvas.create_line(objInfo[0], objInfo[1], objInfo[2], objInfo[3],
                                    fill=objInfo[4])
        elif activeObj == "crCircle":
            self.canvas.create_oval(objInfo[0] - objInfo[2], objInfo[1] - objInfo[2], objInfo[0] + objInfo[2], objInfo[1] + objInfo[2],
                                    fill=objInfo[3], outline=objInfo[3])

    def quit(self):
        self.root.destroy()

    def add_rec(self):
        NewApp(rectangleElements, "rectangle")

    def add_circle(self):
        NewApp(circleElements, "circle")

    def add_cr_circle(self):
        NewApp(crCircleElements, "crCircle")

    def add_line(self):
        NewApp(lineElements, "line")

    def clear(self):
        self.canvas.delete("all")

    def change_color(newColor):
        color = newColor

    def press(self, event):
        self.pressing = True
        if self.colorLabel.get() == "Color":
            print("Set your color first!")

    def release(self, event):
        self.pressing = False

    def windowInterval(self, event):
        global newObj
        if newObj:
            print("drawing")
            self.draw_obj()

        newObj = False

    def motion(self, event):
        drawSize = self.sizeScale.get()
        pointerX = event.x
        pointerY = event.y

        self.statusBar.config(text="(" + str(pointerX) + ", " + str(pointerY) + ")")

        if self.pressing and self.colorLabel.get() != "Color":
            self.canvas.create_oval(pointerX - drawSize, pointerY - drawSize, pointerX + drawSize,
                                    pointerY + drawSize, outline=self.colorLabel.get(), fill=self.colorLabel.get())

    def __init__(self):
        self.root = Tk()
        # root.state('zoomed')

        # ************ MENU **********

        menu = Menu(self.root)
        self.root.config(menu=menu)

        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Quit", command=self.quit)

        addMenu = Menu(menu)
        menu.add_cascade(label="Add", menu=addMenu)
        addMenu.add_command(label="Line", command=self.add_line)
        addMenu.add_command(label="Rectangle", command=self.add_rec)
        addMenu.add_command(label="Circle", command=self.add_circle)
        addMenu.add_command(label="CR Circle", command=self.add_cr_circle)

        # ******* Toolbar ******

        toolBar = Frame(self.root, bg="grey")

        clearButt = Button(toolBar, text="Clear", command=self.clear)
        clearButt.pack(side=LEFT, padx=2, pady=5)

        sizeFrame = Frame(toolBar)
        sizeLabel = Label(sizeFrame, text="Size: ")
        sizeLabel.pack()
        self.sizeScale = Scale(sizeFrame, from_=1, to=30, orient=HORIZONTAL, showvalue=0)
        self.sizeScale.pack()
        sizeFrame.pack(side=LEFT, padx=2, pady=5)

        self.colorLabel = StringVar(toolBar)
        self.colorLabel.set("Color")

        colorMenu = OptionMenu(toolBar, self.colorLabel, "Black", "Red", "Green", "Blue")
        colorMenu.pack(side=LEFT, padx=2, pady=5)

        toolBar.pack(side=TOP, fill=X)

        # ********** CANVAS ***********
        self.pressing = False

        canWidth = 600
        canHeight = 400

        self.canvas = Canvas(self.root, width=canWidth, height=canHeight, bd=1, relief=SOLID)
        self.canvas.pack()

        # *********** STATUS BAR **********

        self.statusBar = Label(self.root, text="( " + str(0) + " , " + str(0) + " )", bd=1, relief=SUNKEN, anchor=W)
        self.root.bind('<Motion>', self.windowInterval)
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind("<Button-1>", self.press)
        self.canvas.bind("<ButtonRelease-1>", self.release)

        self.statusBar.pack(side=BOTTOM, fill=X)

        self.root.mainloop()




app = MainApp()


#app.canvas.create_rectangle(10, 10, 100, 109, fill="red", outline="red")