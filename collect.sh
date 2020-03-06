#!/bin/bash

# Skapar en mapp "dag-månad-år" med undermappar för varje företag i companies.txt
# Kör sedan tweets.py för varje företag och tillhörande mapp. 
# Loggar även med timestamps till log.txt.

# companies.txt ska innehålla en @user per rad med tom rad på slutet. 

# Söker enligt https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
# '@user OR to:user OR from:user' = tweets som nämner user, till user eller av user
# För att få till detta som ett argument används följande nedan:
# "'$line OR to:"${line#'@'}" OR from:"${line#'@'}"'"

DATE=$(date +"%d-%m-%y")
mkdir ${DATE}
touch "$DATE/log.txt"

cat companies.txt | while read line; do
    query="$line OR to:"${line#'@'}" OR from:"${line#'@'}
    mkdir "$DATE/$line"
    touch "$DATE/$line/INFO.txt"
    touch "$DATE/$line/tweet_list.json"
    echo $(date +%T)" - collecting '${query}'" | tee -a "$DATE/log.txt"
    python3 tweets.py "${query}" "$DATE/$line" 2>&1 | tee -a "$DATE/log.txt"
    echo $(date +%T)" - done with $line" | tee -a "$DATE/log.txt"
done