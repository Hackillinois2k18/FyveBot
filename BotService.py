from BingExternalClient import ArticleTopicQueryNews, ArticleTopicQuerySearch
from SummaryExternalClient import SummaryExternalClient
from ContentSummary import ContentSummary
from YoutubeExternalClient import YoutubeVideoQuery
from selenium_crawler import SeleniumScrape
import os
from random import shuffle
import time


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
        return artSummaries

    def queryYoutubeVideos(self, keywords):
        videoIds = self.youtubeQueryClient.get(keywords)
        videoSummaries = []
        for vidId, title in videoIds.iteritems():
            vidUrl = "https://www.youtube.com/watch?v={}".format(vidId)
            try:
                self.seleniumScrape.run(vidId)
                time.sleep(3)
                with open('raw_transcript.txt', 'r') as rawTranscriptFile:
                    transcript = rawTranscriptFile.read().replace('\n', '')
                rawTranscriptFile.close()
                os.remove('raw_transcript.txt')
            except:
                continue
            if transcript:
                os.system("cat python3 /deep-auto-punctuation/infer.py {} >> inferred_transcript.txt".format(transcript))
                with open('deep-auto-punctuation/inferred_transcript.txt', 'r') as inferredStrFile:
                    inferredString = inferredStrFile.read().replace('\n', '')
                inferredStrFile.close()
                os.remove('deep-auto-punctuation/inferred_transcript.txt')
                sumSentences = self.summaryExtClient.pullSummaryForText(inferredString, title)
                videoSummary = ContentSummary(vidUrl, title, sumSentences)
                videoSummaries.append(videoSummary)
        print("Vid SUMMARIESSSSSSS: {}".format(videoSummaries))
        return videoSummaries



if __name__ == '__main__':
    botService = BotService()
    botService.queryYoutubeVideos("birds")



