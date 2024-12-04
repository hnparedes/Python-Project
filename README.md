# Reverb Analyzer
This project provides a graphical tool to load .wav audio files, convert its formats, clean its data, and analyze its RT60 pattern.

## Features
- **Audio File Loading**: Loads .wav file for analysis, or first converts any audio file type to .wav then anaylzes it.  
- **Data Cleaning**: Processes and cleans the audio data to remove noise.  
- **RT60 Calculation**: Measures the reverberation time (RT60) using exponential decay analysis.  
- **User-Friendly GUI**: Built with an MVC design pattern, allowing clear separation of logic and interface.

## Requirements
- Pycharm
- Python 3.8 or higher  
- Import package libraries listed in `requirements.txt`

## Installation
1. go to the terminal and type pip install -r requirements.txt
2. Run __main__.py file
3. Click open file and select .wav file or any audio file which wil then automatically convert to .wav
4. Click analyze file so that it displays the reverberation frequency graph of the sound file
5. Play around with the graph by selecting either intensity graph, waveform graph, cycle RT60 graphs, or combine RT60 graphs
