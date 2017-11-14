# -*- coding: utf-8 -*-



# Define here the models for your spider middleware

#

# See documentation in:

# http://doc.scrapy.org/en/latest/topics/spider-middleware.html



from scrapy import signals

from scrapy.exceptions import IgnoreRequest





from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session

from sqlalchemy import create_engine







class ContractScraperSpiderMiddleware(object):

    # Not all methods need to be defined. If a method is not defined,

    # scrapy acts as if the spider middleware does not modify the

    # passed objects.



    @classmethod

    def from_crawler(cls, crawler):

        # This method is used by Scrapy to create your spiders.

        s = cls()

        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)

        return s



    def process_spider_input(self, response, spider):

        # Called for each response that goes through the spider

        # middleware and into the spider.



        # Should return None or raise an exception.

        return None



    def process_spider_output(self, response, result, spider):

        # Called with the results returned from the Spider, after

        # it has processed the response.

        # DEFAULT MIDDLEWARE
        for i in result:
            yield i


        # CHECKS FOR DUPILICATE SOLICITATION NUMBERS IN SQL DATABASE, RAISES IGNOREREQUEST IF SOL NUMBER EXISTS

        # # Initialize connection to database
        #
        # Base = automap_base()
        #
        # engine = create_engine('postgresql://postgres:passpass@localhost/contract_directory_site')
        #
        # Base.prepare(engine, reflect=True)
        #
        #
        #
        # # Create object to be mapped to database table
        #
        # Contract = Base.classes.contracts
        #
        # session = Session(engine)
        #
        #
        #
        # solicitation_numbers = set()
        #
        # for record in session.query(Contract):
        #
        #     solicitation_numbers.add(record.solicitation_number)
        #
        #
        #
        # # Must return an iterable of Request, dict or Item objects.
        #
        # for item in result:
        #
        #     if type(item) == dict:
        #
        #         if item['solicitation number'] in solicitation_numbers:
        #
        #             print(item['solicitation number'])
        #
        #             # raise IgnoreRequest()
        #
        #
        #
        #         else:
        #
        #             yield item
        #
        #     else:
        #
        #         yield item







    def process_spider_exception(self, response, exception, spider):

        # Called when a spider or process_spider_input() method

        # (from other spider middleware) raises an exception.



        # Should return either None or an iterable of Response, dict

        # or Item objects.

        pass



    def process_start_requests(self, start_requests, spider):

        # Called with the start requests of the spider, and works

        # similarly to the process_spider_output() method, except

        # that it doesn’t have a response associated.



        # Must return only requests (not items).

        for r in start_requests:

            yield r



    def spider_opened(self, spider):

        spider.logger.info('Spider opened: %s' % spider.name)