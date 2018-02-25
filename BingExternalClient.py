from flask_restful import Resource
import requests
import credentials


class ArticleTopicQueryNews(Resource):
    def get(self, keyword):
        articleNames = {}
        articleDisplays = {}
        auth = {"Ocp-Apim-Subscription-Key": credentials.BING_CLIENT_API_KEY}
        url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search?q={}&count=2&offset=0&mkt=en-us".format(keyword)
        jsonData = requests.get(url=url, headers=auth)
        if jsonData.json()['value']:
            articles = jsonData.json()['value']
            for art in articles:
                try:
                    articleNames[art['url']] = art['name']
                except KeyError:
                    articleNames[art['url']] = ""
                try:
                    articleDisplays[art['url']] = art['image']['thumbnail']['contentUrl']
                except KeyError:
                    articleDisplays[art['url']] = ""
        return articleNames, articleDisplays

class ArticleTopicQuerySearch(Resource):
    def get(self, keyword):
        articleNames = {}
        articleDisplays = {}
        auth = {"Ocp-Apim-Subscription-Key": credentials.BING_CLIENT_API_KEY}
        url = "https://api.cognitive.microsoft.com/bing/v7.0/search?q={}&count=3&offset=0&mkt=en-us".format(keyword)
        jsonData = requests.get(url=url, headers=auth)
        if jsonData.json()['webPages']:
            articles = jsonData.json()['webPages']['value']
            for art in articles:
                try:
                    articleNames[art['url']] = art['name']
                except KeyError:
                    articleNames[art['url']] = ""
                try:
                    articleDisplays[art['url']] = art['displayUrl']
                except KeyError:
                    articleDisplays[art['url']] = ""
        return articleNames, articleDisplays

