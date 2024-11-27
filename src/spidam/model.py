import os
import logging
import functools
from typing import Tuple, Optional, List

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
        self._duration: float = None
 
    def load_audio(self, filepath: str, output_directory: Optional[str] = None) -> None:
        # Ensure the file exists
        if not os.path.isfile(filepath):
            logging.critical(f"File {filepath} does not exist")
            raise FileNotFoundError(filepath)
        
        # Check if the file is in wav format
        self._convert_to_wav(filepath, output_directory)

        # Get sample rate, data, frequencies, and pxx values
        self._sample_rate, self._audio = scipy.io.wavfile.read(self._filepath)
        self._frequencies, self._pxx = scipy.signal.welch(self._audio, self._sample_rate, nperseg=4096)

        # Calculate the duration of the wav file
        self._duration = len(self._audio) / self._sample_rate

        # Clear the function cache
        self.get_frequencies.cache_clear()
        self.calculate_rt60.cache_clear()
        logging.info("Function cache cleared")

    def _convert_to_wav(self, filepath: str, output_directory: Optional[str]) -> None:    
        # If the output directory is not set, then use the current working directory
        directory: str = output_directory if output_directory else os.getcwd()

        filename: str = 'out.wav'
        output_filepath: str = os.path.join(directory, filename)

        # Load the audiofile and convert into .wav
        ffmpeg.input(filepath).output(output_filepath, ac=1, f='wav').run()
        self._filepath = output_filepath
        logging.info("Converted to .wav at {output_filepath}")

    @functools.cache
    def get_frequencies(self, low_cutoff: int = 60, low_max: int = 250, mid_max: int = 5000, high_cutoff: int = 10000) -> Tuple[NDArray, NDArray, NDArray]:
        """ Returns the low, mid, and high frequencies as ndarrays in a tuple
        """
        if not self._filepath:
            logging.critical("Load audio file")
            raise ValueError("Load audio file")
    
        low_mask: NDArray = np.logical_and(low_cutoff <= self._frequencies, self._frequencies <= low_max)
        mid_mask: NDArray = np.logical_and(low_max < self._frequencies, self._frequencies <= mid_max)
        high_mask: NDArray = np.logical_and(mid_max < self._frequencies, self._frequencies <= high_cutoff)

        return (self._frequencies[low_mask], self._frequencies[mid_mask], self._frequencies[high_mask])
            
    @functools.cache
    def calculate_rt60(self, low_cutoff: int = 60, low_max: int = 250, mid_max: int = 5000, high_cutoff: int = 10000, decay_db: int = 60) -> Tuple[int, int, int, int]:
        """ Generate a tuple containing the low, mid, high, and average rt60 values
        """
        filtered_frequencies: Tuple[NDArray, NDArray, NDArray] = self.get_frequencies(low_cutoff, low_max, mid_max, high_cutoff)
        rt60: List[int] = list()
        for frequency in filtered_frequencies:
            power: NDArray = frequency ** 2
            power_rev: NDArray = np.flip(power)
            energy: NDArray = np.flip(np.cumsum(power_rev))
            energy_db: NDArray = 10 * np.log10(energy / np.max(energy))
            i_decay = np.where(energy_db <= -decay_db)[0][0]
            t_decay = i_decay / self._sample_rate
            rt60.append((60 / decay_db) * t_decay)
        return tuple(rt60)

    @property
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
    def duration(self) -> float:
        """ Duration of the audio fi;e
        """
        return self._duration
    
    @property
    def unfiltered_frequency(self) -> NDArray:
        return self._frequencies