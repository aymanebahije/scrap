from abc import ABC
import re
import scrapy
import psycopg2
import pandas as pd

class namehot(scrapy.Spider, ABC):

    name = 'ba'
    page_num = 0
    allowed_domains = ["booking.com"]
    start_urls = [
        "https://www.booking.com/searchresults.fr.html?ss=Rabat&ssne=Rabat&ssne_untouched=Rabat&efdco=1&label=gen173nr-1FCAso7AFCJnRoZS1yaXR6LWNhcmx0b24tbmV3LXlvcmstY2VudHJhbC1wYXJrSAlYBGiMAYgBAZgBCbgBF8gBDNgBAegBAfgBAogCAagCA7gC4eOroAbAAgHSAiQ2NzI4ZmUxZS0yZTEwLTQzNGYtYjlhOS0zNjU2MTI3MzFhYjLYAgXgAgE&sid=b85d5f37ea7a23a27f0ec5f4f0df18df&aid=304142&lang=fr&sb=1&src_elem=sb&src=searchresults&dest_id=-43376&dest_type=city&checkin=2023-06-15&checkout=2023-06-16&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure"]

    def parse(self, response):
        for link in response.css('div.dd023375f5 a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_hotelinf)

    def parse_hotelinf(self, response):
        faciliti = response.css('div.hp--popular_facilities.js-k2-hp--block')
        hotprice = response.css('table.hprt-table')
        roomtype = response.css('table.hprt-table')
        equipement = response.css('div.e50d7535fa')
        review = response.css('div.a1b3f50dcd.ade831375b.cc84eb0131.b2fe1a41c3.c1b465858f.d46673fe81')
        option = response.css('table.hprt-table')
        summary = response.css('div.hp_desc_main_content')
        superficie_elements = response.css(
            'span.bui-badge.bui-badge--outline.room_highlight_badge--without_borders ::text').getall()
        superficie_with_m2 = [text for text in superficie_elements if "m²" in text]

        for  z, w,y,x,u,t,v in zip(faciliti, roomtype,hotprice,option,review,summary,equipement) :
            summary_text = '|'.join(t.css('div.hp_desc_main_content ::text').getall())
            summary_text = summary_text.replace('\n', '').replace('\xa0', '|').replace('|', '').replace('En voir plus','')
            restaurant_elements = response.css('div.b3d1cacd40.a2cb913cd1')
            restaurants = response.css('div.a0c113411d.c90c0a70d3.a34d1a4138 ::text').getall()
            restaurantw_text = '|'.join(restaurants)
            if len(restaurant_elements) >= 3:
                restaurant_text = restaurant_elements[1].css('::text').get()
            else:
                restaurant_text = None

            if superficie_with_m2:
                super =  ' | '.join(superficie_with_m2)

            yield {
                    'name': response.css('h2.d2fee87262.pp-header__title ::text').get(),
                    'adress': response.css('span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip ::text').get().replace('\n','').replace('\n',''),
                    'points forts': ' | '.join(z.css('span.db312485ba ::text').extract()),
                    'roomtype': ' | '.join(w.css('span.hprt-roomtype-icon-link ::text').extract()).replace('\n','').replace('\n',''),
                    'nombre de personne': '|'.join(response.css('span.bui-u-sr-only ::text').extract()),
                    'prix de tous les chambres' : '|'.join(y.css('span.prco-valign-middle-helper ::text').extract()).replace('\nMAD\xa0', '').replace('\n','').strip(),
                    'type des categories' : '|'.join(u.css('span.d6d4671780 ::text').extract()),
                    'numero des categories' : '|'.join(u.css('div.ee746850b6.b8eef6afe1 ::text').extract()),
                    'petit dej': '|'.join(x.css('span.ungreen-condition-green ::text').extract()),
                    'summary' : summary_text,
                    'commentaire client' : response.css('div.b5cd09854e.d10a6220b4 ::text').get(),
                    'etat de note' : response.css('div.d8eab2cf7f.ae7544114a ::text').get(),
                    'nbr de restaurant sur place': restaurant_text,
                    'equipement': ' | '.join(v.css('span.db312485ba ::text').extract()),
                    'information du restaurant' : restaurantw_text,
                    'superficie chambre' : super,
                    'coordonnées' : response.css('.hp--sidebar .hotel-sidebar-map #hotel_sidebar_static_map ::attr(data-atlas-latlng)').get(),
                    'durabilité' : response.css('span.d8eab2cf7f.cf9ebde7b2.be09c104ad ::text').get(),
                }





            next_page = f'https://www.booking.com/searchresults.fr.html?ss=Rabat&ssne=Rabat&ssne_untouched=Rabat&efdco=1&label=gen173nr-1FCAso7AFCJnRoZS1yaXR6LWNhcmx0b24tbmV3LXlvcmstY2VudHJhbC1wYXJrSAlYBGiMAYgBAZgBCbgBF8gBDNgBAegBAfgBAogCAagCA7gC4eOroAbAAgHSAiQ2NzI4ZmUxZS0yZTEwLTQzNGYtYjlhOS0zNjU2MTI3MzFhYjLYAgXgAgE&sid=b85d5f37ea7a23a27f0ec5f4f0df18df&aid=304142&lang=fr&sb=1&src_elem=sb&src=searchresults&dest_id=-43376&dest_type=city&checkin=2023-06-15&checkout=2023-06-16&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset='+str(namehot.page_num) +''
            if namehot.page_num <= 25:
                namehot.page_num += 25
                yield response.follow(next_page, callback=self.parse)


