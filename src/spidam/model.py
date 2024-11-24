import os
import logging
import typing

import ffmpeg
import scipy
import numpy as np

class Model:
    def __init__(self) -> None:
        self._filepath: str = None
        self._audio: np.ndarray = None
        self._sample_rate: int = None
 
    def load_audio(self, filepath: str, output_directory: typing.Optional[str] = None) -> None: 
        # Ensure the file exists
        if not os.path.isfile(filepath):
            logging.critical(f"File {filepath} does not exist")
            raise FileNotFoundError(filepath)
        
        # Check if the file is in wav format
        split_filepath: tuple = os.path.splitext(filepath)
        if split_filepath[1] != '.wav':
            self._filepath = filepath
        else:
            # Convert into a .wav file and store in a temporary directory
            self._convert_to_wav(filepath, output_directory)

    def visualize_waveform(self):
        """ Plot the waveform
        """        
        pass
    def _convert_to_wav(self, filepath: str, output_directory: typing.Optional[str]) -> None:    
        # If the output directory is not set, then use the current working directory
        directory: str = output_directory if output_directory else os.getcwd()

        # Get the filename without the extension and make the output filepath
        basename: str = os.path.basename(filepath)
        filename: str = os.path.splitext(basename)[0] + '.wav'
        output_filepath: str = os.path.join(directory, filename)

        # Load the audiofile and convert into .wav
        ffmpeg.input(filepath).output(output_filepath, ac=1, f='wav').run()
        logging.info("Converted to .wav at {output_filepath}")

    def calculate_rt60(self) -> int:
        pass
    def highest_resonance(self) -> int:
        pass
        
    @property
    def filepath(self) -> str:
        """ Filepath of processed audiofile

        Returns:
            str: Filepath of processed audiofile
        """    

        return self._filepath
    
    @property
    def sample_rate(self) -> int:
        """ Sample rate of the audio file

        Returns:
            int: Sample Rate
        """
        return self._sample_rate
    
