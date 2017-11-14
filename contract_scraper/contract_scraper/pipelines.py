# -*- coding: utf-8 -*-



# Define your item pipelines here

#

# Don't forget to add your pipeline to the ITEM_PIPELINES setting

# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



import psycopg2
from pymongo import MongoClient
import re

import contract_data_cleaners as clean

class ContractScraperPipeline(object):
    def process_item(self, item, spider):

        cleaned_naic = clean.parse_naics(item['naics'])
        cleaned_soliciation_number = clean.parse_solicitation_number(item['solicitation number'])
        # initialize connection to mongo database
        client = MongoClient()
        db = client.pminc
        # ensure solicitation exists & record is not blank

        if item['solicitation number'] is not None:
            # print("hello govna!!!")
            # connection string
            conn = psycopg2.connect(host="localhost", database="contract_directory_site", user="postgres",
                                    password="passpass")
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

            # Filter synopsis to look nice
            synopsis = ''.join(item['synopsis']).lstrip("{\"").lstrip().lstrip("\",\"").lstrip().rstrip(
                "\"}").rstrip().rstrip("\",\"")

            query = """
            INSERT INTO contracts(url, title, naics, solicitation_number, agency, agency_office, agency_location, gov_contact_full, posted_date, response_deadline,
            notice_type, classification_code, synopsis, vendor_contact_full, award_date, award_number, award_amount, awarded_duns, awardee,
             point_of_contact, primary_point_of_contact, set_aside)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s)
            """

            data = (str(item['url']), item['title'], cleaned_naic, cleaned_soliciation_number,
                    agency, office, location,
                    item['gov contact full'], item['posted date'], item['response deadline'], item['notice type']
                    , item['classification code'], synopsis, item['vendor contact full']
                    , item['award date'], item['award number'], item['award dollar amount'], item['awarded duns']
                    , item['awardee'], item['point of contact'], item['primary point of contact'], item['set aside'])

            cur.execute(query, data)
            conn.commit()
            cur.close()
            conn.close()
            # END SQL #

            # START MONGO #
            cursor = db.matches.find_one({cleaned_naic + ".contracts": {"$exists": True}})

            # TEST CURSOR
            # cursor = db.matches.find_one({"2.contracts": {"$exists": True}})
            if cursor != None:
                ## THERE IS A LIST OF CONTRACTS FOR THIS NAIC, APPEND THIS CONTRACT TO IT ##

                # if db.matches.find_one({cleaned_naic + ".contracts": { "$in": [cleaned_soliciation_number]}}) == None:
                document_id = db.matches.find_one({cleaned_naic + ".contracts": {"$exists": True}})['_id']
                db.matches.update(
                    {'_id': document_id},
                    {
                        '$addToSet': {
                            cleaned_naic + ".contracts": cleaned_soliciation_number
                        }
                    }
                )

                print("already exists")
            else:
                ## THIS IS THE FIRST CONTRACT FOR THIS NAIC, CREATE A LIST WITH THIS CONTRACT AS THE ONLY ELEMENT ##
                db.matches.insert({cleaned_naic: {"contracts": [cleaned_soliciation_number]}})
                print("add")

            # END MONGO #
        # endif

        return item