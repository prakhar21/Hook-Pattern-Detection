try:
    import glob
    import json
    from collections import defaultdict
    import warnings
    warnings.filterwarnings("ignore")
    from scenedetect import VideoManager, SceneManager
    from scenedetect.detectors import ContentDetector
except ImportError:
    print ("Missing 'scenedetect'. Please install...\n")
    raise ("pip install scenedetect==0.6.7")


try:
    import cv2
except ImportError:
    print ("Missing 'opencv-python'. Please install...\n")
    raise ("pip install opencv-python==4.6.0.66")


try:
    import easyocr
except ImportError:
    print ("Missing 'easyocr'. Please install...\n")
    raise ("pip install easyocr-1.7.2")


class VisualFeatures:
    
    def __init__(self, video_path):
        self.video_path = video_path
        self.videos = glob.glob(self.video_path+'/*')
    
    
    def detect_cuts(self, video:str, threshold:float=30.0):
        video_manager = VideoManager([video])
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=threshold))
    
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list()
    
        cuts = [(start.get_seconds(), end.get_seconds()) for start, end in scene_list]
        video_manager.release()
        
        return cuts, len(cuts)
    
    
    def _remove_duplicate_text_overlays(self, text_overlays:list) -> dict:
        # STEP 1 Merge: Merge Common Frame but Different Text
        grouped = defaultdict(list)
        for item in text_overlays:
            grouped[item['frame']].append(item['text'])
        result = [{'frame': frame, 'text': texts} for frame, texts in grouped.items()]
        
        # STEP 2 Merge: Merge Common Text with Different Frame
        grouped = defaultdict(list)

        for item in result:
            key = tuple(item['text'])
            grouped[key].append(item['frame'])
        
        result = [{'frames': frames, 'text': list(text)} for text, frames in grouped.items()]        
        return result

    
    def detect_text_overlays(self,  video:str, sample_rate:int=30) -> dict:
        cap = cv2.VideoCapture(video)
        reader = easyocr.Reader(['en'])
        overlays = []
    
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
    
            if frame_idx % sample_rate == 0:
                results = reader.readtext(frame)
                for (bbox, text, prob) in results:
                    if prob > 0.5:  # confidence filter
                        overlays.append({"frame": frame_idx, "text": text})
            frame_idx += 1
        cap.release()
        text_overlays = self._remove_duplicate_text_overlays(overlays)
        return text_overlays
    
    
    def extract_visual_features(self):
        visual_feat = {}
        for idx, video in enumerate(self.videos):
            f_name = video.split('/')[-1].split('_30sec')[0]
            
            text_overlays = self.detect_text_overlays(video)
            cuts, total_cuts = self.detect_cuts(video)
            
            visual_feat[f_name] = {'cuts': 
                                           {'cut_details': cuts, 'total_cuts': total_cuts},
                                   'text_overlays':
                                           {'overlay_details': text_overlays}
                                }
        return visual_feat
            


video_path = "data/videos_30sec/videos"

vf = VisualFeatures(video_path=video_path)
vf_set=vf.extract_visual_features()
json.dump(vf_set, open('data/videos_30sec/visual_features.json', 'w'), indent=4)
