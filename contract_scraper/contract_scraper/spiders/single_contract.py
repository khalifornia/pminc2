import scrapy


class SingleContractSpider(scrapy.Spider):
    name = "singlecontract"

    def start_requests(self):
        # open('singlecontract.json', 'w').close()

        urls = ["https://www.fbo.gov/index?s=opportunity&mode=form&id=af2bae8856cd61928defef7277c739c4&tab=core&_cview=0"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_results, meta={'url': url})

    def parse_results(self, response):
        contract_url = response.meta.get('url')

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
