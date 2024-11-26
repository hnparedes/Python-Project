import numpy as np
import matplotlib.pyplot as plt

from model import Model
from view import View
from controller import Controller

if __name__=="__main__":
	#Model
	model = Model()

	#View
	view = View(model)
	
	#Controller
	controller = Controller(model, view)

	#Run root.mainloop
	view.mainloop()
