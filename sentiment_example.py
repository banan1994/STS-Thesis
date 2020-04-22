from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

strings = ["We got an email and a text saying our flight was cancelled. On My Bookings it also says it's cancelled. Yet when I click further it says it's NOT cancelled and it won't let me get a refund. SORT THIS OUT!!!", "RT @SputnikInt: Russia's Aeroflot suspends flights to US, UAE, European destinations amid virus outbreak\n\n@aeroflot #CoronavirusOutbreak #C\u2026", "@aeroflot your US customer number is busy and I need to cancel a flight due to Covid-19, help?", "@British_Airways Can someone look at my DM from 5 days ago", "@CooperativeBank, and a big plaudit to them for painlessly refunding my flight money from @flybe with ease. Although only £250, the money was back in my account within hours. Great service as always.👍🏻"]

for string in strings:
    print('Tweet:',string)
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(string)
    print('Positivt sentiment:', sentiment["pos"])
    print('Negativt sentiment:', sentiment["neg"])
    print('Neutral sentiment:', sentiment["neu"])
    print('Compound sentiment:', sentiment["compound"])
    print('')