from flask_restful import Resource
import requests
import credentials

class YoutubeVideoQuery(Resource):

    def get(self, keywords):
        params = {"q": keywords,
                  "part": "snippet",
                  "type": "video",
                  "key": credentials.YOUTUBE_API_KEY}
        url = "https://www.googleapis.com/youtube/v3/search"
        videoQuery = requests.get(url=url, params=params)
        videoTitles = {}
        videoDisplays = {}
        if videoQuery.json()['items']:
            videos = videoQuery.json()['items']
            if len(videos) > 4:
                for i in range(4):
                    vidId = videos[i]['id']['videoId']
                    videoTitles[vidId] = videos[i]['snippet']['title']
                    try:
                        videoDisplays[vidId] = videos[i]['snippet']['thumbnails']['default']['url']
                    except KeyError:
                        videoDisplays[vidId] = ""
            else:
                for vd in videos:
                    vidId = vd['id']['videoId']
                    videoTitles[vidId] = vd['snippet']['title']
                    try:
                        videoDisplays[vidId] = vd['snippet']['thumbnails']['default']['url']
                    except KeyError:
                        videoDisplays[vidId] = ""
        return videoTitles, videoDisplays


