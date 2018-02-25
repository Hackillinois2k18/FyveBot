from flask import Flask
from flask_restful import Resource, Api
from BotService import BotService
import requests

app = Flask(__name__)
api = Api(app)

class BotClient(Resource):

    def get(self, content, query):
        botService = BotService()
        if content == 'video':
            jsonResp = botService.queryYoutubeVideos(query)
        else:
            jsonResp = botService.getSummariesForArticles(query)
        url = "bot_url"
        requests.post(url=url, data=jsonResp)


api.add_resource(BotClient, '/fyve-bot/<content>/<query>')

if __name__ == '__main__':
    app.run(port=5000)

