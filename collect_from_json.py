import os 
import json
import datetime
import subprocess

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

                        res = subprocess.run(["python3", "get_tweets.py", searchterm, collection_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                        if res.returncode == 1:
                            log(res.stdout)
                        
                else:
                    collection_dir = os.path.join(DATE, industry, name, twitter_handles)
                    os.mkdir(collection_dir)
                    searchterm = " OR ".join([twitter_handles, "to:"+twitter_handles[1:], "from:"+twitter_handles[1:]])
                    log("Collecting: " + searchterm)

                    res = subprocess.run(["python3", "get_tweets.py", searchterm, collection_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    if res.returncode == 1:
                        log(res.stdout)

                log("Done with: " + name)

    except Exception as e:
        log(str(e))
        exit(1)

main()
