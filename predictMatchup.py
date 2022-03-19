import sys
from leagueDataExtractor import load_settings, connect, getMatchupData, close

if __name__ == "__main__":
    
    try:
        user, password = load_settings()
        driver = connect({'user_name': user, 'password': password})
        resultInfo, oldWeekInfo, remainingWeekInfo = getMatchupData(driver)
        close(driver)
    
    except KeyboardInterrupt as ex:
        sys.exit(0)
    