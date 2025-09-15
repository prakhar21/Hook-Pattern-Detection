# [Analysing Youtube Podcast Hooks](https://docs.google.com/document/d/1XlqZfPvA3VO_mFgSoBKqOb-UdTC29Cg5g62UtHNj1TQ/edit?tab=t.0)
_Analyze the first 30 seconds of successful videos to identify hook patterns that drive retention_
- Successful video has following attributes ; >=1M views AND duration >60 sec & <=7200 sec (2hr). 

#### Deliverable #1 (Video Processing Pipeline)
 - **Download and extract first 30 seconds from 200+ podcast videos** - [code](https://github.com/prakhar21/Hook-Pattern-Detection/blob/main/1_video_processing_pipeline/1_pull_yt_videos.py)
    1. Used YT Data v3 API to fetch the videos based on keyword, language, region, views, and more. The API returns maximum 50 response in 1 API pull, leveraged pagination to iterate through the pages.
    2. First 30 seconds of videos along with their meta-data for videos with more than 1M views that are greater than 60 sec and less then 2 hr duration are dowloaded using Moviepy. 
 - **Generate transcripts using Whisper or similar** - [code](https://github.com/prakhar21/Hook-Pattern-Detection/blob/main/1_video_processing_pipeline/2_speech_to_text.py)
    1. Used Whisper tiny.en model to transcribe the audio of each 30 sec video clips
 - **Measure audio features: energy levels, speaking pace, music presence** - [code](https://github.com/prakhar21/Hook-Pattern-Detection/blob/main/1_video_processing_pipeline/3_audio_feature_extract.py)
    1. Extracted Intensity/Energy per frame of the video using librosa. Aggregated over frames to get min, max, avg, variance of the intesity in the video. **[ Intuition : higher energy variance = more engaging ]**
    2. Extracted Speech Rate (words / min) using librosa. *It can also be calculated using the count of words in transcript over duration of the video (in sec).* **[ Intuition : higher speech rate = need for better articulation ]**
    3. Extracted Pitch Variance **[ Intuition : Flat pitch = Monotone. Variability = Gngaging ]**
    4. Tried extracting presence of music in the video using librosa [Line 68-Line 69](https://github.com/prakhar21/Hook-Pattern-Detection/blob/main/1_video_processing_pipeline/3_audio_feature_extract.py#L68C13-L69C84) but didn't seem to work correctly.
 - **Extract visual features: cut frequency, zoom patterns, text overlays** - [code](https://github.com/prakhar21/Hook-Pattern-Detection/blob/main/1_video_processing_pipeline/4_visual_features_extract.py)
    1. Extracted the total number of scene cuts in the entire 30 sec of the video. Also the cut frequency. **[ Intuition : Higher cut Freq = Fast-paced, Dynamic ]**
    2. Extracted the % of overlayed text in the video. **[ Intuition : More text overlays = Clear potential messaging for retention, but too much can be distracting ]**
    3. Apply 2 level of grouping on the extracted text 1> group by time 2> group by text.

__Possible Enhancements that could have been done in Deliverable #1__
    1. The extracted engagement measures are just proxies. There are more stronger signals like avg. view duration %, drop rate in first N seconds, and more that are private to creators and are available via Analytics API.
    2. More visual features such as visual loudness by analysing brightness/scene intensity could also be beneficial.
    3. Analysing close-up vs wide shot based on Face detection bounding box ratio.
    4. Analysing Face expressiveness with markers like nodding, hand gestures, and smiles can be a really good feature of engaging video.
    5. Understanding Signal-to-noise ratio. Low SNR makes it hard to listen.


