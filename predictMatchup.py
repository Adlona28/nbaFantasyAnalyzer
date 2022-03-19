import sys
import csv
from leagueDataExtractor import load_settings, connect, getMatchupData, close
from dataAnalyzer import predictResult

if __name__ == "__main__":
    
    try:
        user, password = load_settings()
        driver = connect({'user_name': user, 'password': password})
        resultInfo, oldWeekInfo, remainingWeekInfo = getMatchupData(driver)
        close(driver)
        resultInfo.to_csv('resultInfo.csv')
        for i in range(len(oldWeekInfo)):
        	oldWeekInfo[i].to_csv('oldWeekInfo'+str(i)+'.csv')

        for i in range(len(remainingWeekInfo)):
        	remainingWeekInfo[i].to_csv('remainingWeekInfo'+str(i)+'.csv')
        
        predictResult(resultInfo, remainingWeekInfo)
    
    except KeyboardInterrupt as ex:
        sys.exit(0)
    