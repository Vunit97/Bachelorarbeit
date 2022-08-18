import soundfile
import numpy as np
import librosa
import glob
import os
from sklearn.model_selection import train_test_split

# all emotions based on RAVDESS dataset & TORONTO dataset
emotion_set = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised"
}

# Only these emotions allowed
needed_emotions = {
    "happy",
    "sad",
    "angry",
    "neutral"
}

# Feature extraction from a raw wav audio
def extract_feature(input_name, **kwargs):
    mfcc = kwargs.get("mfcc")
    mel = kwargs.get("mel")
    chroma = kwargs.get("chroma")

    with soundfile.SoundFile(input_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            melfcc = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, melfcc))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
    return result

# Load Data and use train-split method
def load_data(test_size=0.25):
    X, y = [], []
    for file in glob.glob("data/Actor_*/*.wav"):
        filename = os.path.basename(file)
        emotion = emotion_set[filename.split("-")[2]]

        if emotion not in needed_emotions:
            continue

        speech_features = extract_feature(file, mfcc=True, mel=True, chroma=True)
        X.append(speech_features)
        y.append(emotion)

    return train_test_split(np.array(X), y, test_size=test_size, random_state=5)
