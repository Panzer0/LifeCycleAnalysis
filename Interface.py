import os
import tkinter as tk
from tkinter import ttk, filedialog, CENTER

import LifeTable
import LogNormal


def openFile():
    file = filedialog.askopenfile(mode='r',
                                  filetypes=[('Excel files', '*.xlsx')])
    if file:
        filepath = os.path.abspath(file.name)
        secondView(file.name)


def cleanUpForSecond():
    fileButton.destroy()


def getSurvival(filename, time, label):
    print(f"filename: {filename}, time: {time}")
    label['text'] = LifeTable.executeGetSurvival(filename, time)


def handleLogNormal(filename, label):
    a, b = LogNormal.execute(filename)
    label['text'] = f"Line equation: \n{a} * x + {b}" \
                    f"\na = {a}\nb = {b}" \
                    f"\nλ = {a / b}\nμ = {1 / a}"


def secondView(filename):
    cleanUpForSecond()
    root.geometry('300x200')

    timeLabel = tk.Label(root, text="Enter time")
    timeLabel.grid(row=0, column=0)
    timeLabel.config(bg="teal")

    timeEntry = tk.Entry(root, text="Enter time")
    timeEntry.grid(row=1, column=0)
    timeEntry.config(bg="gray")

    survivalNote = tk.Label(root, text="Survival odds for given time")
    survivalNote.grid(row=0, column=1)
    survivalNote.config(bg="teal")

    survivalLabel = tk.Label(root, text="-")
    survivalLabel.grid(row=1, column=1)
    survivalLabel.config(bg="teal")

    survivalButton = tk.Button(root, text="Confirm",
                               command=lambda: getSurvival("data.xlsx",
                                                           timeEntry.get(),
                                                           survivalLabel)
                               )
    survivalButton.grid(row=2, column=0)
    survivalButton.config(bg="gray")

    functionLabel = tk.Label(root, text="")
    functionLabel.grid(row=4, column=0)
    functionLabel.grid(columnspan=2)
    functionLabel.config(bg="teal")

    logNormalButton = tk.Button(root,
                                text="Display lognormal graph",
                                command=lambda: handleLogNormal("data.xlsx",
                                                                functionLabel))

    logNormalButton.grid(row=3, column=0)
    logNormalButton.config(bg="gray")

    lifeTableButton = tk.Button(root,
                                text="Display life table graphs",
                                command=lambda: LifeTable.execute("data.xlsx"))
    lifeTableButton.grid(row=3, column=1)
    lifeTableButton.config(bg="gray")


root = tk.Tk()
root.configure(bg="Teal")
root.geometry('300x200')
root.iconbitmap('icon.ico')

root.resizable(False, False)

# Create a Button
fileButton = ttk.Button(root, text="Browse", command=openFile)
fileButton.place(relx=root.winfo_width() / 2,
                 rely=root.winfo_height() / 2,
                 anchor=CENTER)

# button
# label
# grid
# entry

root.mainloop()

