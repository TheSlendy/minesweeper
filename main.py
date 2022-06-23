from Controller import MinesweeperController
from Model import MinesweeperModel
from View import MinesweeperView

model = MinesweeperModel()
controller = MinesweeperController(model)
view = MinesweeperView(model, controller)
view.pack()
view.mainloop()



