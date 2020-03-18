import os 
import json
import datetime
import get_tweets

DATE = str(datetime.date.today())
os.mkdir(DATE)
with open(os.path.join(DATE, "log.txt"), "a") as f:
        f.write("---")

def log(m):
    with open(os.path.join(DATE, "log.txt"), "a") as f:
        f.write("\n" + m)
    print(m)

def main():
    try: 
        #Kollar stavfel i nycklar först
        with open("companies_europe.json", "r") as f:
            company_data = json.loads(f.read())
        for branch in company_data:
            industry = branch["industry"]
            companies = branch["companies"]
            for company in companies:
                name = company["name"]
                twitter_handles = company["twitter_handle"]
        
        #Kör datainsamling
        for branch in company_data:
            industry = branch["industry"]
            companies = branch["companies"]
            os.mkdir(os.path.join(DATE, industry))
            for company in companies:
                name = company["name"]
                twitter_handles = company["twitter_handle"]
                os.mkdir(os.path.join(DATE, industry, name))
                log("Working on: " + name)
                if isinstance(twitter_handles, list):
                    for handle in twitter_handles:
                        collection_dir = os.path.join(DATE, industry, name, handle)
                        os.mkdir(collection_dir)
                        searchterm = " OR ".join([handle, "to:"+handle[1:], "from:"+handle[1:]])
                        log("Collecting: " + searchterm)
                        get_tweets.collect([searchterm, collection_dir])
                        with open(os.path.join(collection_dir, "hej.txt"), "w") as f:
                            pass
                else:
                    collection_dir = os.path.join(DATE, industry, name, twitter_handles)
                    os.mkdir(collection_dir)
                    searchterm = " OR ".join([twitter_handles, "to:"+twitter_handles[1:], "from:"+twitter_handles[1:]])
                    log("Collecting: " + searchterm)
                    get_tweets.collect([searchterm, collection_dir])
                    with open(os.path.join(collection_dir, "hej.txt"), "w") as f:
                        pass
                log("Done with: " + name)

    except Exception as e:
        log(str(e))
        exit()

main()
