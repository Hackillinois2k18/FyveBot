from flask import Flask, jsonify
from flask_restful import Resource, Api
import requests
import json

app = Flask(__name__)
api = Api(app)

class TopHeadlines(Resource):

    def get(self, keyword):
        json_data = requests.get(
            "https://newsapi.org/v2/everything?q={}&sortBy=relevance&apiKey=8e4ff85bcf95457b8ec90707797bcb3e".format(keyword))
        for art in json_data.json()['articles']:
            print(art['url'])
        return json_data.json()


api.add_resource(TopHeadlines, '/headlines/<keyword>')

if __name__ == '__main__':
    app.run(port=8888)
