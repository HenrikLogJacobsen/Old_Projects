from tkinter import *
import os
import math


class Box:
    def __init__(self, box_pos):
        self.x1 = box_pos[0]
        self.y1 = box_pos[1]
        self.x2 = box_pos[2]
        self.y2 = box_pos[3]
        self.color = box_pos[4]


class Circle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.c = color
        self.r = 0


class Coin:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value


class Polygon:
    def __init__(self, pos, active, color):
        self.pos = [pos, active]
        self.color = color


class SaveApp:
    def __init__(self):
        self.saveRoot = Tk()
        self.saveRoot.title("DashGameEditor")
        dir_label = Label(self.saveRoot, text="Level Name")
        dir_label.grid(row=0, column=0)
        self.dir = Entry(self.saveRoot)
        self.dir.grid(row=0, column=1)

        button = Button(self.saveRoot, text="Save", command=self.quit)
        button.grid(columnspan=2)
        self.saveRoot.mainloop()

    def quit(self):
        global level_dir
        level_dir = (self.dir.get())
        self.saveRoot.destroy()


class NewApp:
    def __init__(self):
        self.newRoot = Tk()
        self.newRoot.title("DashGameEditor")
        w_label = Label(self.newRoot, text="Width")
        w_label.grid(row=0, column=0)
        self.w = Entry(self.newRoot)
        self.w.grid(row=0, column=1)

        h_label = Label(self.newRoot, text="Height")
        h_label.grid(row=1, column=0)
        self.h = Entry(self.newRoot)
        self.h.grid(row=1, column=1)

        button = Button(self.newRoot, text="Continue", command=self.quit)
        button.grid(columnspan=2)
        self.newRoot.mainloop()

    def quit(self):
        global start_dims
        start_dims = (int(self.w.get()), int(self.h.get()))
        self.newRoot.destroy()


class MainApp:
    def __init__(self):
        NewApp()
        # **** Locals ****
        global start_dims
        try:
            self.level_w, self.level_h = start_dims
        except:
            self.level_w, self.level_h = 0, 0
            print("Level dimensions was not specified. Please try again")

        self.making_circle = False
        self.making_polygon = False
        self.canWidth = 700
        self.canHeight = 700
        self.active_elem = False
        self.active_box_info = []  # x1, y1, x2, y2
        self.box_array = []
        self.coin_array = []
        self.circle_array = []
        self.poly_array = []
        self.x = 0
        self.y = 0
        self.root = Tk()
        self.spawn_pos = (0, 0)
        self.making_spawn = False
        self.offset_x = 0
        self.offset_y = 0
        self.root.title("DashGameEditor")
        self.player_dims = (27, 47)

        # ************ MENU **********
        menu = Menu(self.root)
        self.root.config(menu=menu)

        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Quit", command=self.quit)
        fileMenu.add_command(label="Clear", command=self.clear)
        fileMenu.add_command(label="Save", command=self.save)

        addMenu = Menu(menu)
        menu.add_cascade(label="Add", menu=addMenu)
        addMenu.add_command(label="Spawn Point", command=self.spawn_point)

        # ******* Toolbar ******
        toolBar = Frame(self.root, bg="grey")

        color_frame = Frame(toolBar)
        color_label = Label(color_frame, text="Color")
        color_label.pack(side=LEFT)
        self.colorLabel = StringVar(toolBar)
        self.colorLabel.set("Black")
        colorMenu = OptionMenu(color_frame, self.colorLabel, "Black", "Red", "Green", "Blue")
        colorMenu.pack()
        color_frame.pack(side=LEFT, padx=2, pady=5)

        self.coin_check_var = IntVar()
        self.coin_check = Checkbutton(toolBar, text="Drop Coin", variable=self.coin_check_var, onvalue=1, offvalue=0)
        self.coin_check.pack(side=LEFT)

        self.circle_check_var = IntVar()
        self.circle_check = Checkbutton(toolBar, text="Draw Circle", variable=self.circle_check_var, onvalue=1,
                                        offvalue=0)
        self.circle_check.pack(side=LEFT)

        self.poly_check_var = IntVar()
        self.poly_check = Checkbutton(toolBar, text="Draw Polygons", variable=self.poly_check_var, onvalue=1,
                                      offvalue=0)
        self.poly_check.pack(side=LEFT)

        drawButton = Button(toolBar, text="Draw", command=self.draw)
        drawButton.pack(side=LEFT, padx=2, pady=5)

        toolBar.pack(side=TOP, fill=X)

        # ********** CANVAS ***********
        self.canvas = Canvas(self.root, width=self.canWidth, height=self.canHeight, bd=1, relief=SOLID)
        self.canvas.pack()
        self.draw()

        # *********** STATUS BAR **********
        self.statusBar = Label(self.root, text="Mouse(" + str(self.x) + ", " +
                               str(self.y) + ") Offset("+str(self.offset_x)+", "+str(self.offset_y)+")",
                               bd=1, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)

        # *****
        self.canvas.bind("<Button-1>", self.press)
        self.canvas.bind('<Motion>', self.motion)
        self.root.bind("<KeyPress>", self.key_down)

        self.root.mainloop()

    def draw(self):
        self.canvas.delete("all")
        # Draw level area
        self.canvas.create_rectangle(0, 0, self.canWidth, self.canHeight, fill="black")
        self.canvas.create_rectangle((self.canWidth/2) - (self.level_w/2) + self.offset_x,
                                     (self.canHeight/2) - (self.level_h/2) + self.offset_y,
                                     (self.canWidth/2) + (self.level_w/2) + self.offset_x,
                                     (self.canHeight/2) + (self.level_h/2) + self.offset_y,
                                     outline="grey", fill="white", width=4)
        # Draw coins
        for coin in self.coin_array:
            self.canvas.create_oval(coin.x - 5 + self.offset_x, coin.y - 5 + self.offset_y,
                                    coin.x + 5 + self.offset_x, coin.y + 5 + self.offset_y, fill="yellow")
        # Draw buildings
        for box in self.box_array:
            self.canvas.create_rectangle(box.x1 + self.offset_x, box.y1 + self.offset_y, box.x2 + self.offset_x,
                                         box.y2 + self.offset_y, fill=box.color)
        # Draw spawn pos
        self.canvas.create_rectangle(self.spawn_pos[0] + self.offset_x - (self.player_dims[0]/2) + (self.canWidth/2),
                                     self.spawn_pos[1] + self.offset_y + (self.canHeight/2),
                                     self.spawn_pos[0] + self.offset_x + (self.player_dims[0]/2) + (self.canWidth/2),
                                     self.spawn_pos[1] + self.offset_y + self.player_dims[1] + (self.canHeight/2),
                                     fill="black")
        self.canvas.create_polygon(self.spawn_pos[0] + self.offset_x + (self.canWidth/2),
                                   self.spawn_pos[1] + self.offset_y + (self.canHeight/2),
                                   self.spawn_pos[0] + self.offset_x + 10 + (self.canWidth/2),
                                   self.spawn_pos[1] + self.offset_y + 20 + (self.canHeight/2),
                                   self.spawn_pos[0] + self.offset_x - 10 + (self.canWidth/2),
                                   self.spawn_pos[1] + self.offset_y + 20 + (self.canHeight/2),
                                   fill="grey")

        # Draw circles
        for circle in self.circle_array:
            self.canvas.create_oval(circle.x - circle.r + self.offset_x, circle.y - circle.r + self.offset_y,
                                    circle.x + circle.r + self.offset_x, circle.y + circle.r + self.offset_y,
                                    fill=circle.c)

        # Draw polygons
        for polygon in self.poly_array:
            if len(polygon.pos) == 2:
                self.canvas.create_line(polygon.pos[0], polygon.pos[1])

    def quit(self):
        try:
            self.root.destroy()
        except:
            pass

    def clear(self):
        self.active_elem = False
        self.active_box_info.clear()
        self.box_array.clear()
        self.coin_array.clear()
        self.draw()

    def save(self):
        SaveApp()
        global level_dir
        try:
            global dir
            dir = level_dir
            os.mkdir("data/"+dir)
            print("Directory " + dir + " Created.")

        except FileExistsError:
            print("ERROR")

        props = open("data/" + dir + "/properties.txt", "w")
        # Note spawn pos
        props.write(str(int(self.spawn_pos[0]))+" "+str(int(self.spawn_pos[1])))
        props.close()

        b = open("data/"+dir+"/boxes.txt", "w")
        for box in self.box_array:
            b.write(str(box.x1)+" "+str(box.y1)+" "+str(box.x2)+" "+str(box.y2)+" "+box.color+"\n")
        b.close()

        cir = open("data/" + dir + "/circles.txt", "w")
        for circle in self.circle_array:
            cir.write(str(circle.x) + " " + str(circle.y) + " " + str(circle.r) + " " + str(circle.c) + "\n")
        cir.close()

        p = open("data/" + dir + "/polygons.txt", "w")
        for poly in self.poly_array:
            p.write(str(poly.c) + " ")
            for i in range(len(poly.pos)):
                print(i)
                p.write(str(poly.pos[i]) + " ")
            p.write("\n")
        p.close()

        c = open("data/" + dir + "/coins.txt", "w")
        for coin in self.coin_array:
            c.write(str(coin.x)+" "+str(coin.y)+" "+str(coin.value)+"\n")
        c.close()
        print("Files created successfully")
        self.quit()

    def is_inside_level(self):
        if ((self.canWidth/2) - (self.level_w/2) + self.offset_x <= self.x <=
                (self.canWidth/2) + (self.level_w/2) + self.offset_x and
                (self.canHeight/2) - (self.level_h/2) + self.offset_y <= self.y <=
                (self.canHeight/2) + (self.level_h/2) + self.offset_y):
            return True
        else:
            return False

    def create_box(self):
        self.active_box_info.append(self.x - self.offset_x)
        self.active_box_info.append(self.y - self.offset_y)
        self.active_box_info.append(self.colorLabel.get())
        self.box_array.append(Box(self.active_box_info))
        self.active_elem = False

    def spawn_point(self):
        self.canvas.config(cursor="target")
        self.making_spawn = True

    def key_down(self, event):
        d_off = 5
        if event.char == "w":
            self.offset_y += d_off
        elif event.char == "s":
            self.offset_y -= d_off
        elif event.char == "a":
            self.offset_x += d_off
        elif event.char == "d":
            self.offset_x -= d_off
        else:
            print("Invalid key pressed: " + event.char)
        self.draw()
        self.statusBar.config(text="Mouse(" + str(self.x) + ", " + str(self.y) + ") Offset(" + str(self.offset_x) +
                                   ", " + str(self.offset_y) + ")")

    def press(self, event):
        self.x = event.x
        self.y = event.y

        if self.is_inside_level():
            if self.making_spawn:
                self.spawn_pos = (int(self.x - self.offset_x - (self.canWidth/2)),
                                  (self.y - self.offset_y - (self.canWidth/2)))
                self.making_spawn = False
                self.canvas.config(cursor="arrow")

            elif self.coin_check_var.get():
                self.coin_array.append(Coin(self.x - self.offset_x, self.y - self.offset_y, 1))

            elif self.circle_check_var.get():
                if not self.making_circle:
                    self.making_circle = True
                    self.circle_array.append(Circle(self.x - self.offset_x, self.y - self.offset_y,
                                                    self.colorLabel.get()))
                else:
                    self.making_circle = False

            elif self.poly_check_var.get():
                if not self.making_polygon:
                    self.making_polygon = True
                    print("poly")
                    self.poly_array.append(Polygon((self.x - self.offset_x, self.y - self.offset_y),
                                                   (self.x - self.offset_x, self.y - self.offset_y),
                                                   self.colorLabel.get()))
                else:
                    self.making_polygon = False

            elif not self.making_circle and not self.making_polygon:
                if self.active_elem:
                    self.create_box()
                else:
                    self.active_box_info.clear()
                    self.active_box_info.append(self.x - self.offset_x)
                    self.active_box_info.append(self.y - self.offset_y)
                    self.active_elem = True

        self.draw()

    def motion(self, event):
        self.x = event.x
        self.y = event.y
        if not self.is_inside_level() and self.active_elem:
            self.create_box()
        if self.making_circle:
            c = self.circle_array[len(self.circle_array) - 1]
            self.circle_array[len(self.circle_array) - 1].r = math.sqrt(math.pow(abs(self.x - c.x), 2)
                                                                      + math.pow(abs(self.y - c.y), 2))

        if self.making_polygon:
            p = self.poly_array[len(self.poly_array) - 1]
            self.poly_array[len(self.poly_array) - 1].pos[len(p.pos) - 1] = (self.x, self.y)
        self.draw()
        if self.active_elem:
            self.canvas.create_rectangle(self.active_box_info[0] + self.offset_x,
                                         self.active_box_info[1] + self.offset_y, self.x, self.y)
        self.statusBar.config(text="Mouse(" + str(self.x) + ", " + str(self.y) + ") Offset("+str(self.offset_x) +
                                   ", "+str(self.offset_y)+")")


start_dims = ()
level_dir = ""

app = MainApp()