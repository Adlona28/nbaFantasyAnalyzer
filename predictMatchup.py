import sys
from predictMatchup import run
		
if __name__ == "__main__":
	
	try:
		run()
	
	except KeyboardInterrupt as ex:
		sys.exit(0)
	