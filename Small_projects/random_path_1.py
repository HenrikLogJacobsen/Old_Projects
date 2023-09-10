from tkinter import *
import random
import datetime

class MainApp:

    def check_diag(self, a, x, y):
        NW = False
        NE = False
        SE = False
        SW = False

        if y - 1 >= 0 and y + 1 < self.rows and x - 1 >= 0 and x + 1 < self.columns:
            if not(a[x - 1][y - 1]):
                NW = True

            if not(a[x + 1][y - 1]):
                NE = True

            if not(a[x + 1][y + 1]):
                SE = True

            if not(a[x - 1][y + 1]):
                SW = True

        return [NW, NE, SE, SW]

    def free_room(self, a, x, y):
        airIdx = 0
        canMoveUp = False
        if y - 1 >= 0:
            if not(a[x][y - 1]):
                canMoveUp = True
                airIdx = airIdx + 1

        canMoveDown = False
        if y + 1 < self.rows:
            if not(a[x][y + 1]):
                canMoveDown = True
                airIdx = airIdx + 1

        canMoveLeft = False
        if x - 1 >= 0:
            if not(a[x - 1][y]):
                canMoveLeft = True
                airIdx = airIdx + 1

        canMoveRight = False
        if x + 1 < self.columns:
            if not(a[x + 1][y]):
                canMoveRight = True
                airIdx = airIdx + 1

        return [canMoveUp, canMoveDown, canMoveLeft, canMoveRight, airIdx]

    def can_move(self, a, x, y):
        bool = False

        for i in range(2):
            if self.free_room(a, x, y)[i]:
                boolY = self.free_room(a, x, y + self.moveInfo[i])
                if boolY[4] >= 3:
                    bool = True
            if self.free_room(a, x, y)[i + 2]:
                boolX = self.free_room(a, x + self.moveInfo[i], y)
                if boolX[4] >= 3:
                    bool = True

        return bool

    def make_move(self, a, x, y):

        direction = random.randint(0, 3)  # NSWE

        freeSpace = self.free_room(a, x, y)

        if freeSpace[direction]:
            if direction <= 1:
                canMove = self.free_room(a, x, y + self.moveInfo[direction])
                canDiag = self.check_diag(a, x, y + self.moveInfo[direction])
                if canMove[4] >= 3:
                    if direction == 0 and canDiag[0] and canDiag[1]:
                        a[x][y + self.moveInfo[direction]] = True
                        y = y + self.moveInfo[direction]
                    elif direction == 1 and canDiag[2] and canDiag[3]:
                        a[x][y + self.moveInfo[direction]] = True
                        y = y + self.moveInfo[direction]
            else:
                canMove = self.free_room(a, x + self.moveInfo[direction], y)
                canDiag = self.check_diag(a, x + self.moveInfo[direction], y)
                if canMove[4] >= 3:
                    if direction == 2 and canDiag[0] and canDiag[3]:
                        a[x + self.moveInfo[direction]][y] = True
                        x = x + self.moveInfo[direction]
                    elif direction == 3 and canDiag[1] and canDiag[2]:
                        a[x + self.moveInfo[direction]][y] = True
                        x = x + self.moveInfo[direction]


        return [a, x, y]

    def areaGrid(self):
        a = [[False for i in range(self.rows)] for j in range(self.columns)]
        return a

    def draw_grid(self, x, y):
        for i in range(self.columns):
            self.canvas.create_line(x * i, 0, x * i, self.canHeight)

        for i in range(self.rows):
            self.canvas.create_line(0, y * i, self.canWidth, y * i)

    def draw(self):
        self.gridArray = self.areaGrid()
        self.canvas.delete("all")

        self.gWidth = self.canWidth / self.columns
        self.gHeight = self.canHeight / self.rows

        self.draw_grid(self.gWidth, self.gHeight)

        for i in range(self.entities):
            idx = 0
            self.x = random.randint(0, self.columns - 1)
            self.y = random.randint(0, self.rows - 1)

            self.gridArray[self.x][self.y] = True

            self.canMove = self.can_move(self.gridArray, self.x, self.y)
            while self.canMove and idx < 100:
                idx = idx + 1
                self.pWidth = self.gWidth * self.x + (self.canWidth / self.columns / 2)
                self.pHeight = self.gHeight * self.y + (self.canHeight / self.rows / 2)
                self.canvas.create_rectangle(self.pWidth - self.size, self.pHeight - self.size, self.pWidth + self.size,
                                             self.pHeight + self.size,
                                             fill="black", outline="black")
                self.newMove = self.make_move(self.gridArray, self.x, self.y)

                self.canMove = self.can_move(self.newMove[0], self.newMove[1], self.newMove[2])
                if self.canMove:
                    self.gridArray = self.newMove[0]
                    self.x = self.newMove[1]
                    self.y = self.newMove[2]

    def windowInterval(self):
        # FOR INTERVALS
        if self.entities != self.entityScale.get() or self.size != self.sizeScale.get() or \
           self.rows != self.rowScale.get() or self.columns != self.columnScale.get():
            self.entities = self.entityScale.get()
            self.size = self.sizeScale.get()
            self.columns = self.columnScale.get()
            self.rows = self.rowScale.get()

        self.draw()

    def quit(self):
        self.root.destroy()

    def __init__(self):

        # **** Locals ****
        self.moveInfo = [-1, 1, -1, 1]
        self.columns = 5
        self.rows = 5
        self.size = 5
        self.entities = 5
        self.canWidth = 900
        self.canHeight = 900

        self.root = Tk()

        # self.root.state('zoomed')

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
        self.entityScale.set(2)
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
        self.columnScale = Scale(columnFrame, from_=1, to=100, orient=HORIZONTAL)
        self.columnScale.set(5)
        self.columnScale.pack()
        columnFrame.pack(side=LEFT, padx=2, pady=5)

        rowFrame = Frame(toolBar)
        rowLabel = Label(rowFrame, text="Rows:")
        rowLabel.pack()
        self.rowScale = Scale(rowFrame, from_=1, to=100, orient=HORIZONTAL)
        self.rowScale.set(5)
        self.rowScale.pack()
        rowFrame.pack(side=LEFT, padx=2, pady=5)

        drawButton = Button(toolBar, text="Draw", command=self.windowInterval)
        drawButton.pack(side=LEFT, padx=2, pady=5)

        toolBar.pack(side=TOP, fill=X)

        # ********** CANVAS ***********

        self.canvas = Canvas(self.root, width=self.canWidth, height=self.canHeight, bd=1, relief=SOLID)
        self.canvas.pack()
        self.draw()

        # *********** STATUS BAR **********

        self.statusBar = Label(self.root, text=str(datetime.datetime.now()), bd=1, relief=SUNKEN, anchor=W)

        self.statusBar.pack(side=BOTTOM, fill=X)

        # *****

        #self.root.bind('<Motion>', self.windowInterval)

        self.root.mainloop()


app = MainApp()
