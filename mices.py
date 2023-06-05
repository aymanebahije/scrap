import scrapy


class MicesSpider(scrapy.Spider):
    name = "mices"
    allowed_domains = ["successfulmeetings.com"]
    page_num = 0
    start_urls = ["https://www.successfulmeetings.com/Meeting-Event-Venues/Casablanca-Morocco/Hotels?acg=1&pg=1"]

    def parse(self, response):
        for link in response.css('div.venue-name a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_miceinf)

    def parse_miceinf(self,response):
        venue_inf = response.css('div.venue-info')
        tab = response.css('tbody')
        tab1 = response.css('table.table thead')

        for x,y,z in zip(venue_inf,tab,tab1) :

            yield {
                'name' : response.css('h1.heading-2 ::text').get().replace('                        ','').replace('\r','').replace('\n',''),
                'thead' : '|'.join(z.css('th ::text').get().replace('\r','').replace('\n','')),
                'venue inf' : '|'.join(x.css('div ::text').extract()).replace('\r','').replace('\n',''),
                'tableau' : '|'.join(y.css('tr ::text').extract()).replace('\r','').replace('\n','')
            }
            next_page = f'https://www.successfulmeetings.com/Meeting-Event-Venues/Casablanca-Morocco/Hotels?acg=1&pg='+ str(MicesSpider.page_num) +''
            if MicesSpider.page_num <= 5:
                MicesSpider.page_num += 1
                yield response.follow(next_page, callback=self.parse)


