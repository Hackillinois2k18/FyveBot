from flask import Flask
from flask_restful import Resource, Api
from BotService import BotService
import requests

app = Flask(__name__)
api = Api(app)

class BotClientArticle(Resource):

    def get(self, query):
        botService = BotService()
        jsonResp = botService.getSummariesForArticles(query)
        url = "bot_url"
        requests.post(url=url, data=jsonResp)

class BotClientVideo(Resource):

    def get(self, query):
        botService = BotService()
        jsonResp = botService.getYoutubeVideoSums(query)
        url = "bot_url"
        requests.post(url=url, data=jsonResp)


api.add_resource(BotClientArticle, '/fyve-bot/articles/<query>')
api.add_resource(BotClientVideo, '/fyve-bot/videos/<query>')

if __name__ == '__main__':
    app.run(port=5000)

