import tweepy
import json
import sys

'''
python3 tweets.py [sökterm] [mapp]

-Sökinstruktion: https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators

-Använder Twitters search api och sparar alla tillgängliga tweets i tweet_list.json i angiven mapp. 
-tweet_list.json öppnas sedan som ett file object f och samtliga tweets kan laddas som en lista med json.load(f)
-Skapar även INFO.txt med tidsintervall och antal. 

-Tillgängliga tweets är inte nödvändigtvis samtliga tweets, och den söker ungefär en vecka tillbaka. 
-Search apin är att jämföra med att skriva söktermen i sökfältet och trycka på latest (eftersom vi använder recent)
    samt kombinera detta med tweets&replies från användarens sida. 
-Vet inte vad som händer när saker går fel, så logga gärna. Felutskrifterna är rätt basic.

För att testa att den verkligen fungerar:
-Satte count till 2 i getMoreTweets()
-Använde ett sömnigt sökord: '@liberalapartiet OR to:liberalapartiet OR from:liberalapartiet'
-Jämförde insamlade tweets med resultaten på hemsidan
'''

FILE_SIZE = 1000

# Ha nyckeln, annars går det inte.
with open("twitter_auth.json") as f:
    TWITTER_APP_AUTH = json.load(f)

def collect(argv):
    # Kör programmet med argument.
    if len(argv) != 2:
        print("Run with 2 arguments: search_term, directory")
        return

    search_term = argv[0]
    directory = argv[1]

    

    api = connectTweepy()

    # Tweets har unika ID ordnade efter tid. 
    # Hämtar den senaste tweeten för att få tillgång till max_id. 
    earliest_tweet = latest_tweet = getInitialTweet(search_term, api)

    # Lite översiktsinfo. Mappen måste finnas.  
    with open(directory+"/INFO.txt", "w") as f:
        f.write("Contains tweets between " + str(latest_tweet["created_at"]))

    tweet_count = 0
    file = 0
    max_id = earliest_tweet["id"] + 1
    tweets_remaining = True
    while tweets_remaining:
        tweet_list = []
        # Inre loopen körs tills listan är full (FILE_SIZE).
        while ((tweet_count - (file*FILE_SIZE)) // FILE_SIZE) == 0:
            # Vi vill ha tweets med IDn mindre än den tidigaste tweeten vi redan har.
            max_id = earliest_tweet["id"] - 1
            # Hämtar upp till 100 till.
            new_tweets, tweets_remaining = getMoreTweets(search_term, api, max_id)
            if not tweets_remaining:
                break
            new_tweets = cleanResults(new_tweets)
            tweet_count += len(new_tweets)
            tweet_list += new_tweets
            # Sista i listan är den tidigaste tweeten. 
            earliest_tweet = tweet_list[-1]
        if len(tweet_list) == 0:
            break
        # Skriv till filerna så variablerna kan återanvändas, vill inte få slut på minne.
        dumpTweetList(tweet_list, directory, file)
        file += 1

    with open(directory+"/INFO.txt", "a") as f:
        f.write(" and " + str(earliest_tweet["created_at"]))
        f.write("\nContains a total of " + str(tweet_count) + " tweets.")

def connectTweepy():
    try:
        auth = tweepy.OAuthHandler(
            TWITTER_APP_AUTH['consumer_key'], 
            TWITTER_APP_AUTH['consumer_secret']
            )
        auth.set_access_token(
            TWITTER_APP_AUTH['access_token'], 
            TWITTER_APP_AUTH['access_token_secret']
            )
        api = tweepy.API(auth, wait_on_rate_limit=True)
    except Exception as e:
        print("connectTweepy()", type(e), e)
        exit()
    else:
        return api

def getInitialTweet(search_term, api):
    try:
        # tweet_mode='extended' är helt nödvändigt för att kunna göra textanalys. 
        initial_tweet = api.search(q=search_term, count=1, result_type='recent', tweet_mode='extended')
        if len(initial_tweet) < 1:
            raise Exception("Empty first tweet.")
    except Exception as e:
        print("getInitialTweet()", type(e), e)
        exit()
    else: 
        return initial_tweet[0]._json

def getMoreTweets(search_term, api, max_id):
    try:
        # Count är max 100. 
        tweet_list = api.search(q=search_term, count=100, result_type="recent", max_id=max_id, tweet_mode='extended')
        if len(tweet_list) < 1:
            return [], False
        else:
            return tweet_list, True
    except Exception as e:
        print("getMoreTweets()", type(e), e)
        exit()

def cleanResults(tweet_list):
    # Att göra: Ta bort fält vi inte behöver
    tweet_list = list(map(lambda x: x._json, tweet_list))
    return tweet_list

def dumpTweetList(tweet_list, directory, file):
    with open(directory+"/tweet_list_"+str(file+1)+".json", "w") as f:
        f.write(json.dumps(tweet_list, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    collect(sys.argv[1:])
