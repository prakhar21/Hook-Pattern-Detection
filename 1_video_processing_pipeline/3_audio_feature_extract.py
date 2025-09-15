try:
    import os
    import librosa
    import numpy as np
    import glob
    import json
except ImportError:
    print ("Missing 'librosa'. Please install...\n")
    raise ("pip install librosa==0.11.0")


def convert(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    raise TypeError
    
    
class AudioFeatures:
    
    def __init__(self, audio_file_path:str):
        self.audio_files = glob.glob(os.path.join(audio_file_path,'*'))
    
    
    def detect_music_presence(self, y, sr, threshold=0.2):    
        """Detects the presence of background music in the video"""
        # Harmonic-percussive source separation
        y_harmonic, y_percussive = librosa.effects.hpss(y)
    
        # Compute spectral flatness (measure of noise-like vs tone-like)
        flatness = librosa.feature.spectral_flatness(y=y_harmonic)
        mean_flatness = np.mean(flatness)
    
        # If harmonic + flatness is strong, it's likely music
        music_score = np.mean(np.abs(y_harmonic)) * (1 - mean_flatness)
    
        return 1 if music_score > threshold else 0
    
    
    def extract_audio_features(self):
        """
        Extracts the features from audio (.wav) such as energy, speech rate.
        """
        audio_features = {}
        for idx, file in enumerate(self.audio_files):
            f_name = file.split('/')[-1].split('.')[0].replace('_30sec','')
            y, sr = librosa.load(file, sr=16000)
            
            # FEATURE 1: Frame-wise RMS energy/intensity
            rms = librosa.feature.rms(y=y)[0]
            audio_features[f_name] = {"intensity":{"mean": round(float(np.mean(rms)), 4), 
                                                    "max": round(float(np.max(rms)), 4), 
                                                    "min": round(float(np.min(rms)), 4),
                                                    "variance": round(float(np.std(rms), 4))
                                                }
                                     }

            # FEATURE 2: Speech Rate (words / min)
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
            audio_features[f_name]["speech_rate"] = round(float(tempo[0]), 4)
            
            # FEATURE 3: Pitch Variance
            f0 = librosa.yin(y, fmin=50, fmax=300, sr=sr)
            audio_features[f_name]["pitch_var"] = round(float(np.std(f0)))

            #music_found = self.detect_music_presence(y, sr)
            #audio_features[f_name]["music_present"] = round(float(music_found), 4)
            #print (audio_features)

            if idx%5==0 and idx!=0:
                print (f'Audio feature extraction completed for {idx} samples')
            
        return audio_features

    
audio_file_path = "data/videos_30sec/audios"

af = AudioFeatures(audio_file_path=audio_file_path)
af_set = af.extract_audio_features()
json.dump(af_set, open('data/videos_30sec/audio_features.json', 'w'), indent=4, default=convert)


