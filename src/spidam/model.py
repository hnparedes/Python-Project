import os
import logging
import tempfile

import ffmpeg

# class AudioModel:

#   def __init__(self):
#   self audio_data, sample_rate, and filename here

#   def convert_to_wav(self, file_path):
#   Conversion code here

#   def calculate_rt60(self):
#   Apply calculations to determine RT60

#   def highest_resonance(self):
#   Find the peak frequency
#   Returns highest peak or frequency details here

class Model:
    def __init__(self) -> None:
        self._filepath: str = None
        self._tempdir: tempfile.TemporaryDirectory = None

    def load_audio(self, filepath: str) -> None:
        """ Load and clean the audio file

        Args:
            file_path (str): File path to audio file
        """        
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
            self._convert_to_wav(filepath)

    def visualize_waveform(self):
        """ Plot the waveform
        """        
        pass
    def _convert_to_wav(self, filepath: str) -> None:
        """ Convert the audio file into a .wav file and store in the temporary directory

        Args:
            filepath (str): Audio file to convert
        """        
        # Create a temporary directory to store .wav
        self._tempdir = tempfile.TemporaryDirectory(delete=False)
        logging.info("Created temporary directory")

        # Load the file into ffmpeg and store into the temporary directory
        basename: str = os.path.splitext(filepath)[0]
        output_filepath: str = f"{self._tempdir}/{output_filepath}.wav"
        ffmpeg.input(filepath).output(output_filepath).run()
        logging.info("Converted audio file into .wav")

        # Set the stored filepath
        self._filepath = output_filepath

    def _clean_audio_data(self):
        """ Check and handle meta and multi-channel data
        """        
    def _calculate_rt60(self):
        pass
    def _highest_resonance(self):
        pass

    def __del__(self):
        if self._tempdir:
            self._tempdir.cleanup()
        
    @property
    def filepath(self) -> str:
        """ Filepath of processed audiofile

        Returns:
            str: Filepath of processed audiofile
        """    

        return self._filepath
    