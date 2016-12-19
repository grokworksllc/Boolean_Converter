import urllib.request as ulib
import base64
import uuid
import json

# Three essential stages to this bot.
# 1. Gather information. (Balance, Odds)
# 2. Check Criteria. (Find desirable bets)
# 3. Place bet.

### First step is to retrieve your balance from the API. 
# Start by creating the url and headers needed to perform a Get request, 
# Get request will return a JSON response with the balance information.
def get_balance(base_url, username, password):
    url = base_url + "/v1/client/balance"
    b64str = base64.b64encode("{}:{}".format(username,password).encode('utf-8'))
    headers = {'Content-length' : '0','Content-type' : 'application/json',
               'Authorization' : "Basic " + b64str.decode('utf-8')}

    req = ulib.Request(url, headers=headers)
    responseData = ulib.urlopen(req).read()
    balance = json.loads(responseData.decode('utf-8'))  # json.loads converts JSON response back to a dict.
    return balance
    
    
### Second Step. Get the odds:
# Once you've checked your balance, the next step is to gather information about the sports we are interested in. 
# Check the API for sports codes, in this example we will use "15" which represents american football, and is given as a default parameter.

def get_sport_odds(base_url, username, password, sport = '15'):
# Get odds is very similar to get balance, but the sport information is added to the URL, and the response is a little different
# Note the variables included in the url after the "?", specifying a sport and odds format.
    url = base_url + '/v1/odds?sportId=' + str(sport) + '&oddsFormat=DECIMAL'
    b64str = base64.b64encode("{}:{}".format(username,password).encode('utf-8'))
    headers = {'Content-length' : '0', 'Content-type' : 'application/json',
               'Authorization' : "Basic " + b64str.decode('utf-8')}

    req = ulib.Request(url, headers=headers)
    responseData = ulib.urlopen(req).read()
    odds = json.loads(responseData.decode('utf-8'))
    return odds
    
### Third Step. Check Criteria
# After retrieving the balance info and some odds it's time to search the odds to find a favorable betting situation. 
# For this example, lets use the when the odds are in favour of the home team.

# If you check the API, you can see the odds contain a "moneyline", and "team" entry. 
# So we want to look through all the odds until we find one where the moneyline assosciated with the home team is 
# less than 1.91 (meaning you get 91 cents profit). If it's perfectly balance, you would expect this to be 2.0, however Pinnacle takes 0.09 of each bet. Passing the dict returned in the previous method to the following function will return the first bet that meets the criteria.

#This is fairly straightforward, but looks complex due to the heirarchy of the returned values. I would recommend a debugger for this especially, as it lets you view all the entries, and navigate hierarchy.
def find_bet(all_odds):
    bet_info = {}
    favourable_odds = 1.91
    bet_info['sportId'] = all_odds['sportId']
    for i in all_odds['leagues']:
        bet_info['leagueId'] = i['id']
        for j in i['events']:
            bet_info['eventId'] = j['id']
            for k in j['periods']:
                bet_info['period'] = k['number']
                for l in k['moneyline'].keys():
                    odds = float(k['moneyline'][l])
                    if odds < favourable_odds and l == 'home':
                        bet_info['team'] = l
                        bet_info['lineId'] = k['lineId']
                        return bet_info

# Step Four. Place a Bet
#Now we have found our balance, checked odds, and returned bet info for a scenario we would like to bet one. 
#There are two sub-steps involved. Gathering additional data to place the bet with, and submitting the POST form.

# Sub-step 1.Gather Required Bet Info
# Gather more information about our bet, specifically, you need to know if your side is "Team1" or "Team2". 
# This is done by using the Get Line API call, and checking if Team1 odds match our criteria. 
# If it matches, we want "Team1", if not, we retrieve "Team2" data.
# There is additional information in here too, like "minRiskStake" that we will use to verify our bet is valid.
def get_bet_info(base_url, username, password, bet, favourable_odds = 1.91):

    b64str = base64.b64encode("{}:{}".format(username,password).encode('utf-8'))
    headers = {'Content-length' : '0',
               'Content-type' : 'application/json',
               'Authorization' : "Basic " + b64str.decode('utf-8')}
    url_without_team = base_url + "/v1/line?sportId={0}&leagueId={1}&eventId={2}&periodNumber={3}&betType=MONEYLINE&OddsFormat=DECIMAL"\
            .format(bet['sportId'], bet['leagueId'], bet['eventId'],bet['period'])

    url = url_without_team + "&Team=Team1"
    req = ulib.Request(url, headers=headers)
    responseData = ulib.urlopen(req).read()
    line_info = json.loads(responseData.decode('utf-8'))
        
    if line_info['price'] < favourable_odds:
        bet['minRiskStake'] = line_info['minRiskStake']            
        bet['team'] = "Team1"
        return

    url = url_without_team + "&Team=Team2"
    req = ulib.Request(url, headers=headers)
    responseData = ulib.urlopen(req).read()
    line_info = json.loads(responseData.decode('utf-8'))
    bet['minRiskStake'] = line_info['minRiskStake']            
    bet['team'] = "Team2"

# Sub-step 2.Submitting Bet
# In this step, you build up a dict containing all the data needed for the Place Bet API call. 
# Then this dict is converted to a JSON file, and a POST is send to the designated URL.

def place_bet(base_url, username, password, bet, stake):
    
    url = base_url + "/v1/bets/place"
    b64str = base64.b64encode("{}:{}".format(username,password).encode('utf-8'))
    headers = {'Content-length' : '1',
               'Content-type' : 'application/json',
               'Authorization' : "Basic " + b64str.decode('utf-8')}

    data = {
            "uniqueRequestId":uuid.uuid4().hex,
            "acceptBetterLine": str(True),
            "stake": str(float(stake)),
            "winRiskStake":"RISK",
            "sportId":str(int(bet['sportId'])),
            "eventId":str(int(bet['eventId'])),            
            "lineId":str(int(bet['lineId'])),
            "periodNumber":str(int(bet['period'])),
            "betType":"MONEYLINE",
            "team":bet['team'],
            "oddsFormat":"DECIMAL"
    }

    req = ulib.Request(url, headers = headers)
    response = ulib.urlopen(req, json.dumps(data).encode("utf-8")).read().decode()
    response = json.loads(response)
    print("Bet status: " + response["status"])
















