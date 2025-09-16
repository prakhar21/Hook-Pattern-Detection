import json
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer


### MODEL LOADING
model = SentenceTransformer("all-mpnet-base-v2")


### FEATURE EXTRACTION
audio_features = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/audio_features.json', 'r').read())
visual_features = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/visual_features.json', 'r').read())
textual_features = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/audio_transcription.json', 'r').read())


### LOOPING OVER ALL THE VIDEOS AND CREATING FEATURE VECTOR
video_ids = list(audio_features.keys())
idx_video_id_map = {}
embeddings = []
for idx, video_id in enumerate(video_ids):
    ## audio features
    mean_intensity, intensity_variance, speech_rate, pitch_variance = audio_features[video_id]['intensity']['mean'], audio_features[video_id]['intensity']['variance'], \
                                        audio_features[video_id]['speech_rate'], audio_features[video_id]['pitch_var']
    ## visual features
    cut_count, overlay_text, cut_freq = visual_features[video_id]['cuts']['total_cuts'], \
                    1 if len(visual_features[video_id]['text_overlays']['overlay_details']) else 0, \
                    visual_features[video_id]['cuts']['cut_freq']
    
    ## transcription features
    text = ' '.join(textual_features[video_id]['text'].split()[:20])
    text_features = model.encode([text]).tolist()[0]
    
    ## concatenating all the features
    feat = [mean_intensity, intensity_variance, speech_rate, pitch_variance, cut_count, overlay_text, cut_freq]
    feat.extend(text_features)
    embeddings.append(feat)
    
    idx_video_id_map[idx] = video_id
    
    if idx>0 and idx%10 == 0:
        print (f'Feature extraction complete for {idx} videos!')
    


### CLUSTERING
# DETERMINING BEST K with Silhoutte scores (Best K = Max Silhoutte score)
n_clusters = 10
sil_scores = []
K = range(2, len(video_ids))
embeddings = np.array(embeddings)

for cluster in K:
    kmeans = KMeans(n_clusters=cluster, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)
    score = silhouette_score(embeddings, labels)
    sil_scores.append(score)
    print(f"#Cluster={cluster}, Silhouette score: {score:.3f}")

### PLOT K AND SILHOUTTE SCORES
plt.plot(K, sil_scores, marker='o')
plt.xlabel("Number of clusters k")
plt.ylabel("Silhouette score")
plt.title("Choosing k with silhouette")
plt.show()
best_k = K[np.argmax(sil_scores)]
print("Best k:", best_k)


## RUNNING WITH BEST K DETERMINED ABOVE
print ('Running Clustering with Best identified K')
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
kmeans.fit(embeddings)
labels = kmeans.labels_
label_videos_map = defaultdict(list)
for i, label in enumerate(labels):
    label_videos_map[int(label)].append(idx_video_id_map[i])


## RUNNING CLUSTER EXPLANABILITY
json.dump(label_videos_map, open('video_clustering.json', 'w'), indent=4)

