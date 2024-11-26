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

        # Clear the function cache
        self.get_frequencies.cache_clear()
        self.calculate_rt60.cache_clear()
        self.highest_resonance.cac
        logging.info("Function cache cleared")

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
            
    @functools.cache
    def calculate_rt60(self, low_cutoff: int = 60, low_max: int = 250, mid_max: int = 5000, high_cutoff: int = 10000, decay_db: int = 60) -> Tuple[int, int, int, int]:
        """ Generate a tuple containing the low, mid, high, and average rt60 values
        """
        # Get the filtered frequencies and convert into a numpy array
        filtered_frequencies: NDArray = np.vstack(self.get_frequencies(low_cutoff, low_max, mid_max, high_cutoff))

        # Calculate energy arrays - I have no idea if this works lmao. Yall should really check this <3
        power: NDArray = filtered_frequencies ** 2
        power_rev: NDArray = np.flip(power)
        energy: NDArray = np.flip(np.cumsum(power_rev, axis=1))
        energy_db: NDArray = 10 * np.log10(energy / np.max(energy, axis=1))
        l_energy, m_energy, h_energy = np.split(energy_db, 3)
        
        # There's almost certainly a better way to do this but I don't wanna figure this out rn <3
        # Calculate the low RT60
        li_decay = np.where(l_energy <= -decay_db)[0][0]
        lt_decay = li_decay / self._sample_rate
        l_rt60 = (60 / decay_db) * lt_decay

        # Calculate the mid RT60
        mi_decay = np.where(m_energy <= -decay_db)[0][0]
        mt_decay = mi_decay / self._sample_rate
        m_rt60 = (60 / decay_db) * mt_decay

        # Calculate the high RT60
        hi_decay = np.where(h_energy <= -decay_db)[0][0]
        ht_decay = hi_decay / self._sample_rate
        h_rt60 = (60 / decay_db) * ht_decay

        # Calculate the average RT60
        a_rt60 = (l_rt60 + m_rt60 + h_rt60) / 3

        return (l_rt60, m_rt60, h_rt60, a_rt60)


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
    def duration(self) -> int:
        """ Duration of the audio fi;e
        """
        return self._duration
    
    @property
    def unfiltered_frequency(self) -> NDArray:
        return self._frequencies