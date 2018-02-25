from BingExternalClient import ArticleTopicQueryNews, ArticleTopicQuerySearch
from SummaryExternalClient import SummaryExternalClient
from ContentSummary import ContentSummary
from YoutubeExternalClient import YoutubeVideoQuery
from selenium_crawler import TestTranscript
import os
from random import shuffle


class BotService:

    def __init__(self):
        self.summaryExtClient = SummaryExternalClient()
        self.newsArticleClient = ArticleTopicQueryNews()
        self.searchArticleClient = ArticleTopicQuerySearch()
        self.youtubeQueryClient = YoutubeVideoQuery()
        self.testTranscript = TestTranscript()

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
                transcript = self.testTranscript.test_grabTranscript(vidId)
            except:
                continue
            if transcript:
                os.system("cat python3 /deep-auto-punctuation/infer.py {} >> inferred_transcript.txt".format(transcript))
                with open('/deep-auto-punctuation/inferred_transcript.txt', 'r') as inferredStrFile:
                    inferredString = inferredStrFile.read().replace('\n', '')
                print(inferredString)
                sumSentences = self.summaryExtClient.pullSummaryForText(inferredString, title)
                videoSummary = ContentSummary(vidUrl, title, sumSentences)
                videoSummaries.append(videoSummary)
        return videoSummaries



if __name__ == '__main__':
    botService = BotService()
    botService.queryYoutubeVideos("birds")



