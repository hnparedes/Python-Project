#Imports
import os
import numpy as np
from tkinter import filedialog as fd

class Controller:
    def __init__(self, model, view):
        #MVC setup
        self.model = model
        self.view = view
        #Precursor definitions
        self.mode = 0
        self.gfile = ''
        self.filename = ''

    #Closer function implementation
    def _closer(self):
        self.view.root.quit()
        self.view.root.destroy()

    #Open file function implementation
    def open_file(self):
        filetypes = (('wav files', '*.wav'), ('mpeg-4 files', '*.m4a'), ('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        self.gfile = os.path.basename(self.filename)

    #Analyze file function implementation
    def analyze_file(self):
        ##Loads selected file into .wav converter and begins analysis
        self.model.load_audio(self.filename)
        ##Default graph call
        self.view.waveform_plot()
        ##Updating labels
        self.view.timerec.set('File Length: ' + str(self.model.duration) + 's')
        self.view.resonance.set('Resonant Frequency: ' + str(self.model.highest_resonance) + ' Hz')
        '''UPDATE WITH RT60 DIFFERENCE FUNCTION'''
        #self.view.rt60.set('Difference: ' + _ + 's'))
        ''''''

    #Intensity Graph Data Connection from Model
    def intensity_plotter(self):
        # Set data (intensity, frequency, time)
        '''UPDATE WITH DATA CALLS AND REMOVE TESTING VALUES'''
        # intensitydata = function for overall intensity
        # frequencydata = function for overall frequency
        # time = self.model.duration()
        intensitydata = np.array([[1, 2, 1], [1, 2, 3], [3, 2, 1]])
        frequencydata = np.array([0, 5, 10])
        time = np.array([1, 2, 3])
        ''''''
        self.view.intensity_plot(intensitydata,frequencydata,time)

    #Waveform Graph Data Connection from Model
    def waveform_plotter(self):
        # Set data (wave amplitude, time)
        '''UPDATE WITH DATA CALLS AND REMOVE TESTING VALUES'''
        # time = self.model.duration()
        # wavedata function, amplitude result
        amplitude = np.array([1, 2, 1])
        time = np.array([1, 2, 3])
        ''''''
        self.view.waveform_plot(amplitude, time)

    #RT60 Alternating Graph Data Connection from Model
    def rt60_plotter(self):
        ##Alterating button tracker- EC
        # Set data depending on alternating state (RT60 frequency, time)
        '''UPDATE WITH DATA CALLS AND REMOVE TESTING VALUES'''
        if self.mode % 3 == 0:  # Low
            modename = "Low RT60 "
            # rtdata = self.model.get_frequencies()[0]
            rtdata = np.array([1, 2, 3])
        elif self.mode % 3 == 1:  # Mid
            modename = "Mid RT60 "
            # rtdata = self.model.get_frequencies()[1]
            rtdata = np.array([3, 2, 1])
        elif self.mode % 3 == 2:  # High
            modename = "High RT60 "
            # rtdata = self.model.get_frequencies()[2]
            rtdata = np.array([2, 3, 2])
        # time = self.model.duration()
        # rtdata = np.array([1, 2, 1])
        time = np.array([1, 2, 3])
        ''''''
        ##Alternating Button - EC
        self.mode+=1
        self.view.rt60_plot(rtdata, time, modename)

    #Combined RT60 Graph Data Connection from Model
    def combinert60_plotter(self):
        # Set data (RT60 frequencies, time)
        '''UPDATE WITH DATA CALLS AND REMOVE TESTING VALUES'''
        # low_wavedata = self.model.get_frequencies()[0]
        # mid_wavedata = self.model.get_frequencies()[1]
        # high_wavedata = self.model.get_frequencies()[2]
        low_wavedata = np.array([1, 2, 3])
        mid_wavedata = np.array([3, 2, 1])
        high_wavedata = np.array([2, 3, 2])
        # time = self.model.duration()
        time = np.array([1, 2, 3])
        ''''''
        self.view.combine_rt60(low_wavedata, mid_wavedata, high_wavedata, time)
