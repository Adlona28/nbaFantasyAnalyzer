from clock import load_settings, connect, processMatchup, close


def run():

	user, password = load_settings()
	driver = connect({'user_name': user, 'password': password})
	getMatchupData(driver)
	close(driver)

	