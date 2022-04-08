from email.charset import BASE64
import requests
import os
import datetime
import base64
import json
from dateutil import tz, parser
import sys

class CubsLineup:
    def __init__(self):
        self.game_id_list = []
        self.season = "2022-regular"
        self.date = datetime.datetime.now().strftime("%Y%m%d")


    def run(self):

        basic_token = base64.b64encode(f"{os.getenv('MSF_MLB_DETAIL_ID')}:{os.getenv('MSF_MLB_DETAIL_SECRET')}".encode("ascii"))
        resp = requests.get(
            url=f"https://api.mysportsfeeds.com/v2.1/pull/mlb/{self.season}/date/{self.date}/games.json?team=CHC",
            headers={'Authorization': f'Basic {basic_token.decode("ascii")}'})
        try:
            games = resp.json().get('games')
        except:
            print("Cannot get game info")
            sys.exit(1)
        
        for g in games:
            self.game_id_list.append(g.get('schedule').get('id'))
        
        for id in self.game_id_list:
            resp = requests.get(
                url=f"https://api.mysportsfeeds.com/v2.1/pull/mlb/2022-regular/games/{id}/lineup.json",
                headers={'Authorization': f'Basic {basic_token.decode("ascii")}'})
            
            response = resp.json()
            away_lineup = response.get('teamLineups')[0]
            home_lineup = response.get('teamLineups')[1]

            cubs_home_away = "home" if response.get('game').get('homeTeam').get('abbreviation') == 'CHC' else "away"
            opponnent_abbr = response.get('game').get('awayTeam').get('abbreviation') if response.get('game').get('homeTeam').get('abbreviation') == "CHC" else response.get('game').get('homeTeam').get('abbreviation')
                        
            away_lineup_positions = away_lineup.get('expected').get('lineupPositions')
            
            away_lineup_starters = [p for p in away_lineup_positions if p.get('position').startswith('B') or p.get('position') == 'P' ]
            away_starters = {}
            away_starters[1] = [b for b in away_lineup_starters if b.get('position') == 'BO1']
            away_starters[2] = [b for b in away_lineup_starters if b.get('position') == 'BO2']
            away_starters[3] = [b for b in away_lineup_starters if b.get('position') == 'BO3']
            away_starters[4] = [b for b in away_lineup_starters if b.get('position') == 'BO4']
            away_starters[5] = [b for b in away_lineup_starters if b.get('position') == 'BO5']
            away_starters[6] = [b for b in away_lineup_starters if b.get('position') == 'BO6']
            away_starters[7] = [b for b in away_lineup_starters if b.get('position') == 'BO7']
            away_starters[8] = [b for b in away_lineup_starters if b.get('position') == 'BO8']
            away_starters[9] = [b for b in away_lineup_starters if b.get('position') == 'BO9']
            away_starters[0] = [b for b in away_lineup_starters if b.get('position') == 'P']
            home_lineup_positions = home_lineup.get('expected').get('lineupPositions')      

            home_lineup_starters = [p for p in home_lineup_positions if p.get('position').startswith('B') or p.get('position') == 'P']
            home_starters = {}
            home_starters[0] = [b for b in home_lineup_starters if b.get('position') == 'P']
            home_starters[1] = [b for b in home_lineup_starters if b.get('position') == 'BO1']
            home_starters[2] = [b for b in home_lineup_starters if b.get('position') == 'BO2']
            home_starters[3] = [b for b in home_lineup_starters if b.get('position') == 'BO3']
            home_starters[4] = [b for b in home_lineup_starters if b.get('position') == 'BO4']
            home_starters[5] = [b for b in home_lineup_starters if b.get('position') == 'BO5']
            home_starters[6] = [b for b in home_lineup_starters if b.get('position') == 'BO6']
            home_starters[7] = [b for b in home_lineup_starters if b.get('position') == 'BO7']
            home_starters[8] = [b for b in home_lineup_starters if b.get('position') == 'BO8']
            home_starters[9] = [b for b in home_lineup_starters if b.get('position') == 'BO9']        

            if cubs_home_away == 'home':
                cubs_lineup = home_starters.copy()
                cubs_lineup['opposing_sp'] = away_starters[0]

            else:
                cubs_lineup = away_starters.copy()
                cubs_lineup['opposing_sp'] = home_starters[0]
    
            discord_fields = []

            time = parser.parse(response.get('game').get('startTime'))
            from_tz = tz.gettz('UTC')
            to_tz = tz.gettz('America/Chicago')

            central = time.replace(tzinfo=from_tz).astimezone(to_tz).strftime("%I:%m %p")            

            discord_fields.append(
                {
                    "name": "Game Time",
                    "value": f"{datetime.datetime.now().strftime('%A, %B %d, %Y')} at {central}"
                }
            )

            discord_fields.append(
                {
                    "name": f"Cubs SP",
                    "value": f"{cubs_lineup[0][0].get('player').get('firstName')} {cubs_lineup[0][0].get('player').get('lastName')}",
                    "inline": True
                }
            )

            discord_fields.append(
                {
                    "name": f"{opponnent_abbr} SP",
                    "value": f"{cubs_lineup['opposing_sp'][0].get('player').get('firstName')} {cubs_lineup['opposing_sp'][0].get('player').get('lastName')}",
                    "inline": True
                }
            )
            cubs_lineup.pop('opposing_sp')
            cubs_lineup.pop(0)
            good_cubs_lineup = {}
            for item in cubs_lineup:
                good_cubs_lineup[item] = cubs_lineup[item][0]

            for index in good_cubs_lineup:

                player = good_cubs_lineup.get(index)
                discord_fields.append(
                    {
                        "name": index if index != 0 else "Cubs SP",
                        "value": f"{player.get('player').get('position')} | {player.get('player').get('firstName')} {player.get('player').get('lastName')}" 
                    }
                )

            discord_payload = {
                "username": "Lineup-Bot",
                "avatar_url": "https://www.kindpng.com/picc/m/121-1214433_transparent-cubs-clipart-chicago-cubs-svg-free-hd.png",
                "embeds": [
                    {
                        "title": "Cubs Lineup",
                        "color": "003399",
                        "fields": discord_fields,
                        "footer": {
                            "text": "built using https://birdie0.github.io/discord-webhooks-guide/discord_webhook.html"
                        }
                    }
                ]
            }

            self.send_to_discord(discord_payload)

            

    def send_to_discord(self, payload):
        header = {"Content-Type": "application/json"}
        resp = requests.post(url = os.getenv("DISCORD_CUBS_LINEUP_WEBHOOK_URL"), headers = header, data=json.dumps(payload))
        resp.raise_for_status

if __name__ == "__main__":
    CubsLineup().run()
