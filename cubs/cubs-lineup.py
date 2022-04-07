from email.charset import BASE64
import requests
import os
import datetime
import base64

class CubsLineup:
    def __init__(self):
        self.game_id_list = []
        self.season = "2022-regular"
        self.date = datetime.datetime.now().strftime("%Y%m%d")
        pass

    def run(self):

        basic_token = base64.b64encode(f"{os.getenv('MSF_MLB_DETAIL_ID')}:{os.getenv('MSF_MLB_DETAIL_SECRET')}".encode("ascii"))
        resp = requests.get(
            url=f"https://api.mysportsfeeds.com/v2.1/pull/mlb/{self.season}/date/{self.date}/games.json?team=CHC",
            headers={'Authorization': f'Basic {basic_token.decode("ascii")}'})
        games = resp.json().get('games')
        
        for g in games:
            self.game_id_list.append(g.get('schedule').get('id'))
        
        for id in self.game_id_list:
            resp = requests.get(
                url=f"https://api.mysportsfeeds.com/v2.1/pull/mlb/2022-regular/games/{id}/lineup.json",
                headers={'Authorization': f'Basic {basic_token.decode("ascii")}'})
            
            away_lineup = resp.json().get('teamLineups')[0]
            home_lineup = resp.json().get('teamLineups')[1]

                        
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

            print(away_starters)

            home_lineup_positions = home_lineup.get('expected').get('lineupPositions')
            
            home_lineup_starters = [p for p in home_lineup_positions if p.get('position').startswith('B') or p.get('position') == 'P']
            home_starters = {}
            home_starters[1] = [b for b in home_lineup_starters if b.get('position') == 'BO1']
            home_starters[2] = [b for b in home_lineup_starters if b.get('position') == 'BO2']
            home_starters[3] = [b for b in home_lineup_starters if b.get('position') == 'BO3']
            home_starters[4] = [b for b in home_lineup_starters if b.get('position') == 'BO4']
            home_starters[5] = [b for b in home_lineup_starters if b.get('position') == 'BO5']
            home_starters[6] = [b for b in home_lineup_starters if b.get('position') == 'BO6']
            home_starters[7] = [b for b in home_lineup_starters if b.get('position') == 'BO7']
            home_starters[8] = [b for b in home_lineup_starters if b.get('position') == 'BO8']
            home_starters[9] = [b for b in home_lineup_starters if b.get('position') == 'BO9']        
            home_starters[0] = [b for b in home_lineup_starters if b.get('position') == 'P']

            print(home_starters)

            post_headers = {"muteHttpExceptions": True}
            print(away_starters)
            print(home_starters)



if __name__ == "__main__":
    CubsLineup().run()
