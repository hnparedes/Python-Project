# Imports
import tkinter as tk
import tkinter.ttk
from tkinter import StringVar
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class View:
    def __init__(self, model):
        #                #
        # Tkinter Setup  #
        #                #
        # root
        self.root = tk.Tk()
        self.root.title('Group 25 SPIDAM')
        self.root.resizable(False, False)
        self.root.geometry('850x750')

        # MVC Definition
        self.model = model
        self.controller = None

        # Setting up the main frame that all buttons/labels reside in
        self.mainframe = tkinter.ttk.Frame(self.root, padding='5 5 5 5')
        self.mainframe.grid(row=0, column=0, sticky=(''))
        self.mainframe.grid_columnconfigure((0, 1, 2), weight=1)

        # Setting up a hidden frame that opens after file is analyzed
        self.hiddenframe = tkinter.ttk.Frame(self.root, padding='5 5 5 5')
        self.hiddenframe.grid(row=1, column=0, sticky=(''))
        self.hiddenframe.grid_columnconfigure((0, 1, 2), weight=1)
        # Hide the hidden frame on init
        self.hiddenframe.grid_forget()

        # Closer function and process prevents pyplot.subplots() from preventing the function from exiting properly.
        def _closer():
            if self.controller:
                self.controller._closer()
        self.root.protocol("WM_DELETE_WINDOW", _closer)

        #         #
        # Buttons #
        #         #

        # Precursor data for labels
        self.wavfile = StringVar()
        self.wavfile.set('File Name: ')
        self.timerec = StringVar()
        self.timerec.set('File Length = 0s')
        self.resonance = StringVar()
        self.resonance.set('Resonant Frequency: ___ Hz')
        self.rt60 = StringVar()
        self.rt60.set('Difference: _._s')

        # Open file command definition
        def open_file():
            if self.controller:
                self.controller.open_file()
                self.wavfile.set('File Name: ' + self.controller.gfile)
                # Create analyze file button after open file command
                _analyzefile_btn = tkinter.ttk.Button(self.mainframe, text='Analyze File', command=analyze_file)
                _analyzefile_btn.grid(row=1, column=0, sticky='W')

        # Open file button
        _openfile_btn = tkinter.ttk.Button(self.mainframe, text='Open a File', command=open_file)
        _openfile_btn.grid(row=0, column=0, sticky='W')

        # Filename label, will start empty and populate after Open file command
        self.filelabel = tkinter.ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.filelabel.grid(row=1, column=1, sticky=('E' 'W' 'N' 'S'))
        mylabel = tk.Label(self.filelabel, textvariable=self.wavfile)
        mylabel.pack()

        # Analyze command Definition
        def analyze_file():
            if self.controller:
                self.controller.analyze_file()
                # Return hidden frame after analyze file command
                self.hiddenframe.grid()

        #          #
        #  GRAPHS  #
        #          #
        # Empty Graph
        self.fig, ax = pyplot.subplots()
        data = (0)
        time = (0)
        ax.plot(time, data)
        pyplot.title("Default Graph")
        pyplot.xlabel("X-axis")
        pyplot.ylabel("Y-axis")
        canvas = FigureCanvasTkAgg(self.fig, master=self.mainframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=1)

        # Graphing buttons
        # Intensity Button - Heatmap, Bonus Graph
        def intensity_selected():
            if self.controller:
                self.controller.intensity_plotter()
        _intensity_btn = tkinter.ttk.Button(self.hiddenframe, text='Intensity Graph', command=intensity_selected)
        _intensity_btn.grid(row=3, column=0)

        # Waveform Button - Waveform Graph
        def waveform_selected():
            if self.controller:
                self.controller.waveform_plotter()
        _waveform_btn = tkinter.ttk.Button(self.hiddenframe, text='Waveform Graph', command=waveform_selected)
        _waveform_btn.grid(row=4, column=0)

        # RT60 Button
        def rt60_selected():
            if self.controller:
                self.controller.rt60_plotter()
        _cycle_btn = tkinter.ttk.Button(self.hiddenframe, text='Cycle RT60 Graphs', command=rt60_selected)
        _cycle_btn.grid(row=5, column=0)

        # Combined RT60 Button
        def combinert60_selected():
            if self.controller:
                self.controller.combinert60_plotter()
        _combine_btn = tkinter.ttk.Button(self.hiddenframe, text='Combine RT60 Graphs', command=combinert60_selected)
        _combine_btn.grid(row=6, column=0)

        #          #
        #  Labels  #
        #          #
        # File Length Label
        self.timelabel = tkinter.ttk.Frame(self.hiddenframe, padding='5 5 5 5')
        self.timelabel.grid(row=4, column=1, sticky=('E' 'W' 'N' 'S'))
        _timelabel = tk.Label(self.timelabel, textvariable=self.timerec)
        _timelabel.pack()

        # Resonant Frequency Label
        self.frequencylabel = tkinter.ttk.Frame(self.hiddenframe, padding='5 5 5 5')
        self.frequencylabel.grid(row=5, column=1, sticky=('E' 'W' 'N' 'S'))
        _frequencylabel = tk.Label(self.frequencylabel, textvariable=self.resonance)
        _frequencylabel.pack()

        # RT60 Difference Label
        self.rt60difference = tkinter.ttk.Frame(self.hiddenframe, padding='5 5 5 5')
        self.rt60difference.grid(row=6, column=1, sticky=('E' 'W' 'N' 'S'))
        _rt60difference = tk.Label(self.rt60difference, textvariable=self.rt60)
        _rt60difference.pack()

    # Intensity Graph Implementation - This is the bonus graph
    def intensity_plot(self, time, frequencydata, intensitydata):
        # Clear previous graph
        pyplot.clf()

        # Defining plot
        pyplot.pcolormesh([time, frequencydata, intensitydata], cmap='autumn_r')
        pyplot.colorbar(location='right', orientation='vertical', label='Intensity (dB)')

        # Updating plot labels
        pyplot.title("Frequency Graph")
        pyplot.xlabel("Time (s)")
        pyplot.ylabel("Frequency (Hz)")

        # Updating GUI
        canvas = FigureCanvasTkAgg(self.fig, master=self.mainframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=1)

    # Waveform Graph Implementation (Default)
    def waveform_plot(self, time, amplitude):
        # Clear previous graph
        pyplot.clf()

        # Defining plot
        pyplot.plot(time, amplitude)

        # Updating plot labels
        pyplot.title("Waveform Graph")
        pyplot.xlabel("Time (s)")
        pyplot.ylabel("Amplitude")

        # Updating GUI
        canvas = FigureCanvasTkAgg(self.fig, master=self.mainframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=1)

    # Cycle RT60 Graph Implementation
    def rt60_plot(self, time, rtdata, modename):
        # Clear previous graph
        pyplot.clf()

        # Defining plot
        pyplot.plot(time, rtdata)

        # Updating plot labels (title is dynamic with RT60 type)
        pyplot.title(modename+"Graph")
        pyplot.xlabel("Time (s)")
        pyplot.ylabel("Power (dB)")

        # Updating GUI
        canvas = FigureCanvasTkAgg(self.fig, master=self.mainframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=1)

    # Combined RT60 Graph Implementation
    def combine_rt60(self, time, low, mid, high):
        # Clear previous graph
        pyplot.clf()

        # Defining plot for all three graphs
        pyplot.plot(time, low)
        pyplot.plot(time, mid)
        pyplot.plot(time, high)

        # Updating plot labels
        pyplot.title("Combined Waveform Graph")
        pyplot.xlabel("Time (s)")
        pyplot.ylabel("Power (dB)")

        # Updating GUI
        canvas = FigureCanvasTkAgg(self.fig, master=self.mainframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=1)

    # Controller link
    def set_controller(self, controller):
        self.controller = controller
