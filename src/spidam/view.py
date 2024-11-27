#Imports
import tkinter as tk
import tkinter.ttk
from tkinter import StringVar
from tkinter import filedialog as fd
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
from model import Model

class View:
    def __init__(self, model):
        ###                 ###
        ### Tkinter Setup   ###
        ###                 ###
        ##root
        self.root = tk.Tk()
        self.root.title('Group 25 SPIDAM')
        self.root.resizable(False, False)
        self.root.geometry('850x750')
        #
        ##MVC Definition
        self.model = model
        '''UPDATE WHEN THE CONTROLLER IS SETUP'''
        #self.controller = None
        #def set_controller(self, controller):
            #self.controller = controller
        ''''''
        #
        ##Setting initial values for labels
        self.target_frequency_index = 0
        self.rt60 = 0
        #
        ##Setting up the main frame that all buttons/labels reside in
        self.mainframe= tkinter.ttk.Frame(self.root, padding='5 5 5 5')
        self.mainframe.grid(row = 0, column = 0, sticky=(''))
        self.mainframe.grid_columnconfigure((0,1,2),weight=1)
        #
        ##Closer function and process prevents pyplot.subplots() from preventing the function from exiting properly.
        def _closer():
            self.root.quit()
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", _closer)

        ###         ###
        ### Buttons ###
        ###         ###
        ##Open file button
        #
        #Precursor data for label
        self.gfile = ''
        self.filename =''
        wavfile = StringVar()
        wavfile.set('File Name: ')
        #
        #Open function definition
        def open_file():
            filetypes = (('wav files', '*.wav'), ('mpeg-4 files', '*.m4a'), ('All files', '*.*'))
            self.filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
            self.gfile = os.path.basename(self.filename)
            wavfile.set('File Name: ' + self.gfile)
        #Open file button, command calls the open_file function
        _openfile_btn = tkinter.ttk.Button(self.mainframe, text='Open a File', command=open_file)
        _openfile_btn.grid(row = 0, column = 0, sticky = 'W')
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
        #Precursor data for graphs
        self.mode = 0
        #
        #Analyze function Definition
        def analyze_file():
            ##Loads selected file into .wav converter and begins analysis
            self.model.load_audio(self.filename)
            ##Default graph call
            waveform_plot()
            ##Updating labels
            timerec.set('File Length: ' + self.model.duration + 's')
            resonance.set('Resonant Frequency: ' + self.model.highest_resonance + ' Hz')
            '''UPDATE WITH RT60 DIFFERENCE FUNCTION'''
            #rt60.set('Difference: ' + _ + 's'))
            ''''''
        #Analyze file button, command calls the analyze_file function
        _analyzefile_btn = tkinter.ttk.Button(self.mainframe, text='Analyze File', command=analyze_file)
        _analyzefile_btn.grid(row = 1, column = 0, sticky = 'W')

        ###          ###
        ###  GRAPHS  ###
        ###          ###
        #Empty Graph
        fig, ax = pyplot.subplots()
        data = np.array(0)
        time = np.array(0)
        ax.plot(time, data)
        pyplot.title("Default Graph")
        pyplot.xlabel("X-axis")
        pyplot.ylabel("Y-axis")
        canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 2, column = 1)

        #Intensity Graph - This is the bonus graph
        def intensity_plot():
            #Clear previous graph
            pyplot.clf()
            #
            #Set data (intensity, frequency, time)
            '''UPDATE WITH DATA CALLS AND REMOVE TESTING VALUES'''
            #intensitydata = function for overall intensity
            #frequencydata = function for overall frequency
            #time = self.model.duration()
            intensitydata = np.array([[1,2,1],[1,2,3],[3,2,1]])
            frequencydata = np.array([0, 5, 10])
            time = np.array([1, 2, 3])
            ''''''
            #
            #Defining plot
            pyplot.pcolormesh(time, frequencydata, intensitydata, cmap='autumn_r')
            pyplot.colorbar(location='right',orientation='vertical',label='Intensity (dB)')
            #
            #Updating plot labels
            pyplot.title("Frequency Graph")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Frequency (Hz)")
            #
            #Updating GUI
            canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=1)

        #Waveform Graph (Default)
        def waveform_plot():
            #Clear previous graph
            pyplot.clf()
            #
            #Set data (wave amplitude, time)
            '''UPDATE WITH DATA CALLS AND REMOVE TESTING VALUES'''
            # time = self.model.duration()
            #wavedata function, amplitude result
            wavedata = np.array([1, 2, 1])
            time = np.array([1, 2, 3])
            ''''''
            #
            #Defining plot
            pyplot.plot(time, wavedata)
            #
            #Updating plot labels
            pyplot.title("Waveform Graph")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Amplitude")
            #
            #Updating GUI
            canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=1)

        #Cycle RT60 graph
        def rt60_plot():
            #Clear previous graph
            pyplot.clf()
            #
            ##Alterating button tracker- EC
            #Set data depending on alternating state (RT60 frequency, time)
            '''UPDATE WITH DATA CALLS AND REMOVE TESTING VALUES'''
            if self.mode % 3 == 0: #Low
                modename = "Low RT60 "
                #rtdata = self.model.get_frequencies()[0]
                rtdata = np.array([1, 2, 3])
            elif self.mode % 3 == 1: #Mid
                modename = "Mid RT60 "
                #rtdata = self.model.get_frequencies()[1]
                rtdata = np.array([3, 2, 1])
            elif self.mode % 3 == 2: #High
                modename = "High RT60 "
                #rtdata = self.model.get_frequencies()[2]
                rtdata = np.array([2, 3, 2])
            #time = self.model.duration()
            #rtdata = np.array([1, 2, 1])
            time = np.array([1, 2, 3])
            ''''''
            #
            #Defining plot
            pyplot.plot(time, rtdata)
            #
            #Updating plot labels (title is dynamic with RT60 type)
            pyplot.title(modename+"Graph")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Power (dB)")
            #
            #Updating GUI
            canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=1)
            #
            ##Alternating Button - EC
            self.mode+=1

        #Combined RT60 grapher
        def combine_rt60():
            #Clear previous graph
            pyplot.clf()
            #
            #Set data (RT60 frequencies, time)
            '''UPDATE WITH DATA CALLS AND REMOVE TESTING VALUES'''
            #low_wavedata = self.model.get_frequencies()[0]
            #mid_wavedata = self.model.get_frequencies()[1]
            #high_wavedata = self.model.get_frequencies()[2]
            low_wavedata = np.array([1, 2, 3])
            mid_wavedata = np.array([3, 2, 1])
            high_wavedata = np.array([2, 3, 2])
            #time = self.model.duration()
            time = np.array([1, 2, 3])
            ''''''
            #
            #Defining plot for all three graphs
            pyplot.plot(time, low_wavedata)
            pyplot.plot(time, mid_wavedata)
            pyplot.plot(time, high_wavedata)
            #
            #Updating plot labels
            pyplot.title("Combined Waveform Graph")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Power (dB)")
            #
            #Updating GUI
            canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=1)

        ##Graphing buttons
        #
        #Intensity graph button, command that changes graph window to intensity heatmap
        _intensity_btn = tkinter.ttk.Button(self.mainframe, text='Intensity Graph', command=intensity_plot)
        _intensity_btn.grid(row=3, column=0)

        #Waveform graph button, command that changes graph window to a waveform plot
        _waveform_btn = tkinter.ttk.Button(self.mainframe, text='Waveform Graph', command=waveform_plot)
        _waveform_btn.grid(row=4, column=0)

        #RT60 cycling graph button, command that uses modulo counter to alternate low-mid-high RT60 plots
        _cycle_btn = tkinter.ttk.Button(self.mainframe, text='Cycle RT60 Graphs', command=rt60_plot)
        _cycle_btn.grid(row=5, column=0)

        #RT60 combine graph button, command that overlays each of the RT60 graphs
        _combine_btn = tkinter.ttk.Button(self.mainframe, text='Combine RT60 Graphs', command=combine_rt60)
        _combine_btn.grid(row=6, column=0)

        ###          ###
        ###  Labels  ###
        ###          ###
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