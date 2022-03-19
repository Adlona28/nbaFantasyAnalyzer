import requests
import pandas as pd
from bs4 import BeautifulSoup

season='2022'

def _getNbaStats():

    url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'.format(season)
       
    r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')

    table=soup.find_all(class_="full_table")

    head=soup.find(class_="thead")

    column_names_raw=[head.text for item in head][0]
    column_names_polished=column_names_raw.replace("\n",",").split(",")[2:-1]

    columnsNeeded =['Player', 'FG', 'FGA', '3P', 'FT', 'FTA', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PTS']

    players=[]

    for i in range(len(table)):
        player_=[]

        for td in table[i].find_all("td"):
            player_.append(td.text)
            
        players.append(player_)
        
    df=pd.DataFrame(players, columns=column_names_polished).set_index("Player")
    df.drop(df.columns.difference(columnsNeeded), axis=1, inplace=True)
    #cleaning the player's name from occasional special characters
    df.index=df.index.str.replace('*', '', regex=True)
    df.index=df.index.str.replace('ü', 'u', regex=True)
    df.index=df.index.str.replace('Ş', 'S', regex=True)
    df.index=[' '.join([name.split()[0][0]+'.'] + name.split()[1:]) for name in df.index]
    df.columns=['FGM', 'FGA', '3PTM', 'FTM', 'FTA', 'REB', 'AST', 'ST', 'BLK', 'TO', 'PTS']
    df = df[['FGM', 'FGA', 'FTM', 'FTA', '3PTM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']]

    return df

def _getPlayerName(player):
    return ' '.join(player.split('Note')[1].split('-')[0].split()[0:-1])

def _playsToday(inputString):
        return any(char.isdigit() for char in inputString)

def _plays(player):
    return player[1]

def _getRemainingPlayers(remainingWeekInfo):

    remainingPlayersA={}
    remainingPlayersB={}

    for info in remainingWeekInfo:
        info.drop(info.columns.difference(['Pos','Player','Player.1']), axis=1, inplace=True)
        info = info.set_index('Pos')
        info = info.drop('IL')
        info = info.dropna()
        listPlayerA = [[_getPlayerName(i), _playsToday(i)] for i in info['Player'].values]
        listPlayerB = [[_getPlayerName(i), _playsToday(i)] for i in info['Player.1'].values]

        for player in listPlayerA:
            if not _plays(player):
                continue

            if player[0] in remainingPlayersA:
                remainingPlayersA[player[0]] += 1
            else:
                remainingPlayersA[player[0]] = 1

        for player in listPlayerB:
            if not _plays(player):
                continue

            if player[0] in remainingPlayersB:
                remainingPlayersB[player[0]] += 1
            else:
                remainingPlayersB[player[0]] = 1

    return remainingPlayersA, remainingPlayersB
        
def _cleanResultInfo(resultInfo):

    resultInfo.columns=resultInfo.columns.str.replace('*', '', regex=True)
    resultInfo[['FGM','FGA']] = resultInfo['FGM/A'].str.split('/',expand=True)
    resultInfo[['FTM','FTA']] = resultInfo['FTM/A'].str.split('/',expand=True)
    columnsNeeded =['Team', 'FGM', 'FGA', 'FTM', 'FTA', '3PTM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']
    resultInfo.drop(resultInfo.columns.difference(columnsNeeded), axis=1, inplace=True)
    resultInfo = resultInfo.set_index('Team')
    resultInfo = resultInfo[['FGM', 'FGA', 'FTM', 'FTA', '3PTM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']]
    return resultInfo


def predictResult(resultInfo, remainingWeekInfo):
    
    resultInfo = _cleanResultInfo(resultInfo)
    stats = _getNbaStats()
    remainingPlayersA, remainingPlayersB = _getRemainingPlayers(remainingWeekInfo)
    remainingA = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for player in remainingPlayersA:
        playerRemainingStats = [remainingPlayersA[player]*float(x) for x in stats.loc[player].values]
        remainingA = [round(x + y, 1) for x, y in zip(remainingA, playerRemainingStats)]
    print(remainingA)

    remainingB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for player in remainingPlayersB:
        print(player)
        print(remainingPlayersB[player])
        print(stats.loc[player].values)
        playerRemainingStats = [remainingPlayersB[player]*float(x) for x in stats.loc[player].values]
        remainingB = [round(x + y, 1) for x, y in zip(remainingB, playerRemainingStats)]
    print(remainingB)

    

if __name__ == "__main__":

    resultInfo = pd.read_csv('../resultInfo.csv')
    remainingWeekInfo = [pd.read_csv('../remainingWeekInfo0.csv'), pd.read_csv('../remainingWeekInfo1.csv')]
    predictResult(resultInfo,remainingWeekInfo)