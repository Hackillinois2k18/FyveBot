from flask import Flask, jsonify
from flask_restful import Resource, Api
import requests
import credentials
import json

app = Flask(__name__)
api = Api(app)


class ArticleTopicQueryNews(Resource):
    def get(self, keyword):
        articleUrls = {}
        auth = {"Ocp-Apim-Subscription-Key": credentials.BING_CLIENT_API_KEY}
        url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search?q={}&count=2&offset=0&mkt=en-us".format(keyword)
        jsonData = requests.get(url=url, headers=auth)
        articles = jsonData.json()['value']
        for art in articles:
            articleUrls[art['name']] = art['url']
        return articleUrls

class ArticleTopicQuerySearch(Resource):
    def get(self, keyword):
        articleUrls = {}
        auth = {"Ocp-Apim-Subscription-Key": credentials.BING_CLIENT_API_KEY}
        url = "https://api.cognitive.microsoft.com/bing/v7.0/search?q={}&count=3&offset=0&mkt=en-us".format(keyword)
        jsonData = requests.get(url=url, headers=auth)
        articles = jsonData.json()['entities']['value']
        for art in articles:
            articleUrls[art['name']] = art['url']
        return articleUrls



api.add_resource(ArticleTopicQueryNews, '/articles/<keyword>')

if __name__ == '__main__':
    app.run(port=5000)
