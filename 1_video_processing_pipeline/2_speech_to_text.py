import os
import glob
import json

try:
    import moviepy.editor as mp
except ImportError:
    print ("Missing 'moviepy'. Please install...\n")
    raise ("pip install moviepy==1.0.3")
    
try:
    import whisper
except ImportError:
    print ("Missing 'whisper'. Please install...\n")
    raise ("pip install openai-whisper")
    

class SpeechToText:
    def __init__(self, video_path:str):
        self.model_path = os.path.join(os.getcwd(), "models/whisper_tiny")
        self.model = whisper.load_model("tiny.en", download_root=self.model_path)
        print ('Whisper model loaded successfuly!')
        self.video_path = video_path
        self.video_files = glob.glob(os.path.join(video_path,'*'))
        print (self.video_files)
    
    
    def extract_audio(self, audio_output_path:str) -> None:
        """
        Processess all the 30sec video files  and extracts their .wav
        """
        for idx, video in enumerate(self.video_files):
            video_name = video.split('/')[-1].split('.')[0]
            video_ = mp.VideoFileClip(video)
            video_.audio.write_audiofile(
                                    f'{audio_output_path}/{video_name}.wav', 
                                    codec='pcm_s16le'
            )
            
            if idx%5==0:
                print (f'Audio extraction complete for {idx} records!')
        return
    
    
    def speech_to_text(self, audio_output_path:str) -> dict:
        """
        Takes path to all the .wav (audio) files and outputs a Dict with 
        its transcription using openai whisper tiny.en model
        """
        audio_transcription = {}
        for idx, file in enumerate(glob.glob(audio_output_path+'/*')): 
            result = self.model.transcribe(file)
            fname = file.split('/')[-1].split('_30sec')[0]
            audio_transcription[fname] = result
            
            if idx%5==0 and idx!=0:
                print (f'Transcription complete for {idx} records!')
                
        return audio_transcription
        

video_path = "data/videos_30sec/videos"
audio_output_path = "data/videos_30sec/audios"

s2t = SpeechToText(video_path)
s2t.extract_audio(audio_output_path)
audio_transcription = s2t.speech_to_text(audio_output_path)
json.dump(audio_transcription, open('data/videos_30sec/audio_transcription.json', 'w'), indent=4)

