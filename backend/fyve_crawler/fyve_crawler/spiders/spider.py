import scrapy


"""
Class for building a spider.
"""

link_placeholder = 'https://www.youtube.com/watch?v=cqcMulBRcTo'

class Spider(scrapy.Spider):
    name = "youtube_links"
    
    def start_requests(self):
        urls = [
            link_placeholder
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        # TODO: implement custom for parsing text log from youtube vid
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)