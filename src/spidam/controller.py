# Imports
import os
from tkinter import filedialog as fd

class Controller:
    def __init__(self, model, view):
        # MVC setup
        self.model = model
        self.view = view
        # Precursor definitions
        self.mode = 0
        self.gfile = ''
        self.filename = ''

    # Closer function implementation
    def _closer(self):
        self.view.root.quit()
        self.view.root.destroy()

    # Open file function implementation
    def open_file(self):
        filetypes = (('wav files', '*.wav'), ('mpeg-4 files', '*.m4a'), ('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        self.gfile = os.path.basename(self.filename)

    # Analyze file function implementation
    def analyze_file(self):
        # Loads selected file into .wav converter and begins analysis
        self.model.load_audio(self.filename)
        # Default graph call
        self.waveform_plotter()
        # Updating labels
        self.view.timerec.set('File Length: ' + str(self.model.duration) + 's')
        self.view.resonance.set('Resonant Frequency: ' + str(self.model.highest_resonance) + ' Hz')
        self.view.rt60.set('Difference: ' + str(self.model.calculate_rt60_difference()) + 's')

    # Intensity Graph Data Connection from Model
    def intensity_plotter(self):
        # Set data (intensity, frequency, time)
        intensitydata = self.model.sound_intensity()
        frequencydata = self.model.abs_waveform_amplitude()
        time = self.model.time_axis()
        self.view.intensity_plot(time, frequencydata, intensitydata)

    # Waveform Graph Data Connection from Model
    def waveform_plotter(self):
        # Set data (wave amplitude, time)
        time = self.model.time_axis()
        amplitude = self.model.waveform_amplitude()
        self.view.waveform_plot(time, amplitude)

    # RT60 Alternating Graph Data Connection from Model
    def rt60_plotter(self):
        # Alternating button tracker- EC
        # Set data depending on alternating state (RT60 frequency, time)
        # Separate RT60 Values
        low = self.model.calculate_rt60()[0]
        mid = self.model.calculate_rt60()[1]
        high = self.model.calculate_rt60()[2]
        if self.mode % 3 == 0:  # Low
            modename = "Low RT60 "
            rtdata = low
        elif self.mode % 3 == 1:  # Mid
            modename = "Mid RT60 "
            rtdata = mid
        elif self.mode % 3 == 2:  # High
            modename = "High RT60 "
            rtdata = high
        time = self.model.time_axis()
        # Alternating Button - EC
        self.mode += 1
        self.view.rt60_plot(time, rtdata, modename)

    # Combined RT60 Graph Data Connection from Model
    def combinert60_plotter(self):
        # Set data (RT60 frequencies, time)
        low, mid, high = self.model.calculate_rt60()
        time = self.model.time_axis()
        self.view.combine_rt60(time, low, mid, high)
