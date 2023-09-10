from tkinter import *
import random


class MainApp:

    def draw_grid(self, x, y):
        for i in range(self.columns):
            self.canvas.create_line(x * i, 0, x * i, self.canHeight)

        for i in range(self.rows):
            self.canvas.create_line(0, y * i, self.canWidth, y * i)

    def draw(self):
        self.canvas.delete("all")

        self.gWidth = self.canWidth / self.columns
        self.gHeight = self.canHeight / self.rows

        self.draw_grid(self.gWidth, self.gHeight)

        for i in range(self.entities):
            x = random.randint(1, self.columns)
            y = random.randint(1, self.rows)



            self.pWidth = self.gWidth * (x - 1) + (self.canWidth / self.columns / 2)
            self.pHeight = self.gHeight * (y - 1) + (self.canHeight / self.rows / 2)

            self.canvas.create_rectangle(self.pWidth - self.size, self.pHeight - self.size, self.pWidth + self.size,
                                         self.pHeight + self.size,
                                         fill="black", outline="black")

    def windowInterval(self):
        # FOR INTERVALS
        if self.entities != self.entityScale.get() or self.size != self.sizeScale.get() or \
           self.rows != self.rowScale.get() or self.columns != self.columnScale.get():
            self.entities = self.entityScale.get()
            self.size = self.sizeScale.get()
            self.columns = self.columnScale.get()
            self.rows = self.rowScale.get()
        # v
        self.draw()

    def quit(self):
        self.root.destroy()

    def __init__(self):

        # **** Locals ****
        self.columns = 5
        self.rows = 5
        self.size = 5
        self.entities = 1
        self.canWidth = 500
        self.canHeight = 500

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

        # ******* Toolbar ******

        toolBar = Frame(self.root, bg="grey")

        entityFrame = Frame(toolBar)
        entityLabel = Label(entityFrame, text="Entities:")
        entityLabel.pack()
        self.entityScale = Scale(entityFrame, from_=1, to=100, orient=HORIZONTAL)
        self.entityScale.pack()
        entityFrame.pack(side=LEFT, padx=2, pady=5)

        sizeFrame = Frame(toolBar)
        sizeLabel = Label(sizeFrame, text="Size:")
        sizeLabel.pack()
        self.sizeScale = Scale(sizeFrame, from_=1, to=50, orient=HORIZONTAL)
        self.sizeScale.set(5)
        self.sizeScale.pack()
        sizeFrame.pack(side=LEFT, padx=2, pady=5)

        columnFrame = Frame(toolBar)
        columnLabel = Label(columnFrame, text="Columns:")
        columnLabel.pack()
        self.columnScale = Scale(columnFrame, from_=1, to=10, orient=HORIZONTAL)
        self.columnScale.set(5)
        self.columnScale.pack()
        columnFrame.pack(side=LEFT, padx=2, pady=5)

        rowFrame = Frame(toolBar)
        rowLabel = Label(rowFrame, text="Rows:")
        rowLabel.pack()
        self.rowScale = Scale(rowFrame, from_=1, to=10, orient=HORIZONTAL)
        self.rowScale.set(5)
        self.rowScale.pack()
        rowFrame.pack(side=LEFT, padx=2, pady=5)

        drawButton = Button(toolBar, text="Draw", command=self.windowInterval)
        drawButton.pack(side=LEFT, padx=2, pady=5)



        toolBar.pack(side=TOP, fill=X)

        # ********** CANVAS ***********

        self.canvas = Canvas(self.root, width=self.canWidth, height=self.canHeight, bd=1, relief=SOLID)
        self.canvas.pack()
        print(self.size)
        self.draw()

        # *********** STATUS BAR **********

        self.statusBar = Label(self.root, text="Status Bar", bd=1, relief=SUNKEN, anchor=W)

        self.statusBar.pack(side=BOTTOM, fill=X)

        # *****

        #self.root.bind('<Motion>', self.windowInterval)

        self.root.mainloop()


app = MainApp()
