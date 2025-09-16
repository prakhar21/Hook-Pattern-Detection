import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-mpnet-base-v2")


### FEATURE LOADING
audio_features = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/audio_features.json', 'r').read())
visual_features = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/visual_features.json', 'r').read())
textual_features = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/audio_transcription.json', 'r').read())
successful_videos = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/successful_videos.json','r').read())

features = []
video_ids = list(audio_features.keys())
for video_id in video_ids:
    ## audio features
    mean_intensity, intensity_variance, speech_rate, pitch_variance = audio_features[video_id]['intensity']['mean'], audio_features[video_id]['intensity']['variance'], \
                                        audio_features[video_id]['speech_rate'], audio_features[video_id]['pitch_var']
                                        
    ## visual features
    cut_count, overlay_text, cut_freq = visual_features[video_id]['cuts']['total_cuts'], \
                    1 if len(visual_features[video_id]['text_overlays']['overlay_details']) else 0, \
                    visual_features[video_id]['cuts']['cut_freq']
                    
    ## transcription features
    text = ' '.join(textual_features[video_id]['text'].split()[:20])
    text_features_sum = np.sum(model.encode([text]).tolist()[0])
    text_features_avg = np.mean(model.encode([text]).tolist()[0])
                    
    views = successful_videos[video_id]['view_cnt']
    features.append([mean_intensity, intensity_variance, speech_rate, pitch_variance, cut_count, overlay_text, cut_freq, text_features_sum, text_features_avg, views])
                    
df = pd.DataFrame(features, columns=['mean_intensity', 'intensity_variance', 'speech_rate', 'pitch_variance', 'cut_count', 'overlay_text', 'cut_freq', 'text_features_sum', 'text_features_avg','views'])

"""
corrs_spearman = df.corr(method="spearman")
corrs_with_views = corrs_spearman["views"].drop("views").reset_index()
corrs_with_views.columns = ["feature", "correlation"]
corrs_with_views["abs_corr"] = corrs_with_views["correlation"].abs()
corrs_with_views = corrs_with_views.sort_values("abs_corr", ascending=False)
print(corrs_with_views)
"""

## CORRELATION MATRIX
corr_spearman = df.corr(method="spearman")
sns.heatmap(corr_spearman, annot=True, fmt=".2f", cmap="coolwarm",
            cbar=True, square=True)

plt.tight_layout()
plt.show()
