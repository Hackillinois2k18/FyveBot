import subprocess
from pipes import quote

from BingExternalClient import ArticleTopicQueryNews, ArticleTopicQuerySearch
from SummaryExternalClient import SummaryExternalClient
from ContentSummary import ContentSummary
from YoutubeExternalClient import YoutubeVideoQuery
from selenium_crawler import SeleniumScrape
import os
from random import shuffle
import time
import json
import re
import jsonify


class BotService:

    def __init__(self):
        self.summaryExtClient = SummaryExternalClient()
        self.newsArticleClient = ArticleTopicQueryNews()
        self.searchArticleClient = ArticleTopicQuerySearch()
        self.youtubeQueryClient = YoutubeVideoQuery()
        self.seleniumScrape = SeleniumScrape()

    def queryRelevantNewsArticles(self, keyword):
        articleUrls = self.newsArticleClient.get(keyword)
        return articleUrls


    def queryRelevantSearchArticles(self, keyword):
        articleUrls = self.searchArticleClient.get(keyword)
        return articleUrls

    def getSummariesForArticles(self, keyword):
        artSummaries = []
        newsArticles = self.queryRelevantNewsArticles(keyword)
        searchArticles = self.queryRelevantSearchArticles(keyword)
        for title, url in searchArticles.iteritems():
            sumSentences = self.summaryExtClient.pullSummaryForUrl(url, title)
            articleSummary = ContentSummary(url, title, sumSentences)
            artSummaries.append(articleSummary)
        for title, url in newsArticles.iteritems():
            sumSentences = self.summaryExtClient.pullSummaryForUrl(url, title)
            articleSummary = ContentSummary(url, title, sumSentences)
            artSummaries.append(articleSummary)
        shuffle(artSummaries)
        print(json.dumps(artSummaries, default=lambda o: o.__dict__))
        return artSummaries

    def getYoutubeVideoSums(self, keywords):
        videoIds = self.youtubeQueryClient.get(keywords)
        videoSummaries = []
        for vidId, title in videoIds.iteritems():
            vidUrl = "https://www.youtube.com/watch?v={}".format(vidId)
            try:
                self.seleniumScrape.run(vidId)
                time.sleep(3)
                with open('raw_transcript.txt', 'r') as rawTranscriptFile:
                    transcript = rawTranscriptFile.read().replace('\n', ' ')
                rawTranscriptFile.close()
                os.remove('raw_transcript.txt')
            except:
                continue
            if transcript:
                transcript = re.sub('\s*\[[^]]*]', '', transcript)
                subprocess.call("cd deep-auto-punctuation;python3 infer.py {} >> inferred_transcript.txt".format(quote(transcript)), shell=True)
                with open('deep-auto-punctuation/inferred_transcript.txt', 'r') as inferredStrFile:
                    inferredString = inferredStrFile.read().replace('\n', ' ')
                inferredStrFile.close()
                os.remove('deep-auto-punctuation/inferred_transcript.txt')
                sumSentences = self.summaryExtClient.pullSummaryForText(inferredString, title)
                videoSummary = ContentSummary(vidUrl, title, sumSentences)
                videoSummaries.append(videoSummary)
        print(json.dumps(videoSummaries, default=lambda o: o.__dict__))
        return videoSummaries



if __name__ == '__main__':
    botService = BotService()
    botService.getYoutubeVideoSums("how to make a slip and slide")



