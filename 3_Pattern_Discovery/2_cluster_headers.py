import json
try:
    from openai import OpenAI
except ImportError:
    print ("Install openai-1.107.3")
    raise ("pip install openai==1.107.3")

openai_key = """<API KEY>"""
client = OpenAI(api_key=openai_key)

hook_patterns = [
    "Shock Value / Clickbait",
    "Personal Story",
    "Expert Authority",
    "Curiosity / Mystery",
    "Controversial Opinion",
    "Relatable Struggle",
    "Big Claim / Bold Statement",
]


def assign_hook_cluster(cluster_elements):
    prompt = f"""
    We have podcast video hook patterns: {hook_patterns}.
    Given the following cluster elements: "{cluster_elements}"
    Assign the best matching hook (choose ONE from the list).
    Return only the hook pattern name, no explanation.
    """
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are a classification assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()


label_videos_map = json.loads(open('video_clustering.json', 'r').read())
textual_features = json.loads(open('../1_video_processing_pipeline/data/videos_30sec/audio_transcription.json', 'r').read())

header_elements = {}
for k, v in label_videos_map.items():
    print (f'Generating Header for Cluster #{k}')
    text_segs = []
    for i in v:
        text_segs.append(' '.join(textual_features[i]['text'].split()[:20]))
    hook = assign_hook_cluster(text_segs)
    header_elements[i] = hook

json.dump(header_elements, open('hook_names_clusters.json', 'w'), indent=4)
    
