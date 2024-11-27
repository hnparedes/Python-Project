from model import Model
from view import View
from controller import Controller

if __name__=="__main__":
	model = Model()
	view = View(model)
	
	#Controller
	controller = Controller(model, view)
	view.set_controller(controller)

	#Run root.mainloop
	view.root.mainloop()
