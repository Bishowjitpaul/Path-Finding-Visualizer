from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from PIL import ImageTk, Image
import time
from algorithm import *


def mainevent():
    HEIGHT = 600
    WIDTH = 600
    SIDE = 24  # Size of 1 cell

    # Check at that location is the wall
    def isWall(a, row, col):
        return a[row][col] == 1

    # Check at that position that is the starting point
    def isStart(a, row, col):
        return a[row][col] == -2

    # Check in that position that the end point
    def isGoal(a, row, col):
        return a[row][col] == 2

    # Reset coordinates within allowed range
    def setInRange(a, row, col):
        if row < 0:
            row = 0
        if row >= len(a):
            row = len(a) - 1
        if col < 0:
            col = 0
        if col >= len(a[0]):
            col = len(a[0]) - 1

        return row, col

    # Board
    class Board(tk.Frame):  # Inherits the frame of tkinter
        def __init__(self, root, h=HEIGHT, w=WIDTH):

            super().__init__(root, width=h, height=w)

            self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg='white')

            heightMatrix = h // SIDE
            widthMatrix = w // SIDE

            self.a = [[0] * (heightMatrix) for i in range(widthMatrix)]  # Matrix of Board

            # 0 to go, 1 to go

            # Initialize the start and end points
            self.startNode = Node(None, (heightMatrix // 2, 0))
            self.endNode = Node(None, (heightMatrix // 2, widthMatrix - 1))

            # Set position for start, end
            startRow, startCol = self.startNode.position
            endRow, endCol = self.endNode.position

            self.a[startRow][startCol] = -2  # The starting point is worth -2
            self.a[endRow][endCol] = 2  # The endpoint has a value of 2

            # List contains the location is wall
            self.wallList = []

        def drawBoard(self):

            self.pack(side='left')
            self.canvas.pack()

            # Draw horizontal and vertical lines to form the board

            # Draw horizontal lines
            x1 = 0
            x2 = WIDTH
            for k in range(0, HEIGHT + 1, SIDE):
                y1 = k
                y2 = k
                self.canvas.create_line(x1, y1, x2, y2)

            # Draw vertical lines
            y1 = 0
            y2 = HEIGHT
            for k in range(0, WIDTH + 1, SIDE):
                x1 = k
                x2 = k
                self.canvas.create_line(x1, y1, x2, y2)

            # Coloring the start and end points
            self.highlight(self.startNode.position[0], self.startNode.position[1], 'green')
            self.highlight(self.endNode.position[0], self.endNode.position[1], 'orange')

        # Create operations with users
        def setUI(self):

            # Click event handling
            self.canvas.bind("<Button-1>", self.callbackClick)

        # Delete content with users
        def disableUI(self):

            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")

        # Update starting and ending points when manipulated
        def updateStart(self, row, col):
            self.a[row][col] = -2
            self.startNode.position = (row, col)

        def updateGoal(self, row, col):
            self.a[row][col] = 2
            self.endNode.position = (row, col)

        # Highlight a clicked cell
        def highlight(self, row, col, color):

            # In fact, create another colored rectangle in that position
            x0 = col * SIDE
            y0 = row * SIDE

            x1 = (col + 1) * SIDE
            y1 = (row + 1) * SIDE

            # If gray, set value and add location to wallList
            if color == 'darkslategray':
                self.a[row][col] = 1
                self.wallList.append((row, col))

            elif color == 'green':
                self.updateStart(row, col)

            elif color == 'orange':
                self.updateGoal(row, col)

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

        def hide(self, row, col):

            if self.a[row][col] == 1:
                self.wallList.remove((row, col))

            # Set value
            self.a[row][col] = 0

            x0 = col * SIDE
            y0 = row * SIDE

            x1 = (col + 1) * SIDE
            y1 = (row + 1) * SIDE

            self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')

        def callbackClick(self, event):

            self.canvas.focus_set()

            row, col = int((event.y) / SIDE), int((event.x) / SIDE)

            row, col = setInRange(self.a, row, col)

            if isStart(self.a, row, col):
                self.canvas.bind("<B1-Motion>", self.dragStart)

            elif isGoal(self.a, row, col):
                self.canvas.bind("<B1-Motion>", self.dragGoal)

            else:

                if isWall(self.a, row, col):
                    self.hide(row, col)
                    self.canvas.bind("<B1-Motion>", self.deleteWall)

                else:
                    self.highlight(row, col, 'darkslategray')
                    self.canvas.bind("<B1-Motion>", self.createWall)

        def dragStart(self, event):

            self.canvas.focus_set()

            oldRow = self.startNode.position[0]
            oldCol = self.startNode.position[1]

            row, col = int((event.y) / SIDE), int((event.x) / SIDE)
            row, col = setInRange(self.a, row, col)

            if not isWall(self.a, row, col) and (oldRow, oldCol) != (row, col) and not isGoal(self.a, row, col):
                self.highlight(row, col, 'green')
                self.hide(oldRow, oldCol)

        def dragGoal(self, event):

            self.canvas.focus_set()

            oldRow = self.endNode.position[0]
            oldCol = self.endNode.position[1]

            row, col = int((event.y) / SIDE), int((event.x) / SIDE)

            row, col = setInRange(self.a, row, col)

            if not isWall(self.a, row, col) and (oldRow, oldCol) != (row, col) and not isStart(self.a, row, col):
                self.highlight(row, col, 'orange')
                self.hide(oldRow, oldCol)

        def createWall(self, event):

            self.canvas.focus_set()

            row, col = int((event.y) / SIDE), int((event.x) / SIDE)
            row, col = setInRange(self.a, row, col)

            if not isWall(self.a, row, col) and not isStart(self.a, row, col) and not isGoal(self.a, row, col):
                self.highlight(row, col, 'darkslategray')

        def deleteWall(self, event):

            self.canvas.focus_set()

            row, col = int((event.y) / SIDE), int((event.x) / SIDE)

            row, col = setInRange(self.a, row, col)

            if isWall(self.a, row, col):
                self.hide(row, col)

    # ================================================================================================================================

    class ProcessBoard(Board):
        def __init__(self, root):

            super().__init__(root)

            self.traversal = []

            self.path = []

            self.algo = "A* Search (Mahattan)"

            self.button = None

        def findPath(self):

            self.clearPath()

            traversal, path = 0, 0

            if self.algo == "A* Search (Mahattan)":

                traversal, path = astar(self.a, self.startNode.position, self.endNode.position)

            elif self.algo == "A* Search (Euclide)":

                traversal, path = astar(self.a, self.startNode.position, self.endNode.position, "Euclide")

            elif self.algo == "Dijkstra Search":
                traversal, path = ucs(self.a, self.startNode.position, self.endNode.position)

            elif self.algo == "Breadth First Search":
                traversal, path = bfs(self.a, self.startNode.position, self.endNode.position)

            else:
                traversal, path = dfs(self.a, self.startNode.position, self.endNode.position)

            if path == -1:
                messagebox.showerror(message='No path', title='Error')

            else:
                self.traversal = traversal
                self.path = path

                self.drawSearch()

        def clearAll(self):

            while self.wallList != []:
                self.hide(self.wallList[0][0], self.wallList[0][1])

            self.clearPath()

        def clearPath(self):

            for x in self.path:
                if x != self.startNode.position and x != self.endNode.position and not isWall(self.a, x[0], x[1]):
                    self.hide(x[0], x[1])
            self.path = []

            for x in self.traversal:
                if x != self.startNode.position and x != self.endNode.position and not isWall(self.a, x[0], x[1]):
                    self.hide(x[0], x[1])
            self.traversal = []

        def linkto(self, optionBoard):
            self.button = optionBoard.runButton

        def drawSearch(self, i=0, j=1):

            self.button.config(state="disable")
            self.disableUI()

            if i >= len(self.traversal) - 1:
                if j >= len(self.path) - 1:

                    self.button.config(state="active")
                    self.setUI()

                    return
                else:
                    self.highlight(self.path[j][0], self.path[j][1], 'yellow')
                    self.canvas.after(0, lambda: self.drawSearch(i, j + 1))
            else:
                self.highlight(self.traversal[i][0], self.traversal[i][1], 'midnightblue')
                self.canvas.after(5, lambda: self.drawSearch(i + 1))

    # ================================================================================================================================

    # BoardOption

    class OptionBoard(tk.Frame):
        def __init__(self, root, h=HEIGHT, w=WIDTH // 3):
            # Frame bên cạnh Main Board
            super().__init__(root, width=h, height=w)
            self.pack(side='left')

            self.process = None

            # Button Run
            self.runButton = None

            # Button Clear All
            self.clearButton = None

            # Button Clear Path
            self.clearPathButton = None

            # Combobox chọn thuật toán
            self.algoBox = ttk.Combobox(self,
                                        values=[
                                            "A* Search (Mahattan)",
                                            "A* Search (Euclide)",
                                            "Dijkstra Search",
                                            "Breadth First Search",
                                            "Depth First Search"])

            self.algoBox.current(0)
            self.algoBox.bind("<<ComboboxSelected>>", self.chooseAlgo)

        def drawOptionBoard(self):
            self.pack(side='left')
            self.runButton.pack(fill='x', padx=10)
            self.clearButton.pack(fill='x', padx=10)
            self.clearPathButton.pack(fill='x', padx=10)
            self.algoBox.pack(fill='x', padx=10)

        def chooseAlgo(self, event):
            self.process.algo = self.algoBox.get()

        def linkto(self, processBoard):
            self.process = processBoard
            self.runButton = tk.Button(self, text='Run', width=10, command=self.process.findPath)
            self.clearButton = tk.Button(self, text='Clear All', width=10, command=self.process.clearAll)
            self.clearPathButton = tk.Button(self, text='Clear Path', width=10, command=self.process.clearPath)

    # ================================================================================================================================

    def main():
        root = tk.Tk()
        root.geometry('770x603+300+50')

        root.resizable(False, False)  # Kích thước cố định cho cửa sổ
        root.title("Pathfinding Visualizer")

        process_board = ProcessBoard(root)
        process_board.drawBoard()
        process_board.setUI()

        option_board = OptionBoard(root)

        option_board.linkto(process_board)
        option_board.drawOptionBoard()

        process_board.linkto(option_board)

        root.mainloop()

    if __name__ == "__main__":
        main()


def areusure():
    answer = messagebox.askquestion("EXIT", 'Do you really want to exit?')
    if answer == 'yes':
        root.quit()


def algorithm():
    algorithm = tk.Tk()
    algorithm.title("Welcome to Info")
    algorithm.geometry('500x400')
    algorithm.iconbitmap("E:\\all\\MY Quarentine python ML works\\CSE PROJECT\\file\\PF\\letter_p_jKk_icon.ico")
    label = Label(algorithm, text='Pathfinding Visualizer', relief='solid', font=('arial', 12, 'bold')).place(x=160,
                                                                                                              y=0)
    label = Label(algorithm, text="Simple Pathfinding Visualizer was made using Python Tkinter",
                  font=('arial', 10, 'bold')).place(x=0, y=30)
    label = Label(algorithm, text='Developers:', relief='solid', font=('arial', 12, 'bold')).place(x=0, y=70)
    label = Label(algorithm, text='Azim Miah - 1808028 - 1808028@student.ruet.ac.bd', font=('arial', 10, 'bold')).place(
        x=0, y=100)
    label = Label(algorithm, text='Bishowjit Paul - 1808029 - 1808029@student.ruet.ac.bd ',
                  font=('arial', 10, 'bold')).place(x=0, y=130)
    label = Label(algorithm, text='A. K. M. Mohibur Rahman - 1808030- 1808030@student.ruet.ac.bd',
                  font=('arial', 10, 'bold')).place(x=0, y=160)
    label = Label(algorithm, text='Abu Bakar Siddik - 1808031 - 1808031@student.ruet.ac.bd ',
                  font=('arial', 10, 'bold')).place(x=0, y=190)
    label = Label(algorithm, text='Enamul Hasan Shahed - 1808032 -1808032@student.ruet.ac.bd ',
                  font=('arial', 10, 'bold')).place(x=0, y=220)
    label = Label(algorithm, text='***feel free to contact with us via the e-mails*** ',
                  font=('arial', 10, 'bold')).place(x=70, y=270)

    # lb=Listbox(algorithm)
    # lb.insert(1,'1808028')
    # lb.insert(2,'1808029')
    # lb.insert(3,'1808030')
    # lb.insert(4,'1808031')
    # lb.insert(5,'1808032')
    # lb.pack()


root = Tk()
root.title('Pathfinding Visualizer')
root.geometry('700x500')
root.iconbitmap(r"E:\all\MY Quarentine python ML works\CSE PROJECT\file\PF\letter_p_jKk_icon.ico")


class Example(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)

        self.image = Image.open("E:\\all\MY Quarentine python ML works\\CSE PROJECT\\file\\PF\\background@288x.png")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


e = Example(root)
e.pack(fill=BOTH, expand=YES)

Photo3 = PhotoImage(file="E:\\all\MY Quarentine python ML works\\CSE PROJECT\\file\\PF\\START.png")
btn1 = Button(root, image=Photo3, command=mainevent, border=0, height=40, width=80, bg='red')
btn1.place(x=310, y=150)

Photo1 = PhotoImage(file="E:\\all\MY Quarentine python ML works\\CSE PROJECT\\file\\PF\\EXIT.png")
btn2 = Button(root, image=Photo1, command=areusure, border=0, height=40, width=80, bg='red')
btn2.place(x=310, y=200)

Photo2 = PhotoImage(file="E:\\all\MY Quarentine python ML works\\CSE PROJECT\\file\\PF\\INFO.png")
btn3 = Button(root, image=Photo2, command=algorithm, border=0, height=40, width=80, bg='red')
btn3.place(x=310, y=250)

root.mainloop()
