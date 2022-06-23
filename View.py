from tkinter import *
from tkinter.messagebox import showinfo
from Model import *


class MinesweeperView(Frame):
    def __init__(self, model, controller, parent=None):
        root = Tk()
        root.title("Minesweeper")
        root.config(bg="#0d161d")
        Frame.__init__(self, parent)
        self.model = model
        self.controller = controller
        self.controller.setView(self)
        am = Frame(self)
        am.pack(side=TOP, fill=X)
        am.config(bg="#0d161d")
        global quest
        quest = PhotoImage(file=r"images/question_mark.png")
        about = Label(am, image=quest, bg="#0d161d")
        about.pack(side=LEFT)
        about.bind("<Button-1>", self.showAboutDeveloper)
        self.mines = Label(am, text=f"bombs={str(self.model.minesCounter)}", bg="#0d161d", fg="#cbd8e8")
        self.mines.pack(side=RIGHT)

        self.createBoard()

        panel = Frame(self)
        panel.pack(side=BOTTOM, fill=X)
        panel.config(bg="#0d161d")

        Button(panel, text='New Game', command=self.controller.startNewGame,
               bg="#0d161d", fg="#cbd8e8", relief=GROOVE).pack(side=RIGHT)

        Label(panel, text=' Difficulty: ', bg="#0d161d", fg="#cbd8e8").pack(side=LEFT)

        self.difficulty = StringVar(panel)
        self.difficulty.set(list(DIFFICULT.keys()))
        Spinbox(
            panel,
            values=list(DIFFICULT.keys()),
            textvariable=self.difficulty,
            width=10,
            bg="#0d161d",
            fg="#cbd8e8",
            relief=FLAT
        ).pack(side=LEFT)

    def syncWithModel(self):
        global bomb, flag
        bomb = PhotoImage(file=r"images/bomb.png")
        flag = PhotoImage(file=r"images/flag.png")
        self.mines.config(text=f"bombs={str(self.model.minesCounter)}")
        for row in range(self.model.cells):
            for column in range(self.model.cells):
                cell = self.model.getCell(row, column)
                if cell:
                    btn = self.buttonsTable[row][column]

                    if self.model.isGameOver() and cell.mined:
                        btn.config(image=bomb)

                    if cell.state == 'closed':
                        btn.config(image='', height=2, width=4, relief=FLAT, bg="#41a2cd")
                    elif cell.state == 'opened':
                        btn.config(relief=FLAT, bg="#0d161d")
                        btn.bind('<Button-1>', 'break')
                        if cell.counter > 0:
                            btn.config(text=cell.counter)
                        elif cell.mined:
                            btn.config(image=bomb, height=33, width=30)
                    elif cell.state == 'flagged':
                        btn.config(image=flag, height=33, width=30)

    def blockCell(self, row, column, block=True):
        btn = self.buttonsTable[row][column]
        if not btn:
            return

        if block:
            btn.bind('<Button-1>', 'break')
        else:
            btn.unbind('<Button-1>')

    def getGameSettings(self):
        return self.difficulty.get()

    def createBoard(self):
        try:
            self.board.pack_forget()
            self.board.destroy()
            self.cells.set(self.model.cells)
            self.mineCount.set(self.model.mineCount)
        except:
            pass

        self.board = Frame(self)
        self.board.pack()
        self.board.config(bg="#0d161d")
        self.buttonsTable = []
        for row in range(self.model.cells):
            line = Frame(self.board)
            line.config(bg="#0d161d")
            line.pack(side=TOP)
            self.buttonsRow = []
            for column in range(self.model.cells):
                btn = Button(
                    line,
                    width=4,
                    height=2,
                    command=lambda row=row, column=column: self.controller.onLeftClick(row, column),
                    padx=0,
                    pady=0,
                    relief=FLAT,
                    bg="#41a2cd",
                    fg="#cbd8e8",
                    activebackground="#3c95bc"
                )
                btn.pack(side=LEFT)
                btn.bind(
                    '<Button-3>',
                    lambda e, row=row, column=column: self.controller.onRightClick(row, column)
                )
                self.buttonsRow.append(btn)

            self.buttonsTable.append(self.buttonsRow)

    def showWinMessage(self):
        showinfo('Поздравляем!', f'Вы победили!\nВремя игры: {self.model.timer()}')

    def showGameOverMessage(self):
        showinfo('Игра окончена!', f'Вы проиграли!\nВремя игры: {self.model.timer()}')

    @staticmethod
    def showAboutDeveloper(*args, **kwargs):
        showinfo("Developer", "Артём Муксунов")
