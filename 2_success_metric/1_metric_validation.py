import glob
import os
import json
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


## STEP 1: Metric Formulation and Calculation
successful_videos = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/successful_videos.json','r').read())
analysis_videos = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/audio_features.json','r').read())

video_ids = list(analysis_videos.keys())
w1, w2 = 0.2, 0.8

"""For every video compute the hook effectiveness based on proxy engagement metrics"""
hook_effectiveness = {}
for vid_id in video_ids:
    metadata = successful_videos[vid_id]
    like, comment, view, duration, va = \
        metadata['like_cnt'], metadata['comment_cnt'], metadata['view_cnt'], \
        metadata['duration_sec'], metadata['video_age']
        
    vv = round(view / duration, 4)
    wer = round((w1 * like + w2 * comment) / view, 4)
    he = round(wer * vv * (1/va) * 100, 4)
    hook_effectiveness[vid_id] = {'like':like, 'comment':comment , 'view':view, \
                                  'duration': duration, 'video_age': va, 'he': he
                                  }
        
# storing hook score for analysed videos
json.dump(hook_effectiveness, open('hook_effectiveness.json', 'w'), indent=4)


## STEP 2: Metric Correlation
df = pd.DataFrame(hook_effectiveness).T
df.index.name = "video_id"

scaler = StandardScaler()
scaled = scaler.fit_transform(df)
df_scaled = pd.DataFrame(scaled, columns=df.columns)

sns.regplot(
    x=df_scaled["view"], 
    y=df_scaled["he"], 
    scatter_kws={"alpha":0.6}, 
    line_kws={"color":"red"},
)
plt.xlabel("Views (scaled)")
plt.ylabel("Hook Effectiveness (scaled)")
plt.show()


correlation1 = df_scaled["view"].corr(df_scaled["he"])
print("Correlation (views vs he):", correlation1)
