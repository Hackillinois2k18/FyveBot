import requests
import credentials


class SummaryExternalClient:

    def pullSummaryForUrl(self, artUrl, title):
        url = "https://api.aylien.com/api/v1/summarize"
        headers = {"X-AYLIEN-TextAPI-Application-Key": credentials.AYLIEN_APP_KEY,
                   "X-AYLIEN-TextAPI-Application-ID" : credentials.AYLIEN_APP_ID}
        params = {"url" : artUrl,
                  "title" : title,
                  "sentences_number": 13}
        summary = requests.get(url=url, headers=headers, params=params)
        sentences = summary.json()['sentences']
        return sentences

    def pullSummaryForText(self, text, title):
        url = "https://api.aylien.com/api/v1/summarize"
        headers = {"X-AYLIEN-TextAPI-Application-Key": credentials.AYLIEN_APP_KEY,
                   "X-AYLIEN-TextAPI-Application-ID" : credentials.AYLIEN_APP_ID}
        params = {"text": text,
                  "title": title,
                  "sentences_number": 13}
        summary = requests.get(url=url, headers=headers, params=params)
        sentences = summary.json()['sentences']
        return sentences



if __name__ == "__main__":
    client = SummaryExternalClient()
    print(client.pullSummaryForUrl("https://en.wikipedia.org/wiki/Sailing#History", "Sailing - Wikipedia"))
