# coding=utf-8

# import codecs
import json

import scrapy

from bible_com.items import Book, Verse

API_DOMAIN = 'https://www.bible.com'

start_urls = {
    # 'https://www.bible.com/pl/bible/132/gen.1': u'Biblia Gdańska',
    # 'https://www.bible.com/pl/bible/319/gen.1': u'Nowa Biblia Gdańska',
    # 'https://www.bible.com/pl/bible/547/gen.1': u'King James Version, American Edition',
    # 'https://www.bible.com/pl/bible/130/gen.1': u'Orthodox Jewish Bible',
    # 'https://www.bible.com/pl/bible/1171/gen.1': u'Modern English Version',
    'https://www.bible.com/pl/bible/1171/gen.1': u"International Children's Bible",
}


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["bible.com"]
    start_urls = start_urls.keys()

    def parse(self, response):
        translation = start_urls[response.url]
        for li in response.css('ul#reader_book_list li[data-meta]'):
            metadata = li.xpath('@data-meta')[0].extract()
            book, book_name = metadata.split(' ', 1)
            yield Book(
                translation=translation,
                shortname=book.lower(),
                fullname=book_name,
            )
            for url in li.css('[data-chapter-href]'):
                api_url = url.xpath('@data-chapter-href')[0].extract()
                url = API_DOMAIN + api_url[:api_url.rfind('.')] + '.json'
                yield scrapy.Request(url, self.parse_api, meta={
                    'api_url': api_url,
                    'translation': translation,
                })

    def parse_api(self, response):
        api_url = response.meta['api_url']
        book, chapter = (
            api_url[api_url.rfind('/')+1:api_url.rfind('.')].split('.')
        )

        html = json.loads(response.body)['reader_html']
        html_response = scrapy.http.HtmlResponse(
            response.url,
            body=html,
            encoding='utf8',
        )

        items = {}
        for verse in html_response.css('.verse'):
            verse_number = verse.xpath('@class')[0].extract().split()[1][1:]
            if verse_number in items:
                item = items[verse_number]
            else:
                item = Verse(
                    translation=response.meta['translation'],
                    book=book,
                    chapter=int(chapter),
                    verse=int(verse_number),
                    text='',
                )
                items[verse_number] = item
            item['text'] += ''.join(verse.css('.content::text').extract())
        return items.values()
