## Deliverable #3 (Pattern Discovery)

## **Cluster hooks by similar patterns (question-based, dramatic statement, etc.)**
1. Features per Video = [text_embeddings, mean_intensity, intensity_variance, speech_rate, pitch_variance, cut_count, overlay_text, cut_freq]
2. Text embeddings are extracted based on first N words (**N=20**) from the transcript using the sentence-transformer model.
3. Determine the best K for K-means with Silhouette score and K plot. Chosen K is the one, where Silhouette is maximum. Plot attached as **Choosing_K.png** - [code](https://github.com/prakhar21/Hook-Pattern-Detection/blob/main/3_Pattern_Discovery/1_cluster.py)
4. **Best K determined = 5** Refer **video_clustering.json** for cluster centre and elements.
5. Each cluster elements list (containing first 20 words from transcript of these videos) is passed to GPT-5 to generate Hook type from list of predefined hooks - [code](https://github.com/prakhar21/Hook-Pattern-Detection/blob/main/3_Pattern_Discovery/2_cluster_headers.py)


Generating Header for Cluster #4 - **"Shock Value / Clickbait"**

["How much money do you make? Make $1 million every month. And how old are you? I'm 17. This is", "As a 20 year old man, zero home, AIMM, A podcast, Unnekebad, whatever I'm doing, a mooji fun. Five levels", "Chatchie can take, it's going to potentially embrace your risk of dimension. I'm sorry, but you've pressed my button and", 'Welcome to TED. Thank you so much for coming. Thank you, Saunter. Your company has been releasing crazy and sane', 'They call you the Godfather of AI. So what would you be saying to people about their career prospects in', "I got a crazy AI story. This guy. He's being interviewed. He basically went into Chachi BT. He got super", 'I asked Chachi RpD, what is currently the theory of creation? Big Bang went back. What caused the Big Bang?']



Generating Header for Cluster #1 - **"Curiosity / Mystery"**

["The Jerogan experience. So this is logical. And the problem is, like I said, when I've talked to Mark and", "This mission is too important for me to allow you to jeopardize it. I don't know what you're talking about,", "OK, class, phones away, phones away. But Ms. Raunman, it's my calculator. I can see from here that you're playing", "You got really two choices. You can either be a spectator or a participant. We're talking about an economy that", 'May Rajo flatmate, he is a software developer. Or Japsi, AI-ka, katra-y, AI-ka. Pah-gal-gal-ga. Pah-gal-ga, pah-gal-ga. Pah-gal-ga, pah-gal-ga, pah-gal-ga, pah-gal-ga.', "It's the biggest trend of the world right now and I can't help myself hear the five best baby AIs", "I don't normally do this, but I feel like I have to start this podcast with a bit of a", "Eric Schmidt, thank you for joining us. Thank you. Let's go back. You said the arrival of non-human intelligence is", "Look, you've spent so much of your life explaining science to people. Yes. Basically being a human well actually meme.", "Sometimes I have been I hear, he Le activist and turned strong so I'm crazy. I hear, we moved to", "Please welcome Andrew In. APPLAUSE Thank you. It's such a good time to be a builder. So I'm excited to", 'I just wanted to express their foreign habits over the first time, everything with hard work and wide But they', "because AI is pretty fascinating in AI. And I've been asking AI some questions to ask me. Obviously, there's no", "Web of you have told me about so many air tools which are the top three air tools that you'd", 'Most people around the world are still not aware of what is happening on the AI front. It can invent']



Generating Header for Cluster #2 - **"Personal Story"**

["The general going to experience it a perfect world though. If there is this, these race dynamics that we're discussing", "The Jerogan experience. And wondering what the potential for the future is, whether or not that's a good thing. I", 'I had that weird conversation with chat GPT. I said rule number one, only respond with one word. Rule number', "There is actually a really good reason why you should say please and thank you to your chatbots And it's", 'I went to school with a lot of the people that now build these technologies. I went to school with', "MUSIC Stargate put that name down in your books because I think you're going to hear a lot about it", 'You may not take interest in politics, but politics will take interest in you. So the same applies to AI']



Generating Header for Cluster #0 -  **"Expert Authority"** 

["This is like a crazy amount of power for one piece of technology, and it's happened to us so fast.", "I want to tell you what I see coming. I've been lucky enough to be working on AI for almost", "You've been working on AI safety for two decades at least. Yeah. I was convinced we can make safe AI,", "At some point, you have to believe something. We've reinvented computing this, we know it. What is the vision for", "Last week, I spent five hours and $49 to complete Google's latest AI essentials course for beginners. And since I", "I'd love to start with these 10 years of work right there. Someone on your team called these the real-life", "Despite what you hear about artificial intelligence, machines still can't think like a human. But in the last few years,", "These gummies say 3,000 milligrams, but I ain't no bitch. Gotta keep the grand in the flesh. HOA been on", "Each and any opportunities in the Hindi world. That's a Instability We Will The rebellion in the future of rituals"]



Generating Header for Cluster #3 -  **"Expert Authority"**

["Hello, I'm Caroline Steele. This is the BBC World Service and welcome to the engineers. This year we're at the", "Artificial intelligence or AI, it has been pitched as capitalism's new golden goos, generative AI, we're supposed to root all,", "So, I'm going to explain what artificial intelligence is and I want this to be a bit interactive"]


## **Identify statistical correlations between hook elements and success** - [code](https://github.com/prakhar21/Hook-Pattern-Detection/blob/main/3_Pattern_Discovery/3_hookelements_success.py)
* Correlation matrix is saved in __corr.png__
* Correlation is calculated between hook elements and life time views (proxy to succcess)

