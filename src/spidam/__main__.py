from model import Model
from view import View
from controller import Controller

if __name__=="__main__":
	model = Model()
	view = View(model)

	model.load_audio('path_to_audio.wav')

	amplitude = model.waveform_amplitude
	intensity = model.sound_intensity

	print(f"Waveform Amplitude: {amplitude}")
	print(f"Sound Intensity (dB): {intensity}")
	
	#Controller
	controller = Controller(model, view)
	view.set_controller(controller)

	#Run root.mainloop
	view.root.mainloop()
