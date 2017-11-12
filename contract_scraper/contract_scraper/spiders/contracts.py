from scrapy.selector import Selector

from scrapy.http import HtmlResponse

import scrapy

import re


class ContractSpider(scrapy.Spider):
    name = "contracts"

    # assigns command line argument as page_id to be appended to URL string
    def __init__(self, page_id, *args, **kwargs):
        super(ContractSpider, self).__init__(*args, **kwargs)
        self.page_id = page_id

    # Request to Results page with list of contracts
    def start_requests(self):

        # URL of contract to scrape
        url = "https://www.fbo.gov/index?s=opportunity&mode=list&tab=list&tabmode=list&pp=50&pageID=" + self.page_id

        # calls callback function which parses results page containing list of links to contracts
        yield scrapy.Request(url=url, callback=self.parse_results)

    # crawls results page and requests parse function which crawls the associated page of each result
    def parse_results(self, response):

        # clears output file
        # open('contracts.json', 'w').close()

        # initialize list of contract urls on results page
        url_list = []

        # for each result, get the url of each page associated with the result
        for result in response.selector.css('tr.lst-rw'):
            url_list.append("https://www.fbo.gov/index" + result.css("td.lst-cl a::attr(href)").extract_first())

        # iterate through all contract url's on results page and parse each listing
        for url in url_list:
            # scrape each page associated with each result
            yield scrapy.Request(url=url, callback=self.parse_contract, meta={'url': url})

    # parses specific page for each contract
    def parse_contract(self, response):

        contract_url = response.meta.get('url')

        list = response.css('div.fld_description div.widget::text').extract()

        yield {

            'url': contract_url,
            'title': response.css('div.agency-header > h2::text').extract_first(),
            'naics': response.css('div.fld_naics_code div.widget::text').extract_first(),
            'solicitation number': response.css('div.sol-num::text').extract_first(),
            'agency': response.css('div.agency-header div.agency-name::text').extract(),
            # 'agency office': response.css('div.agency-header div.agency-name::text').extract()[1],
            # 'agency location': response.css('div.agency-header div.agency-name::text').extract()[2],
            'gov contact full': response.css('div.agency-header div.agency-name::text').extract(),
            'posted date': response.css('div.fld_posted_date div.widget::text').extract_first(),
            'response deadline': response.css('div.fld_response_deadline div.widget::text').extract_first(),
            'notice type': response.css('div.fld_procurement_type div.widget::text').extract_first(),
            'classification code': response.css('div.fld_classification_code div.widget::text').extract_first(),
            'synopsis': response.css('div.fld_description div.widget::text').extract(),

            # Office address
            'vendor contact full': response.css('div.fld_office_address_text div.widget::text').extract(),
            'award date': response.css('div.fld_contract_award_date div.widget::text').extract(),
            'award number': response.css('div.fld_contract_award_number div.widget::text').extract(),
            'award dollar amount': response.css('div.fld_contract_award_amount div.widget::text').extract(),
            'awarded duns': response.css('div.fld_contractor_awarded_duns div.widget::text').extract(),

            # contractor POC
            'awardee': response.css('div.fld_contractor_awardee_text div.widget::text').extract(),

            # Government POC
            'point of contact': response.css('div.fld_poc_text div.widget::text').extract(),

            # #Also could be government POC
            'primary point of contact': response.css('div.fld_primary_poc div.widget::text').extract(),
            'set aside': response.css('div.fld_set_aside div.widget::text').extract(),

        }
