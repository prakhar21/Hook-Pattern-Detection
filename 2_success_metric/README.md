## Success Metric Definition
### **View Velocity**
```
View_Velocity (vv) = views/duration
```
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

### **Hook effectiveness using Engagement Proxies**
```
Hook_Effectiveness (he) = Weighted_Engagement_Ratio * View_Velocity * 100
```
