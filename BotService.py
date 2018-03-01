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
        articleNames, articleDisplays = self.newsArticleClient.get(keyword)
        return articleNames, articleDisplays


    def queryRelevantSearchArticles(self, keyword):
        articleNames, articleDisplays = self.searchArticleClient.get(keyword)
        return articleNames, articleDisplays

    def getSummariesForArticles(self, keyword):
        artSummaries = []
        newsArticleNames, newsArticleDisplays = self.queryRelevantNewsArticles(keyword)
        searchArticleNames, searchArticleDisplays = self.queryRelevantSearchArticles(keyword)
        search_count = 0
        news_count = 0
        for url, title in searchArticleNames.iteritems():
            sumSentences = self.summaryExtClient.pullSummaryForUrl(url, title)
            displayUrl = searchArticleDisplays.get(url)
            if len(sumSentences) > 0:
                articleSummary = ContentSummary(url, title, sumSentences, displayUrl)
                artSummaries.append(articleSummary)
                search_count += 1
            if search_count > 3:
                break
        for url, title in newsArticleNames.iteritems():
            sumSentences = self.summaryExtClient.pullSummaryForUrl(url, title)
            displayUrl = newsArticleDisplays.get(url)
            if len(sumSentences) > 0:
                articleSummary = ContentSummary(url, title, sumSentences, displayUrl)
                artSummaries.append(articleSummary)
                news_count += 1
            if news_count > 3:
                break
        shuffle(artSummaries)
        return json.dumps(artSummaries, encoding='utf-8', default=lambda o: o.__dict__)

    def getYoutubeVideoSums(self, keywords):
        videoTitles, videoDisplays = self.youtubeQueryClient.get(keywords)
        videoSummaries = []
        for vidId, title in videoTitles.iteritems():
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
                vidDisplay = videoDisplays.get(vidId)
                videoSummary = ContentSummary(vidUrl, title, sumSentences, vidDisplay)
                videoSummaries.append(videoSummary)
            else:
                vidDisplay = videoDisplays.get(vidId)
                videoSummary = ContentSummary(vidUrl, title, [], vidDisplay)
                videoSummaries.append(videoSummary)
        return json.dumps(videoSummaries, encoding='utf-8', default=lambda o: o.__dict__)




