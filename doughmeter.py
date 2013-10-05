#!/home/pi/.virtualenvs/doughmeter/bin/python

import yahoofantasyfootball, calibrate, time, settings

if __name__ == '__main__':
	print 'initializing...'
	y = yahoofantasyfootball.YahooFantasyFootball(settings.YAHOO_LEAGUE_URL)
	c = calibrate.load_calibrators()
	while True:
		print 'reloading HTML...'
		y.refresh()
		print 'reprocessing...'
		y.process()
		print y.scores
		score = None
		try:
			score = y.get_score_differential('Cologne Centurions')
		except:
			score = None

		if score is not None:
			print score
			if score<0:
				c[6].set(0)
				c[5].set(abs(score))
			else:
				c[5].set(0)
				c[6].set(abs(score))
		time.sleep(60)
