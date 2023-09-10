from tkinter import *
import numpy as np
import random


def drawvalue(i):
    value = random.randint(10, candim - 10)
    valuelist.append(value)

    canvas.create_rectangle(valuewidth * i * 2 + valuewidth, candim - value,
                            valuewidth * i * 2 + (valuewidth * 2), candim, fill="black")
    root.update()


def generatevalues():
    global valuelist
    canvas.delete("all")
    valuelist = []
    for i in range(valueidx):
        root.after(dt, drawvalue(i))


def draw():
    canvas.delete("all")
    for i in range(len(valuelist)):
        canvas.create_rectangle(valuewidth * i * 2 + valuewidth, candim - valuelist[i],
                                valuewidth * i * 2 + (valuewidth * 2), candim, fill="black")


def draw_single(value, i):
    canvas.create_rectangle(valuewidth * i * 2 + valuewidth, candim - value,
                            valuewidth * i * 2 + (valuewidth * 2), candim, fill="black")
    root.update()


def merge(a1, a2):
    canvas.delete("all")
    a3 = []
    i = 0

    while len(a1) > 0 < len(a2):
        if a1[0] > a2[0]:
            a3.append(a2[0])
            a2 = np.delete(a2, 0)
        else:
            a3.append(a1[0])
            a1 = np.delete(a1, 0)
        root.after(dt, draw_single(a3[-1], i))
        i += 1

    while len(a1) > 0:
        a3.append(a1[0])
        a1 = np.delete(a1, 0)
        root.after(dt, draw_single(a3[-1], i))
        i += 1

    while len(a2) > 0:
        a3.append(a2[0])
        a2 = np.delete(a2, 0)
        root.after(dt, draw_single(a3[-1], i))
        i += 1

    return a3


def mergesort(a):
    if len(a) == 1:
        return a
    a1, a2 = np.array_split(a, 2)

    a1 = mergesort(a1)
    a2 = mergesort(a2)

    return merge(a1, a2)


def swapvalues(i1, i2):
    valuelist[i1], valuelist[i2] = valuelist[i2], valuelist[i1]
    draw()


def sortvalues():
    global valuelist
    activesort = sortvar.get()
    if activesort == "Merge":
        valuelist = mergesort(valuelist)

    elif activesort == "Quick":
        print(2)

    elif activesort == "Insertion":
        for i in range(1, len(valuelist)):
            while valuelist[i] < valuelist[i - 1]:
                root.after(dt, swapvalues(i, i - 1))
                root.update()
                i -= 1
                if i == 0:
                    break

    else:
        print("ERROR")

    print("Finished!")


valueidx = 40
candim = 500
dt = 50
valuewidth = candim / (valueidx * 2 + 1)
valuelist = []

root = Tk()
root.title("Sorting algorithm")

Label(root, text="Choose a sorting type").grid(row=1, column=1)

sortingtypes = {"Merge", "Quick", "Insertion"}
sortvar = StringVar(root)
sortvar.set("Merge")

sortmenu = OptionMenu(root, sortvar, *sortingtypes)
sortmenu.config(width=30)
sortmenu.grid(row=1, column=2)

generatebutton = Button(root, text="Generate", command=generatevalues)
generatebutton.grid(row=2, column=1)

sortbutton = Button(root, text="Sort", command=sortvalues)
sortbutton.grid(row=2, column=2)

canvas = Canvas(root, width=candim, height=candim, bd=1, relief=SOLID)
canvas.grid(row=3, column=1, columnspan=2)


root.mainloop()


