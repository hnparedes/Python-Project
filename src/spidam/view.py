#genuinely do not know why it needs this, if I take out even one of these imports the program breaks
#may be with my IDE, as tkinter had to be commented out of the requirements.txt to prevent errors
import tkinter as tk
import tkinter.ttk
from tkinter import StringVar
from tkinter import filedialog as fd
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from numpy.typing import NDArray

import os


#from pandas import options

from model import Model


#temporary matplotlib imports for testing graphs soon
#from matplotlib import pyplot as plt
#from matplotlib import FigureCanvasTkAgg
#import matplotlib
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class View:
    def __init__(self, model):
        self.root = tk.Tk()
        self.root.title('Group 25 SPIDAM')
        self.root.resizable(False, False)
        self.root.geometry('870x800')

        self.model = model

        self.controller = None
        def set_controller(self, controller):
            self.controller = controller

        ##will replace
        #self.create_widgets()

        self.target_frequency_index = 0
        self.rt60 = 0

        ##Setting up the main frame that all buttons/labels reside in
        #
        ##This currently has an issue where things are not aligned correctly, will be fixed
        #
        self.mainframe= tkinter.ttk.Frame(self.root, padding='5 5 5 5')
        self.mainframe.grid(row = 0, column = 0, sticky=('E' 'W' 'N' 'S'))
        #three columns to handle buttons
        self.mainframe.grid_columnconfigure((0,1,2),weight=1)

        ##Buttons (this will be moved to self.create_widgets()
        #
        ##Open file button
        #
        #Precursor data for label
        self.gfile = ''
        self.filename =''
        wavfile = StringVar()
        wavfile.set('File Name: ')
        #Function definition
        def open_file():
            filetypes = (('wav files', '*.wav'), ('mpeg-4 files', '*.m4a'), ('All files', '*.*'))
            self.filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
            self.gfile = os.path.basename(self.filename)
            wavfile.set('File Name: ' + self.gfile)
        #Button definition and function call on button press
        _openfile_btn = tkinter.ttk.Button(self.mainframe, text='Open a File', command=open_file)
        _openfile_btn.grid(row = 0, column = 0, sticky='W')
        # Filename label, will start empty and populate after Open file command
        self.filelabel = tkinter.ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.filelabel.grid(row=1, column=1, sticky=('E' 'W' 'N' 'S'))
        mylabel = tk.Label(self.filelabel, textvariable=wavfile)
        mylabel.pack()

        ##Analyze file button
        #
        #Precursor data for labels
        timerec = StringVar()
        timerec.set('File Length = 0s')
        resonance = StringVar()
        resonance.set('Resonant Frequency: ___ Hz')
        rt60 = StringVar()
        rt60.set('Difference: _._s')
        #Function definition
        def analyze_file():
            self.model.load_audio(self.filename)
            #graph call

            timerec.set('File Length: ' + self.model.duration + 's')
            resonance.set('Resonant Frequency: ' + self.model.highest_resonance + ' Hz')
            #replace with the rt60 difference function
            #rt60.set('Difference: ' + _ + 's'))


        #Analyze file button
        _analyzefile_btn = tkinter.ttk.Button(self.mainframe, text='Analyze File', command=analyze_file)
        _analyzefile_btn.grid(row = 0, column = 2, sticky='E')



        ##
        ## GRAPHS WILL GO HERE
        ##
        fig, ax = pyplot.subplots()
        data = np.array(0)
        ax.plot(data)

        pyplot.title("Waveform Graph")
        pyplot.xlabel("Time (s)")
        pyplot.ylabel("Amplitude")
        canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
        canvas.draw()

        canvas.get_tk_widget().grid(row = 2, column = 1, sticky = 'EW')

        #this function and process prevents pyplot.subplots() from preventing the function from exiting
        def _closer():
            self.root.quit()
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", _closer)

        #Intensity Graph
        def intensity_plot():
            pass
        #Waveform Graph (Default)
        def waveform_plot():
            pass
        #temporary graph window
        #this will use mainframe row 2
        #Bonus Graph
        def bonus_plot():
            pass


        ##Graphing buttons
        #
        #Intensity graph button, temporary command that will change graph window to intensity heatmap
        _intensity_btn = tkinter.ttk.Button(self.mainframe, text='Intensity Graph', command=print('Temp Intensity'))
        _intensity_btn.grid(row=3, column=0)

        #Waveform graph button, temporary command that will change graph window to a waveform plot
        _waveform_btn = tkinter.ttk.Button(self.mainframe, text='Waveform Graph', command=print('Temp Waveform'))
        _waveform_btn.grid(row=3, column=1)

        #RT60 cycling graph button, temporary command that will use modulo counter to alternate low-mid-high
        _cycle_btn = tkinter.ttk.Button(self.mainframe, text='Cycle RT60 Graphs', command=(print('Temp Cycle')))
        _cycle_btn.grid(row=3, column=2)

        #RT60 combine graph button, temporary command that will overlay each of the RT60 graphs
        #This button goes between resonance label and rt60 cycle button on the provided example, so it is row 5
        _combine_btn = tkinter.ttk.Button(self.mainframe, text='Combine RT60 Graphs', command=print('Temp Combine'))
        _combine_btn.grid(row=5, column=2)

        ##Labels
        #
        # File Length Label
        self.timelabel = tkinter.ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.timelabel.grid(row=4, column=1, sticky=('E' 'W' 'N' 'S'))
        _timelabel = tk.Label(self.timelabel, textvariable=timerec)
        _timelabel.pack()
        # Resonant Frequency Label
        self.frequencylabel = tkinter.ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.frequencylabel.grid(row=5, column=1, sticky=('E' 'W' 'N' 'S'))
        _frequencylabel = tk.Label(self.frequencylabel, textvariable=resonance)
        _frequencylabel.pack()
        # RT60 Difference Label
        self.rt60difference = tkinter.ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.rt60difference.grid(row=6, column=1, sticky=('E' 'W' 'N' 'S'))
        _rt60difference = tk.Label(self.rt60difference, textvariable=rt60)
        _rt60difference.pack()





#Temporary tester to run the GUI, uncomment this when testing until controller.py exists
if __name__ == "__main__":
    model = Model()
    view = View(model)

    view.root.mainloop()