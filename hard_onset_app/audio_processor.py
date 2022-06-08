# Please leave this credit if using code below. DO NOT REMOVE COMMENTS
# Authored: Rick Tesmond. https://github.com/tesmonrd/Hard-Onset-Tracker

import pyaudio
import copy
import numpy
import time
import sys


class LiveAudioSession:
    """Class to handle all audio creation."""

    def __init__(self, listen_time=2, baseline=None, analysis=False):
        self.is_terminal_executed = False
        self.audio_session = pyaudio.PyAudio()
        self.listen_time = time.time() + listen_time
        self.input = None
        self.output = None
        self.buffer_size = None
        self.stream = None
        self.isAnalysis = analysis
        self.baseline = baseline
        self.graph = ''
        self.fft_stream_data = []

    def clone(self):
        """Helper method for deepcopy."""
        return copy.deepcopy(self)

    def start_session(self):
        """Initializes the live audio session."""
        self.get_audio_input_output_loc()
        rate = int(self.input['defaultSampleRate'])
        self.buffer_size = int(rate * 0.02)
        self.stream = self.audio_session.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            input_device_index=self.input['index'],
            frames_per_buffer=self.buffer_size)
        return self

    def exit_session(self):
        """Closes session."""
        self.stream.close()
        self.audio_session.terminate()

    def get_audio_input_output_loc(self):
        """Detects the audio devices specified in audio_sessions."""
        try:
            self.input = self.audio_session.get_default_input_device_info()
            self.output = self.audio_session.get_default_output_device_info()
        except Exception as e:
            print("{}. No Audio Input Found".format(e))

    def listen(self):
        """Listen to input and log."""
        try:
            width = 79
            block_string = self.stream.read(self.buffer_size, exception_on_overflow=False)
            block = numpy.frombuffer(block_string, dtype=numpy.int16) / 32768.0
            nbands = 30 * width
            fft = abs(numpy.fft.fft(block, n=nbands))
            if self.isAnalysis:
                self.visualize_data(fft)
            self.fft_stream_data.append(int(max(fft)))
            sys.stdout.flush()
            return int(max(fft))
        except Exception as e:
            print("Exception encountered during listening session: {}".format(e))

    def visualize_data(self, data):
        """Data visualizer. Checks execution method."""
        peak = max(data)/10
        if self.is_terminal_executed:
            if self.baseline and max(data) > int(float(self.baseline)) + 1:
                bars = "\033[91m" + ("#" * int(20 * peak)) + "\033[91m"
            else:
                bars = "\033[92m" + ("#" * int(20 * peak)) + "\033[92m"
            print("{} - {}".format(int(max(data)), bars))

        else:
            if self.baseline and max(data) > int(float(self.baseline)) + 1:
                bars = "<span style='color:red'>" + ("#" * int(20 * peak)) + "</span></br>"
            else:
                bars = "<span style='color:green'>" + ("#" * int(20 * peak)) + "</span></br>"
        self.graph += "{} - {}".format(int(max(data)),bars)


class StreamAnalysis:
    """Class defining our hard-onset analysis."""
    def __init__(self, stream_obj, baseline_fft=None):
        self.stream_obj = stream_obj
        self.baseline_fft = baseline_fft
        self.last_fft = None
        self.marked_h_onsets = 0

    def process_average_ftt(self):
        """Calculates the average ftt."""
        cleaned_max_vals = [i for i in self.stream_obj.fft_stream_data if i > 1]
        self.baseline_fft = int(sum(cleaned_max_vals)/len(cleaned_max_vals))

    def listen_hard_onsets(self):
        """Detects and logs hard onsets by comparing ftt data."""
        _cur_fft = self.stream_obj.listen()
        if not self.last_fft:
            self.last_fft = _cur_fft

        if _cur_fft > int(self.baseline_fft):
            if self.last_fft < int(self.baseline_fft):
                self.marked_h_onsets += 1
        self.last_fft = _cur_fft


if __name__ == "__main__":
    # Set variables passed through cmdline
    duration = 5
    speech_effort = 45
    if len(sys.argv) == 2:
        duration = int(sys.argv[-1])
    if len(sys.argv) == 3:
        duration = int(sys.argv[-2])
        speech_effort = int(sys.argv[-1])
    # Initialize Session
    s = LiveAudioSession(duration, speech_effort, True).clone()
    s.is_terminal_executed = True
    stats = StreamAnalysis(s, speech_effort)

    s.start_session()
    while time.time() < s.listen_time:
        stats.listen_hard_onsets()
    s.exit_session()
    stats.process_average_ftt()
    print("H-Onsets: {}".format(stats.marked_h_onsets))
