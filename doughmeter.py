#!/home/pi/.virtualenvs/doughmeter/bin/python

import yahoofantasyfootball
import time
import datetime
import settings
import sys

def gametime(d=None):
	if d is None:
		d = datetime.datetime.now()
	if d.weekday()==6: # Sunday
		return (d.hour>=13)
	elif d.weekday()==0: # Monday -- account for early morning hours!
		return (d.hour<3) or (d.hour>18)
	elif d.weekday()==3: # Thursday
		return (d.hour>18)
	elif d.weekday()==4: # Friday
		return (d.hour<3)

def calculate_sleep_delay():
	if gametime():
		return 60
	else:
		# will it be gametime in the next hour?
		n = datetime.datetime.now()
		for i in range(0,60):
			if gametime(n + datetime.timedelta(minutes=i)):
				return (i * 60)
		
		return 60 * 60

def main():
	c = None
	y = None

	DEBUG = '--debug' in sys.argv	

	if DEBUG:
		print 'Initializing... (DEBUG)'
	else:
		print 'Initializing...'
		import calibrate
		c = calibrate.load_calibrators()
	
	y = yahoofantasyfootball.YahooFantasyFootball(settings.YAHOO_LEAGUE_URL)

	while True:
		if DEBUG:
			print 'reloading HTML...'
		y.refresh()
		if DEBUG:
			print 'reprocessing...'
		y.process()
		if DEBUG:
			print y.scores
		
		score = None
		try:
			score = y.get_score_differential(settings.TEAM_NAME)
		except:
			if DEBUG:
				print 'Failed to extract score'
			score = None

		try:
			rank = y.get_standing(settings.TEAM_NAME)
		except:
			if DEBUG:
				print 'Failed to extract rank'
			rank = None

		if score is not None:
			if DEBUG:
				print 'Score differential: %d' % (score)
			else:
				if score<0:
					c[6].set(0)
					c[5].set(abs(score))
				else:
					c[5].set(0)
					c[6].set(abs(score))

		if rank is not None:
			if DEBUG:
				print 'Rank: %d' % (rank)
			else:
				c[1].set(rank)

		delay = calculate_sleep_delay()
		if DEBUG:
			print 'Sleeping for %d seconds...' % delay
		time.sleep(delay)

if __name__ == '__main__':
	main()
	
	
	
