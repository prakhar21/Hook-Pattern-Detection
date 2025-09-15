import os
import json
import re
import subprocess

try:
    from pytubefix import YouTube
    from pytubefix.cli import on_progress
except ImportError:
    print("Missing 'pytubefix'. Please install...\n")
    raise ("pip install pytubefix-9.5.0")

try:
    from googleapiclient.discovery import build
except ImportError:
    print ("Missing 'google-api-python-client'. Please install...\n")
    raise ("pip install google-api-python-client==2.181.0")

try:
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
except ImportError:
    print ("Missing 'moviepy'. Please install...\n")
    raise ("pip install moviepy==2.2.1")


class YTDownloader:
    def __init__(self, query:str, api_key:str, video_count:int):
        self.yt_api_key = api_key
        self.search_query = query
        self.yt_svc = build("youtube", "v3", developerKey=self.yt_api_key)
        self.video_count = video_count
        self.successful_video_view_cnt = 1000000

    
    def search_youtube(self) -> dict:
        """
        Fetches for Youtube Videos and their Titles for a given User Query.
        Search happens for US region, with Pagination to traverse required 
        video count.
        """

        video_details = {}
        videos_fetched = 0
        next_page_token = None
        try:
            while videos_fetched < self.video_count:
                search_response = self.yt_svc.search().list(
                    q=self.search_query,
                    part="snippet",
                    maxResults=self.video_count,
                    pageToken=next_page_token,
                    type="video",
                    relevanceLanguage="en",
                    regionCode="US",
                    order="viewCount"
                ).execute()
                
                next_page_token = search_response.get('nextPageToken', None)
                videos_fetched += search_response.get("pageInfo").get("resultsPerPage")
                print (f'Total videos fetched till now : {videos_fetched}')
                
                for item in search_response['items']:
                    video_details[item['id']['videoId']] = {
                                                            'title':item['snippet']['title']
                                                        } 
            return video_details
        except Exception as e:
            print (f"Failed to search on YT - {e}")
        
        
    def filter_only_successful_videos(self, video_details:dict) -> dict:
        """
        Filters for videos that have more than 1M views. View count is a proxy
        to a successful video.
        """
        successful_videos = {}
        for k, v in video_details.items():
            if int(v['view_cnt']) >= self.successful_video_view_cnt:
                successful_videos[k] = v
        print (f'Found {len(successful_videos)} videos with >= 1M views')
        return successful_videos
    
    
    def download_video(self, successful_videos:dict) -> None:
        print (f'Total successful videos: {len(successful_videos)}')
        print ('\n\nStarting to Download Video...')
        for k, _ in successful_videos.items():
            video_url = f'https://www.youtube.com/watch?v={k}'
            try:
                yt = YouTube(video_url, on_progress_callback=on_progress)
                if yt.length > 60 and yt.length <= 7200: #exclude shorts and content>=2hr
                    stream = yt.streams.filter(file_extension="mp4", progressive=True)
    
                    for idx,i in enumerate(stream):
                       if i.resolution=='480p':
                          break
                    yt.streams[idx].download(f'data/videos_full_length/{k}')
                    ## save video in videos/ folder
                    print (f'Downloaded {k}')
                        
                    ## trim and extract first 30 sec of the saved video
                    inp_f = f'data/videos_full_length/{k}/'
                    files = os.listdir(inp_f)
                    
                    ffmpeg_extract_subclip(
                                            os.path.join(inp_f, files[0]), 
                                            "00:00:00", 
                                            "00:00:30", 
                                            f'data/videos_30sec/videos/{k}_30sec.mp4'
                    )
                    #os.remove(os.path.join(inp_f, files[0]))
                
            except Exception as e:
                print(f"An error occurred: {e}")
        print("All videos downloaded successfully!")
    
    def _iso8601_duration_to_seconds(self, duration:str):
        """
        Converts an ISO 8601 duration string (e.g., 'PT1H2M30S') to seconds.
        """
        pattern = re.compile(
            r'P'              # starts with 'P'
            r'(?:(\d+)D)?'    # days
            r'T'              # time part starts with 'T'
            r'(?:(\d+)H)?'    # hours
            r'(?:(\d+)M)?'    # minutes
            r'(?:(\d+)S)?'    # seconds
        )
        match = pattern.fullmatch(duration)
        if not match:
            return 0
        days, hours, minutes, seconds = match.groups()
        total_seconds = (
            int(days or 0) * 86400 +
            int(hours or 0) * 3600 +
            int(minutes or 0) * 60 +
            int(seconds or 0)
        )
        return total_seconds
    
    def get_video_metadata(self, video_details:dict) -> dict:
        counter = 0
        for k, v in video_details.items():
            try:
                response = self.yt_svc.videos().list(
                            part="statistics, contentDetails",
                            id=k
                        ).execute()
            except:
                print (f'Failed to pull meta-data for : {k}-{v}')
                response = {}
                
            video_data = response['items'][0] if response["items"] else None
            if video_data:
                view_cnt = int(video_data["statistics"].get("viewCount", 0))
                like_cnt = int(video_data["statistics"].get("likeCount", 0))
                comment_cnt = int(video_data["statistics"].get("commentCount", 0))
                duration_iso = video_data['contentDetails'].get('duration', 0)
                if duration_iso:
                    duration_sec = self._iso8601_duration_to_seconds(duration_iso)
                else:
                    duration_sec = 0
            else:
                view_cnt, like_cnt, comment_cnt, duration_sec = 0, 0, 0, 0
                        
            video_details[k]['view_cnt'] = view_cnt
            video_details[k]['like_cnt'] = like_cnt
            video_details[k]['comment_cnt'] = comment_cnt
            video_details[k]['like_per_view'] = round(like_cnt/view_cnt,4) if view_cnt else 0
            video_details[k]['comment_per_view'] = round(comment_cnt/view_cnt,4) if view_cnt else 0
            video_details[k]['duration_sec'] = round(duration_sec,4) if duration_sec else 0
            
            
            counter += 1
            if counter % 50 == 0:
                print (f'Meta-data fetch for {counter} videos is complete!')
        
        return video_details
            
    

api_key = "AIzaSyCf6Vq6BBpx_BRldyjfro90vlvXtAmTVyU"
query = "business podcasts"
video_count = 1000

yt_downloader = YTDownloader(
                            query=query, 
                            api_key=api_key, 
                            video_count=video_count
                )

#STEP 1 :: Search for list of videos for a given keyword
yt_search_result = yt_downloader.search_youtube() 

#STEP 2 :: Extract meta-data for the videos extracted from prev. step
yt_search_result_w_metadata = yt_downloader.get_video_metadata(yt_search_result)

#STEP 3 :: Filter only videos >=1M views
successful_videos = yt_downloader.filter_only_successful_videos(yt_search_result_w_metadata)
json.dump(successful_videos, open('data/videos_30sec/successful_videos.json', 'w'), indent=4)

#STEP 4 :: Download successful videos in a folder and save meta-data details in JSON
yt_downloader.download_video(successful_videos)




