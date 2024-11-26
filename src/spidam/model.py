import os
import logging
import functools
from typing import Tuple, Optional

import ffmpeg
import scipy.io
import scipy.signal
import numpy as np
from numpy.typing import NDArray

class Model:
    def __init__(self) -> None:
        self._filepath: str = None
        self._audio: NDArray = None
        self._sample_rate: int = None
        self._frequencies: NDArray = None
        self._pxx: NDArray = None
        self._duration: int = None
 
    def load_audio(self, filepath: str, output_directory: Optional[str] = None) -> None: 
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

        # Get sample rate, data, frequencies, and pxx values
        self._sample_rate, self._audio = scipy.io.wavfile.read(self._filepath)
        self._frequencies, self._pxx = scipy.signal.welch(self._audio, self._sample_rate)

        # Calculate the duration of the wav file
        self._duration = len(self._audio) / self._sample_rate

    def _convert_to_wav(self, filepath: str, output_directory: Optional[str]) -> None:    
        # If the output directory is not set, then use the current working directory
        directory: str = output_directory if output_directory else os.getcwd()

        # Get the filename without the extension and make the output filepath
        basename: str = os.path.basename(filepath)
        filename: str = os.path.splitext(basename)[0] + '.wav'
        output_filepath: str = os.path.join(directory, filename)

        # Load the audiofile and convert into .wav
        ffmpeg.input(filepath).output(output_filepath, ac=1, f='wav').run()
        self._filepath = output_filepath
        logging.info("Converted to .wav at {output_filepath}")

    @functools.cache
    def get_frequencies(self, low_cutoff: int = 60, low_max: int = 250, mid_max: int = 5000, high_cutoff: int = 10000) -> Tuple[NDArray, NDArray, NDArray]:
        """ Returns the low, mid, and high frequencies as ndarrays in a tuple
        """
        if not self._frequencies:
            logging.critical("Load audio file")
            raise ValueError("Load audio file")
    
        low_mask: NDArray = low_cutoff <= self._frequencies <= low_max
        mid_mask: NDArray = low_max < self._frequencies <= mid_max
        high_mask: NDArray = mid_max < self._frequencies <= high_cutoff

        return (self._frequencies[low_mask], self._frequencies[mid_mask], self._frequencies[high_mask])
            
    def calculate_rt60(self) -> Tuple[int, int, int, int]:
        """ Generate a tuple containing the low, mid, high, and average rt60 values
        """
        pass

    @property
    @functools.cached_property
    def highest_resonance(self) -> int:
        return self._frequencies[np.argmax(self._pxx)]
        
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
    
    @property
    def duration(self) -> int:
        """ Duration of the audio fi;e
        """
        return self._duration
    