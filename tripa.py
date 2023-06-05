from abc import ABC

import scrapy


class tripaa(scrapy.Spider, ABC):
    name = 'tri'
    allowed_domains = ["tripadvisor.fr"]
    start_urls =['https://www.tripadvisor.fr/Hotels-g293737-oa30-Tangier_Tanger_Tetouan_Al_Hoceima-Hotels.html']
    page_num = 0

    def parse(self, response):
        cases = response.css('div.yJIls.z.P0.M0')

        for p in cases :

            yield {
            'name' : '|'.join(p.css('div.nBrpc.Wd.o.W ::text').extract()),
            'rate' : p.css('div.jVDab.o.W.f.u.w.GOdjs ::attr(aria-label)').get().replace('\xa0bulles.' ,'/')

         }
        next_page = f'https://www.tripadvisor.fr/Hotels-g293737-oa'+str(tripaa.page_num) +'-Tangier_Tanger_Tetouan_Al_Hoceima-Hotels.html'
        if tripaa.page_num <= 500:
            tripaa.page_num += 30
            yield response.follow(next_page, callback=self.parse)



