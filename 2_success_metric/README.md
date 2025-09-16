## Success Metric Definition
### **View Velocity**
```
View_Velocity (vv) = views/duration
```
* Duration of the video is the runtime of the video (in sec)
* Higher velocity (vv) suggests that viewers are watching more in a shorter period, suggesting the start is engaging.

### **Weighted Engagement Ratio**
```
Weighted_Engagement_Ratio (wer) = w1 * (Likes/Views) + w2 * (Comments/Views)
```
Here, w2 > w1, because;
* Likes are easy, low-effort actions. They show approval but not very strong.
* Comments take more effort — typing thoughts, or asking questions.
* Comments are considered 3–5x stronger signals of engagement compared to Likes. 
Hence, we are setting **w1=0.2, w2=0.8** as our heuristic choice. (w1+w2 = 1)

### Normalize by Video Age
```
Video_age_in_days (va) = Today_Date - Video_Published_Date
```
* Multiplying the factor of (1/va) to the Hook Effectiveness Formula. Videos accumulate views and engagement over time. Comparing a videos that's been live for 2 days vs the one for 30 days can skew the metrics.
  
### **Hook effectiveness using Engagement Proxies**
```
Hook_Effectiveness (he) = Weighted_Engagement_Ratio * View_Velocity * 1/Video_age_in_days) * 100
```

**Possible improvements in the above Formulation**
* It would have been interesting to add Views in first K hours.
* Retention % in the first 30 seconds.
* It would be beneficial to add Share/Views as part of Weighted_Engagement_Ratio. It is a much stronger signal than Like/Views and almost similar or better than Comment/Views. Unfortunately, share stats are not openly available as part of Data API.
* The above formulation discounts the Channel / Topic bias. Bigger channela and Trending topics is likely to inflate the engagement regardless of the Hook quality.

 ## Defining Overall Video Performance
 * We treat Lifetime views of the video as proxy for Video Performance.
 
**Other potential factors include**
* Total watch time for the video.
* Subscriber growth from particular video.
* Average view duration.
