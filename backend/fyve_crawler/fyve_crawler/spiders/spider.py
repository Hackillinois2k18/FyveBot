import scrapy


"""
Class for building a spider.
"""

link_placeholder = 'link'

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
        
        pass
    
    