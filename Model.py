from random import randint
import time

DIFFICULT = {"Easy": [8, 3], "Normal": [16, 30], "Hard": [20, 90]}


class MinesweeperCell:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.state = 'closed'
        self.mined = False
        self.counter = 0

    markSequence = ['closed', 'flagged']

    def nextMark(self):
        if self.state in self.markSequence:
            stateIndex = self.markSequence.index(self.state)
            self.state = self.markSequence[(stateIndex + 1) % len(self.markSequence)]

    def open(self):
        if self.state != 'flagged':
            self.state = 'opened'


class MinesweeperModel:
    def __init__(self):
        self.startGame('Easy')

    def startGame(self, difficulty):
        self.difficulty = difficulty
        self.cells, self.mineCount = DIFFICULT.get(self.difficulty)
        self.firstStep = True
        self.gameOver = False
        self.cellsTable = []
        self.minesCounter = self.mineCount
        for row in range(self.cells):
            cellsRow = []
            for column in range(self.cells):
                cellsRow.append(MinesweeperCell(row, column))
            self.cellsTable.append(cellsRow)

    def getCell(self, row, column):
        if row < 0 or column < 0 or self.cells <= row or self.cells <= column:
            return None

        return self.cellsTable[row][column]

    def isWin(self):
        for row in range(self.cells):
            for column in range(self.cells):
                cell = self.cellsTable[row][column]
                if not cell.mined and (cell.state != 'opened' and cell.state != 'flagged'):
                    return False
        self.running = False
        self.end_time = time.time()
        return True

    def isGameOver(self):
        return self.gameOver

    def openCell(self, row, column):
        cell = self.getCell(row, column)
        if not cell:
            return False

        cell.open()

        if cell.mined:
            self.end_time = time.time()
            self.gameOver = True
            return

        if self.firstStep:
            self.start_time = time.time()
            self.firstStep = False
            self.generateMines()

        cell.counter = self.countMinesAroundCell(row, column)
        if cell.counter == 0:
            neighbours = self.getCellNeighbours(row, column)
            for n in neighbours:
                if n.state == 'closed':
                    self.openCell(n.row, n.column)

    def nextCellMark(self, row, column):
        cell = self.getCell(row, column)
        if cell:
            cell.nextMark()
            if cell.state == "flagged":
                self.minesCounter -= 1
            else:
                self.minesCounter += 1
        else:
            return False

    def generateMines(self):
        for i in range(self.mineCount):
            while True:
                row = randint(0, self.cells - 1)
                column = randint(0, self.cells - 1)
                cell = self.getCell(row, column)
                if not cell.state == 'opened' and not cell.mined:
                    cell.mined = True
                    break

    def countMinesAroundCell(self, row, column):
        neighbours = self.getCellNeighbours(row, column)
        return sum(1 for n in neighbours if n.mined)

    def getCellNeighbours(self, row, column):
        neighbours = []
        for r in range(row - 1, row + 2):
            neighbours.append(self.getCell(r, column - 1))
            if r != row:
                neighbours.append(self.getCell(r, column))
            neighbours.append(self.getCell(r, column + 1))

        return filter(lambda n: n is not None, neighbours)

    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        return "{0:02d}:{1:02d}:{2:02.0f}".format(int(hours), int(mins), sec)

    def timer(self):
        return self.time_convert(self.end_time - self.start_time)
