# Reverb Analyzer
This project provides a graphical tool to load .wav audio files, convert its formats, clean its data, and analyze its RT60 pattern.

## Features
- **Audio File Loading**: Loads .wav file for analysis, or first converts any audio file type to .wav then anaylzes it.  
- **Data Cleaning**: Processes and cleans the audio data to remove noise.  
- **RT60 Calculation**: Measures the reverberation time (RT60) using exponential decay analysis.  
- **User-Friendly GUI**: Built with an MVC design pattern, allowing clear separation of logic and interface.

## Requirements
- FFmpeg and FFprobe in path
- Python 3.10 or higher  

## Installation
```sh 
git clone https://github.com/sjones5516/spidam
cd spidam
pip install -r requirements.txt
cd src/spidam
python __main__.py
```