from BingExternalClient import ArticleTopicQueryNews, ArticleTopicQuerySearch
from SummaryExternalClient import SummaryExternalClient
from ArticleSummary import ArticleSummary
from random import shuffle


class BotService:

    def __init__(self):
        self.summaryExtClient = SummaryExternalClient()
        self.newsArticleClient = ArticleTopicQueryNews()
        self.searchArticleClient = ArticleTopicQuerySearch()

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
            articleSummary = ArticleSummary(url, title, sumSentences)
            artSummaries.append(articleSummary)
        for title, url in newsArticles.iteritems():
            sumSentences = self.summaryExtClient.pullSummaryForUrl(url, title)
            articleSummary = ArticleSummary(url, title, sumSentences)
            artSummaries.append(articleSummary)
        shuffle(artSummaries)
        return artSummaries

if __name__ == '__main__':
    botService = BotService()
    botService.getSummariesForArticles("birds")



