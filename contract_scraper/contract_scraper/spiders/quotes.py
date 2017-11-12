import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # example of using command line arguments

    def __init__(self, test='', *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, *kwargs)

        self.test = test

    def start_requests(self):
        urls = [

            'http://quotes.toscrape.com/page/1/',

            'http://quotes.toscrape.com/page/2/',

        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Saves html responses in project directory

    def parse(self, response):
        # Grabs page # from URL (1 or 2)

        page = response.url.split("/")[-2]

        # downloads response into html files

        filename = 'quotes-%s.html' % page

        with open(filename, 'wb') as f:
            f.write(response.body)

        self.log('Saved file %s' % filename)





        # Parses the quotes

        # def parse(self, response):

        #     for quote in response.css('div.quote'):

        #         yield {

        #             'text': quote.css('span.text::text').extract_first(),

        #             'author': quote.css('small.author::text').extract_first(),

        #             'tags': quote.css('div.tags a.tag::text').extract(),

        #         }
