from flask import Flask, jsonify
from flask_restful import Resource, Api
import requests
import credentials
import json

app = Flask(__name__)
api = Api(app)

class YoutubeVideoQuery(Resource):

    def get(self, keywords):
        params = {"q": keywords,
                  "part": "snippet",
                  "type": "video",
                  "key": credentials.YOUTUBE_API_KEY}
        url = "https://www.googleapis.com/youtube/v3/search"
        videoQuery = requests.get(url=url, params=params)
        videos = videoQuery.json()['items']
        videoIds = {}
        if len(videos) > 4:
            for i in range(4):
                vidId = videos[i]['id']['videoId']
                videoIds[vidId] = videos[i]['snippet']['title']
        else:
            for vd in videos:
                vidId = vd['id']['videoId']
                videoIds[vidId] = vd['snippet']['title']
        return videoIds


api.add_resource(YoutubeVideoQuery, '/videos/<keywords>')

if __name__ == '__main__':
    app.run(port=6000)

