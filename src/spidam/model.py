
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

        # Read .wav file and process metadata
        self._sample_rate, self._audio = scipy.io.wavfile.read(self._filepath)
        self._audio = self._handle_multichannel(self._audio)
        self._frequencies, self._pxx = scipy.signal.welch(self._audio, self._sample_rate, nperseg=4096)

        # Calculate the duration of the wav file
        self._duration = len(self._audio) / self._sample_rate

        # Clear the function cache
        self.get_frequencies.cache_clear()
        self.calculate_rt60.cache_clear()
        logging.info("Audio file loaded and cache cleared")

    def _convert_to_wav(self, filepath: str, output_directory: Optional[str]) -> None:    
        # Determine output directory and filename
        directory = output_directory if output_directory else os.getcwd()
        filename: str = 'out.wav'
        output_filepath: str = os.path.join(directory, filename)

        # Load the audiofile and convert into .wav
        ffmpeg.input(filepath).output(output_filepath, f='wav').run()
        self._filepath = output_filepath
        logging.info("Converted to .wav at {output_filepath}")

    def _handle_multichannel(self, audio_data: NDArray) -> NDArray:
        # Convert multichannel audio to mono by averaging channels
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1).astype(audio_data.dtype)
            logging.info("Multichannel audio converted to mono.")
        return audio_data

    @functools.cache
    def get_frequencies(self, low_cutoff: int = 60, low_max: int = 250, mid_max: int = 5000, high_cutoff: int = 10000) -> Tuple[NDArray, NDArray, NDArray]:
        """ Returns the low, mid, and high frequencies as ndarrays in a tuple
        """
        if self._frequencies is None:
            raise ValueError("Load audio file first")
    
        low_mask: NDArray = np.logical_and(low_cutoff <= self._frequencies, self._frequencies <= low_max)
        mid_mask: NDArray = np.logical_and(low_max < self._frequencies, self._frequencies <= mid_max)
        high_mask: NDArray = np.logical_and(mid_max < self._frequencies, self._frequencies <= high_cutoff)
        return (self._frequencies[low_mask], self._frequencies[mid_mask], self._frequencies[high_mask])
            
    @functools.cache
    def calculate_rt60(self, low_cutoff: int = 60, low_max: int = 250, mid_max: int = 5000, high_cutoff: int = 10000, decay_db: int = 60) -> Tuple[float, float, float]:
        """ Generate a tuple containing the low, mid, high rt60
        """
        filtered_frequencies: Tuple[NDArray, NDArray, NDArray] = self.get_frequencies(low_cutoff, low_max, mid_max, high_cutoff)
        rt60 = []
        for frequency in filtered_frequencies:
            power = frequency ** 2
            power_rev = np.flip(power)
            energy = np.flip(np.cumsum(power_rev))
            energy_db = 10 * np.log10(energy / np.max(energy))
            try:
                i_decay = np.where(energy_db <= -decay_db)[0][0]
                t_decay = i_decay / self._sample_rate
                rt60.append((60 / decay_db) * t_decay)
            except IndexError:
                rt60.append(0.0)
        return tuple(rt60)

    def calculate_rt60_difference(self, target_rt60: float = 0.5) -> float:
        low, mid, high = self.calculate_rt60()
        avg_rt60 = (low + mid + high) / 3
        difference = avg_rt60 - target_rt60
        return difference

    def time_axis(self):
        timeaxis = []
        x: float
        x = 0
        while x < self._duration - (1 / self._sample_rate):
            timeaxis.append(x)
            x+=(1 / self._sample_rate)
        return timeaxis

    @property
    def highest_resonance(self) -> float:
        if self._frequencies is None or self._pxx is None:
            raise ValueError("Audio file must be loaded first.")
        return self._frequencies[np.argmax(self._pxx)]

    #@property
    def waveform_amplitude(self) -> float:
        return self._audio

    def abs_waveform_amplitude(self) -> float:
        return np.abs(self._audio)
    
    #@property
    def sound_intensity(self) ->  NDArray:
        """Average sound intensity in decibels (dB)."""
        if self._audio is None:
            raise ValueError("Audio file must be loaded first.")
        # Compute power of the waveform
        '''
        J: this is wrong, sice np.mean makes this return a single value when the result is meant to be an array.
        The intensity ranges in the SPIDAM example from -100 to ~+50, and there is a value for every point of time.
        It is meant to be plotted as a Z axis on a heatmap where the X is time and Y is the absolute waveform amplitude.
        '''
        # Convert power to dB scale
        intensity_db = 10 * np.log10(self.power())
        return intensity_db
    
    def power(self) -> NDArray:
        if not self._audio:
            raise ValueError("Audio file must be loaded first.")
        return self._audio ** 2

    @property
    def filepath(self) -> str:
        """ Filepath of processed audiofile

        Returns:
            str: Filepath
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
        """ Duration of the audio file

        Returns:
            float: Duration
        """
        return self._duration

    @property
    def unfiltered_frequency(self) -> NDArray:
        """ Frequency of the audio file

        Returns:
            NDArray: Frequencies
        """
        return self._frequencies