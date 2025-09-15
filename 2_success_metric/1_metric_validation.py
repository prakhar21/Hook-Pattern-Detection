import glob
import os
import json
import pandas as pd

## STEP 1: Metric Formulation and Calculation
successful_videos = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/successful_videos.json','r').read())
analysis_videos = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/audio_features.json','r').read())

video_ids = list(analysis_videos.keys())
w1, w2 = 0.2, 0.8

hook_effectiveness = {}
for vid_id in video_ids:
    metadata = successful_videos[vid_id]
    like, comment, view, duration = \
        metadata['like_cnt'], metadata['comment_cnt'], metadata['view_cnt'], \
        metadata['duration_sec']
        
    vv = round(view / duration, 4)
    wer = round((w1 * like + w2 * comment) / view, 4)
    he = round(wer * vv * 100, 4)
    hook_effectiveness[vid_id] = {'like':like, 'comment':comment , 'view':view, \
                                  'duration': duration, 'he': he
                                  }

json.dump(hook_effectiveness, open('hook_effectiveness.json', 'w'), indent=4)

## STEP 2: Metric Correlation
df = pd.DataFrame(hook_effectiveness).T
df.index.name = "video_id"

# Correlation between views and he
correlation1 = df["view"].corr(df["he"], method='spearman')
print("Correlation (views vs he):", correlation1)

