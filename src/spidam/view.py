#genuinely do not know why it needs this, if I take out even one of these imports the program breaks
#may be with my IDE, as tkinter had to be commented out of the requirements.txt to prevent errors
import tkinter as tk
import tkinter.ttk
from tkinter import StringVar

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
        self.root.geometry('700x800')

        self.model = model

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
        #Open file button, temporary command
        _openfile_btn = tkinter.ttk.Button(self.mainframe, text='Open a File', command=print('Temp Openfile'))
        _openfile_btn.grid(row = 0, column = 0, sticky='W')

        #Analyze file button, temporary command, will need to be hidden until Open file command has been processed
        _analyzefile_btn = tkinter.ttk.Button(self.mainframe, text='Analyze File', command=print('Temp Analyzefile'))
        _analyzefile_btn.grid(row = 0, column = 2, sticky='E')

        #Filename label, will start empty and populate after Open file command
        wavfile = StringVar()
        TEMPFILENAME = None
        if TEMPFILENAME != None:
            wavfile.set('File Name: ' + self.model._filepath)
        else:
            wavfile.set('File Name: ')
        self.filelabel= tkinter.ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.filelabel.grid(row = 1, column = 1, sticky = ('E' 'W' 'N' 'S'))
        mylabel=tk.Label(self.filelabel,textvariable=wavfile)
        mylabel.pack()

        ##
        ## GRAPHS WILL GO HERE
        ##
        #temporary graph window
        #this will use mainframe row 2


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
        #File Length Label
        #This time duration block will update when the .wav time is analyzed, however this requires
        #model/controller functions before the TEMPORARY markers can be removed.
        timerec = StringVar()
        TEMPORARY = None
        if TEMPORARY != None:
            timerec.set('File Length: ' + str(TEMPORARY) + 's')
        else:
            timerec.set('File Length = ')
        self.timelabel = tkinter.ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.timelabel.grid(row=4, column=1, sticky=('E' 'W' 'N' 'S'))
        _timelabel = tk.Label(self.timelabel, textvariable=timerec)
        _timelabel.pack()

        #Resonant Frequency Label
        #This will work so long as the _highest_resonance() function is return str(frequency)
        resonance = StringVar()
        if self.model._highest_resonance() != None:
            resonance.set('Resonant Frequency: ' + str(self.model._highest_resonance())+' Hz')
        else:
            resonance.set('Resonant Frequency: ')
        self.frequencylabel = tkinter.ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.frequencylabel.grid(row=5, column=1, sticky=('E' 'W' 'N' 'S'))
        _frequencylabel = tk.Label(self.frequencylabel, textvariable=resonance)
        _frequencylabel.pack()

        #RT60 Difference Label
        #This will work so long as the _calculate_rt60() function is return str(frequency)
        rt60 = StringVar()
        if self.model._calculate_rt60() != None:
            rt60.set('Difference: ' + str(self.model._calculate_rt60() + 's'))
        else:
            rt60.set('Difference: ')
        self.rt60difference = tkinter.ttk.Frame(self.mainframe, padding='5 5 5 5')
        self.rt60difference.grid(row=6, column=1, sticky=('E' 'W' 'N' 'S'))
        _rt60difference = tk.Label(self.rt60difference, textvariable=rt60)
        _rt60difference.pack()



#Temporary tester to run the GUI, uncomment this when testing until controller.py exists
'''if __name__ == "__main__":
    model = Model()
    view = View(model)

    view.root.mainloop()'''