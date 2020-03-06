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

def main(argv):
    # Kör programmet med argument.
    if len(argv) != 2:
        print("Run with 2 arguments: search_term, directory")
        return
    search_term = argv[0]
    directory = argv[1]

    tweet_count = 0

    api = connectTweepy()

    # Tweets har unika ID ordnade efter tid. 
    # Hämtar den senaste tweeten för att få tillgång till max_id. 
    tweet_list = getInitialTweet(search_term, api)
    earliest_tweet = latest_tweet = tweet_list[0]
    tweet_count += 1

    # Filerna måste inte finnas, men mappen måste. 
    createFiles(latest_tweet, directory)

    while True:
        # Vi vill ha tweets med IDn mindre än den tidigaste tweeten vi redan har.
        max_id = earliest_tweet.id - 1
        # Hämtar upp till 100 till.
        tweet_list, tweets_remaining = getMoreTweets(search_term, api, max_id)
        if not tweets_remaining:
            break
        # Sista i listan är den tidigaste tweeten. 
        earliest_tweet = tweet_list[-1]
        # Skriv till filerna så variablerna kan återanvändas, vill inte få slut på minne.
        dumpTweetList(tweet_list, directory)
        tweet_count += len(tweet_list)

    finishUp(earliest_tweet, tweet_count, directory)

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
        return initial_tweet

def createFiles(latest_tweet, directory):
    with open(directory+"/INFO.txt", "w") as f:
        f.write("Contains tweets between " + str(latest_tweet.created_at))
    with open(directory+"/tweet_list.json", "w") as f:
        f.write("[")
        json.dump(latest_tweet._json, f, indent=4, separators=(',', ': '))

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

def dumpTweetList(tweet_list, directory):
    # Borde kanske dela upp i fler filer så den inte blir enorm...
    with open(directory+"/tweet_list.json", "a") as f:
        for tweet in tweet_list:
            f.write(",\n")
            json.dump(tweet._json, f, indent=4, separators=(',', ': '))

def finishUp(earliest_tweet, tweet_count, directory):
    with open(directory+"/tweet_list.json", "a") as f:
        f.write("\n]")
    with open(directory+"/INFO.txt", "a") as f:
        f.write(" and " + str(earliest_tweet.created_at))
        f.write("\nContains a total of " + str(tweet_count) + " tweets.")

main(sys.argv[1:])
