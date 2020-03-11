import os 
import json
import datetime
import get_tweets

# Nästan klar, använd inte!
# Att göra:
#   -Skriv bra log
#   -Testa ordentligt

date = str(datetime.date.today())
os.mkdir(date)
with open("companiestest.json", "r") as f:
    company_data = json.loads(f.read())


for branch in company_data.keys():
    os.mkdir(os.path.join(date, branch))
    for company in company_data[branch].keys():
        os.mkdir(os.path.join(date, branch, company))
        twitter_handles = company_data[branch][company]["twitter_handle"]
        if isinstance(twitter_handles, list):
            for handle in twitter_handles:
                collection_dir = os.path.join(date, branch, company, handle)
                os.mkdir(collection_dir)
                searchterm = " OR ".join([handle, "to:"+handle[1:], "from:"+handle[1:]])
                get_tweets.collect([searchterm, collection_dir])
        else:
            collection_dir = os.path.join(date, branch, company, twitter_handles)
            os.mkdir(collection_dir)
            searchterm = " OR ".join([twitter_handles, "to:"+twitter_handles[1:], "from:"+twitter_handles[1:]])
            get_tweets.collect([searchterm, collection_dir])
