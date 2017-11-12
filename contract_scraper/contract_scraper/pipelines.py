# -*- coding: utf-8 -*-



# Define your item pipelines here

#

# Don't forget to add your pipeline to the ITEM_PIPELINES setting

# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



import psycopg2

import re



class ContractScraperPipeline(object):

    def process_item(self, item, spider):

        # ensure solicitation exists & record is not blank

        if item['solicitation number'] is not None:
            # print("hello govna!!!")
            #connection string
            conn = psycopg2.connect(host="localhost", database="contract_directory_site", user="postgres", password="passpass")
            cur = conn.cursor()

            try:
                agency = item['agency'][0]

            except KeyError:
                agency = "none"

            try:
                office = item['agency'][1]

            except KeyError:
                office = "none"

            try:
                location = item['agency'][2]

            except KeyError:
                location = "none"


            #Filter synopsis to look nice
            synopsis = ''.join(item['synopsis']).lstrip("{\"").lstrip().lstrip("\",\"").lstrip().rstrip("\"}").rstrip().rstrip("\",\"")

            query = """
            INSERT INTO contracts(url, title, naics, solicitation_number, agency, agency_office, agency_location, gov_contact_full, posted_date, response_deadline,
            notice_type, classification_code, synopsis, vendor_contact_full, award_date, award_number, award_amount, awarded_duns, awardee,
             point_of_contact, primary_point_of_contact, set_aside)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s)
            """


            data = (str(item['url']), item['title'], item['naics'], item['solicitation number'],
                    agency, office, location,
                    item['gov contact full'], item['posted date'], item['response deadline'], item['notice type']
                    , item['classification code'], synopsis, item['vendor contact full']
                    , item['award date'], item['award number'], item['award dollar amount'], item['awarded duns']
                    , item['awardee'], item['point of contact'], item['primary point of contact'], item['set aside'])



            cur.execute(query, data)
            conn.commit()
            cur.close()
            conn.close()
        # endif

        return item