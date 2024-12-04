# Imports
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
        return self._frequencies[low_mask], self._frequencies[mid_mask], self._frequencies[high_mask]
            
    @functools.cache
    def calculate_rt60(self) -> Tuple[float, float, float]:
        """
        Calculate RT60 reverberation time for low, mid, and high frequencies dynamically 
        based on the loaded audio file's actual frequency ranges.

        Returns:
        - A tuple of RT60 values for low, mid, and high frequencies (in seconds).
        """
        if self._audio is None or self._sample_rate is None:
            raise ValueError("Audio file must be loaded before calculating RT60.")

        # Retrieve the dynamic frequency ranges
        low_freq_range, mid_freq_range, high_freq_range = self.get_frequencies()

        # Helper function to apply a bandpass filter dynamically
        def bandpass_filter(data: NDArray, freq_range: NDArray, sample_rate: int) -> NDArray:
            nyquist = sample_rate / 2
            low_cut = freq_range[0] / nyquist
            high_cut = freq_range[-1] / nyquist
            b, a = scipy.signal.butter(4, [low_cut, high_cut], btype='band')
            return scipy.signal.filtfilt(b, a, data)

        # Apply bandpass filters for dynamic frequency ranges
        low_filtered = bandpass_filter(self._audio, low_freq_range, self._sample_rate)
        mid_filtered = bandpass_filter(self._audio, mid_freq_range, self._sample_rate)
        high_filtered = bandpass_filter(self._audio, high_freq_range, self._sample_rate)

        # Helper function to calculate RT60 for a frequency band
        def calculate_band_rt60(filtered_audio: NDArray) -> float:
            # Convert the signal to decibels
            filtered_db = 10 * np.log10(np.abs(filtered_audio))
        
            # Find the maximum dB value and corresponding index
            max_index = np.argmax(filtered_db)
            max_db = filtered_db[max_index]

            # Slice the audio data and time axis starting from the maximum dB point
            sliced_db = filtered_db[max_index:]
            time_axis = self.time_axis()
            sliced_time = time_axis[max_index:]

            # Determine the -5 dB and -25 dB points
            db_minus_5 = max_db - 5
            db_minus_25 = max_db - 25

            # Helper function to find the index of the nearest value
            def find_nearest_index(array: NDArray, value: float) -> int:
                return (np.abs(array - value)).argmin()

            idx_minus_5 = find_nearest_index(sliced_db, db_minus_5)
            idx_minus_25 = find_nearest_index(sliced_db, db_minus_25)

            # Calculate RT20 and scale to RT60
            time_minus_5 = sliced_time[idx_minus_5]
            time_minus_25 = sliced_time[idx_minus_25]
            rt20 = time_minus_25 - time_minus_5
            return rt20 * 3

        # Calculate RT60 for each frequency range
        rt60_low = calculate_band_rt60(low_filtered)
        rt60_mid = calculate_band_rt60(mid_filtered)
        rt60_high = calculate_band_rt60(high_filtered)

        rt60 = [rt60_low, rt60_mid, rt60_high]
        return tuple(rt60)

    def calculate_rt60_difference(self, target_rt60: float = 0.5) -> float:
        low, mid, high = self.calculate_rt60()
        avg_rt60 = (np.mean(low) + np.mean(mid) + np.mean(high)) / 3
        difference = avg_rt60 - target_rt60
        return difference

    def time_axis(self):
        timeaxis = np.linspace(0.,self._duration,self._audio.shape[0])
        return timeaxis

    @property
    def highest_resonance(self) -> float:
        if self._frequencies is None or self._pxx is None:
            raise ValueError("Audio file must be loaded first.")
        return self._frequencies[np.argmax(self._pxx)]

    def waveform_amplitude(self) -> float:
        return self._audio

    @property
    def filepath(self) -> str:
        """ Filepath of processed audiofile

        Returns:
            str: Filepath
        """    

        return self._filepath

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
