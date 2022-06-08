# Speech Dysfluency: Hard-Onset Tracker
Authored: Rick Tesmond\
Contact: richard.d.tesmond@vanderbilt.edu



## Overview
This application is developed to help stutterers and people with speech dyslfuency actively practice "easy-onset" speech techniques. By collecting a baseline "speech effort" value, users can analyze live audio using their default audio input devices to see the number of "hard-onsets" occurred during the session, as well as an oscillogram of the session.


Easy-Onset speaking is defined as: “initiating voicing with gentle vibrations; smoothly increasing amplitude level, then decreasing”.
Hard-Onset is the inverse of this, where the vocal cords “overshoot” and contract too tightly at the beginning of speech production, resulting in abrupt amplitude increases.
Along with all accompanying speech fluency techniques (breadth training, articulation, etc.), “Easy-Onset” is one of the most important yet difficult techniques to employ
It requires strict practice and immediate correction. 

Resources: Webster, Ronald L. (2016). _Hollins Fluency System III: High Definition Speech Reconstruction for Stuttering_.



### Technology
Python 3, Flask, PyAudio

The application is built using the Flask framework, and relies on the libraries: PyAudio and Numpy.

Audio input is collected and streamed at the default rate set on the given input device, and the input data is chunked and analyzed multiple times per second. The "speech effort" value is gathered by analyzing live audio using Fast Fourier Transformation (FFT), and extracting the maximum FFT value from the stream.
Hard onsets are calculated by observing the current Fast Fourier Transformation data (FFT) compared to a users given "baseline" effort FFT. If the speech ever differs by an unexpectedly larger FFT, this indicates a Hard-Onset. 


## How to run it
** Ensure you have a Python 3 version installed **
* Navigate to a new project directory
* `git clone` from repo: https://github.com/vu-5278-s21/final-project-tesmonrd.git
* initialize you virtual environment of choice and activate it... i use `python -m venv yourenvname`. 
* load the requirements from requirements.txt using `pip install -r requirements.txt`. 
* load the environment variables from envs/local.env using `source envs/local.env`.
  
#### Executing via Web App (flask)
* Run `flask run` from your command line and you're off! Defaults to run on `localhost:5000`.

#### Executing via Command Line
* This approach gives the most accurate live feedback on your speech.
* Navigate to `hard_onset_app/` directory.
* Run the command `python audio_processor.py`
    * Runs with a default listen duration of 5, and speech effort of 45.
    * Accepts two optional command variables, first for listen duration, and second for speech effort.
        * To configure duration: `python audio_processor.py 10` to listen for 10 seconds.
        * To configure duration and speech effort: `python audio_processor.py 10 35` to listen for 10 seconds and a speech effort of 35.


## Interacting with the Web App
1. First, you will want to find your natural speaking "baseline effort". To do this simply click on the link for `collect baseline`, and follow the instructions.
2. Once the baseline is collected, navigate to the `analyze speech` link. You will need to specify the duration of the session, then press `Start`.

Once a run is completed, you will see the number of Hard Onsets detected over the duration of the session as well as an Ocillogram of the speaking session.
* The returned Ocillogram displays the "speech effort" detected and a visual representation of the calculated speech effort.
    * Green means no Hard Onsets were detected
    * Red means a Hard Onset was detected.

## How to test

Simply run `pytest` from the project's root directory!

## Future Build
* Get the oscillogram to run live in the DOM
* Live counter for hard-onsets
* Improve UI