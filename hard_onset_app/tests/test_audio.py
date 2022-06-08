from .raw_input import RAW_BASE, RAW_STREAM
from ..audio_processor import LiveAudioSession, StreamAnalysis
import time

rb = RAW_BASE
rs = RAW_STREAM


def test_proto_clone():
    clone = LiveAudioSession().clone()
    assert type(clone) == LiveAudioSession


def test_audio_device():
    c = LiveAudioSession()
    c.get_audio_input_output_loc()
    assert c.input['defaultSampleRate']
    assert c.output['defaultHighInputLatency']


def test_setup_stream():
    c = LiveAudioSession()
    c.start_session()
    c.exit_session()
    assert c.stream
    assert c.buffer_size


def test_stream_listen():
    c = LiveAudioSession()
    c.start_session()
    while time.time() < c.listen_time:
        c.listen()
    c.exit_session()
    assert c.fft_stream_data


def test_fft_average():
    c = LiveAudioSession()
    c.fft_stream_data = rb
    stats = StreamAnalysis(c)
    stats.process_average_ftt()
    assert stats.baseline_fft == 79

def test_hard_onset_track():
    """Had to modify logic because listen_hard_onsets has listen() embedded"""
    c = LiveAudioSession()
    st = StreamAnalysis(c, 79)
    for au_input in rs:
        if not st.last_fft:
            st.last_fft = au_input
        if au_input > int(st.baseline_fft):
            if st.last_fft < int(st.baseline_fft):
                st.marked_h_onsets += 1
        st.last_fft = au_input
    assert st.marked_h_onsets == 14
