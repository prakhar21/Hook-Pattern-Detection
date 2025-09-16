### Deliverable #3 (Pattern Discovery)

**Cluster hooks by similar patterns (question-based, dramatic statement, etc.)**
1. Features per Video = [text_embeddings, mean_intensity, intensity_variance, speech_rate, pitch_variance, cut_count, overlay_text, cut_freq]
2. Text embeddings are extracted based on first N words (**N=20**) from the transcript using the sentence-transformer model.
3. Determine the best K for K-means with Silhouette score and K plot. Chosen K is the one, where Silhouette is maximum. Plot attached as **Choosing_K.png**
4. **Best K determined = 5** Refer **video_clustering.json** for cluster centre and elements.
