from bs4 import BeautifulSoup
import requests
import json

url = 'http://stats.softballmeetup.com/'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
response = requests.get(url, headers=headers, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

statsTable = content.find('table', attrs={"class": "stats-table"})
statsCategories = statsTable.find('tr', attrs={"class": "stat-cats"})
stats = []

for stat in statsCategories.findAll('td', attrs={"class": "stats-cell"}):
    stats.append(stat.text)

playerStats = statsTable.findAll('tr')
players = []

for player in playerStats:
    playerData = player.findAll('td', attrs={"class": "stats-cell"})
    playerStat = {}
    # use enumerate to access value and index
    for i, stat in enumerate(playerData):        
        playerName = stat.find('a')
        pStat = stat.find('div')
        
        if playerName is not None:
            playerStat['id'] = playerName['href'].split('?')[1].split('=')[1]
            playerStat['player'] = playerName.text

        if pStat is not None:
            playerStat[stats[i]] = pStat.text
    
    players.append(playerStat)

# delete the first entry because its the thumbnail image of each player
del players[0]

# write player stats to json
with open('softball-stats.json', 'w') as outfile:
    json.dump(players, outfile)

# Example web scraping logic
# url = 'http://ethans_fake_twitter_site.surge.sh/'

# tweets = []
# for tweet in content.findAll('div', attrs={"class": "tweetcontainer"}):
#     tweetObject = {
#         "author": tweet.find('h2', attrs={"class": "author"}).text,
#         "date": tweet.find('h5', attrs={"class": "dateTime"}).text,
#         "tweet": tweet.find('p', attrs={"class": "content"}).text,
#         "likes": tweet.find('p', attrs={"class": "likes"}).text,
#         "shares": tweet.find('p', attrs={"class": "shares"}).text
#     }
#     tweets.append(tweetObject)
# with open('twitterData.json', 'w') as outfile:
#     json.dump(tweets, outfile)
