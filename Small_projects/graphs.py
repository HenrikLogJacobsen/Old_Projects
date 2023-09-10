from tkinter import *
import operator


class MainApp:

    class Function:

        def __init__(self, master, f):
            self.f = f
            self.master = master
            self.operators = {
                '+': operator.add,
                '-': operator.sub,
                '*': operator.mul,
                '/': operator.truediv}

            self.f = self.process_func(self.f)

        @staticmethod
        def process_func(f):
            result = f.replace(" ", "")
            result = result.lower()
            return result

        @staticmethod
        def is_digit(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        def is_operator(self, s):
            for i in self.operators:
                if i == s:
                    return True
            return False

        def calc_func(self, x):
            result = 0
            num1 = ""
            num2 = ""
            op = ""
            activeOp = False
            f = self.f
            f = f.replace("x", x)
            for i in range(len(f)):
                print(f[i])
                if self.is_digit(f[i]) and not activeOp:
                    print(num1)
                    num1 += f[i]
                elif self.is_digit(f[i]) and activeOp:
                    num2 += f[i]
                elif self.is_operator(f[i]) and activeOp:
                    print("Operating")
                    num1 = self.operators[op](int(num1), int(num2))
                    num2 = ""
                    activeOp = False
                elif self.is_operator(f[i]) and not activeOp:
                    op = f[i]
                    activeOp = True

            print(num1)
            return num1

        def draw(self):
            x = 0
            while x < self.master.canWidth:
                f = int(self.calc_func(str(x)))
                self.master.canvas.create_line(x, self.master.canHeight - f, x + 1, self.master.canHeight - f)
                x += 1

    def add_func(self):
        if self.currentFunc != self.funcInput.get():
            self.currentFunc = self.funcInput.get()
            self.funcArray.append(MainApp.Function(self, self.currentFunc))
            self.funcArray[len(self.funcArray) - 1].draw()

    def motion(self, event):
        pointerX = event.x
        pointerY = event.y

        self.statusBar.config(text="(" + str(pointerX) + ", " + str(pointerY) + ")")

    def clear(self):
        self.canvas.delete("all")
        self.funcArray = []

    def __init__(self):

        # **** Locals ****
        self.currentFunc = ""
        self.funcArray = []
        self.canWidth = 500
        self.canHeight = 500

        self.root = Tk()

        # root.state('zoomed')

        # ************ MENU **********

        menu = Menu(self.root)
        self.root.config(menu=menu)

        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Quit", command=self.root.destroy)
        fileMenu.add_command(label="Clear", command=self.clear)

        addMenu = Menu(menu)
        menu.add_cascade(label="Add", menu=addMenu)

        # ******* Toolbar ******

        toolBar = Frame(self.root, bg="grey")

        funcFrame = Frame(toolBar)
        funcLabel = Label(funcFrame, text="F(x) = ")
        funcLabel.pack(side=LEFT)
        self.funcInput = Entry(funcFrame)
        self.funcInput.pack()
        funcFrame.pack(side=LEFT, padx=2, pady=5)

        drawButton = Button(toolBar, text="Draw", command=self.add_func)
        drawButton.pack(side=LEFT, padx=2, pady=5)

        toolBar.pack(side=TOP, fill=X)

        # ********** CANVAS ***********

        self.canvas = Canvas(self.root, width=self.canWidth, height=self.canHeight, bd=1, relief=SOLID)
        self.canvas.pack()

        # ******* MAIN *******
        canInfoText = "Width: {}px - Height: {}px".format(self.canWidth, self.canHeight)

        self.canInfo = Label(self.root, text=canInfoText)
        self.canInfo.pack()

        # *********** STATUS BAR **********

        self.statusBar = Label(self.root, text="Status Bar", bd=1, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)

        # *****
        self.canvas.bind('<Motion>', self.motion)

        self.root.mainloop()


app = MainApp()
