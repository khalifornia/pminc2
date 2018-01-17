from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
# Connect to database using sqlalchemy python package
Base = automap_base()
engine = create_engine('postgresql://postgres:passpass@localhost/contract_directory_site')
Base.prepare(engine, reflect=True)

# Create object to be mapped to existing database table
Vendor = Base.classes.listings_vendor
Session = sessionmaker(bind=engine)
session = Session()

client = MongoClient()
db = client.pminc

vendor_count = 0
write_count = 0

for v in session.query(Vendor):
    vendor_count += 1
    cursor = db.matches.find_one({v.prod_1_naic + ".vendors": {"$exists": True}})
    if cursor != None:
        ## There is a list of vendors for this NAIC, APPEND this vendor to it ##
        document_id = db.matches.find_one({v.prod_1_naic + ".vendors": {"$exists": True}})['_id']
        try:
            db.matches.update(
                {'_id': document_id},
                {
                    '$addToSet': {
                        v.prod_1_naic + ".vendors": v.listing_client_pk
                    }
                }
            )
            write_count += 1
        except:
            print("key error")
            continue

    else:
        ## THERE is no vendor list for this NAIC yet ##
        try:
            db.matches.insert({v.prod_1_naic: {"vendors": [v.listing_client_pk]}})
            write_count += 1
        except:
            print("key error")

print("write count: " + str(write_count))
print("vendor count: " + str(vendor_count))