from settings import *
import simple_crypto
from selenium import webdriver
import cookielib
from BeautifulSoup import BeautifulSoup
from soupselect import select
import time

class YahooFantasyFootball(object):
	"""Collects information from Yahoo Fantasy Football"""
	def __init__(self, league_url):
		super(YahooFantasyFootball, self).__init__()
		self.league_url = league_url

		self.phantom = webdriver.PhantomJS()
		self.phantom.set_window_size(1280, 1024)		

		self.last_refresh = None

	def get_standings(self):
		b = BeautifulSoup(self.html)

	def process(self):
		scores = {}
		matchups = []
		b = BeautifulSoup(self.html)
		for row in select(b, 'ul.Bdrbot li'):
			matchup = []
			for player in select(row, 'div.Grid-h-mid'):
				score = select(player, 'div.Fz-lg')[0].getText()
				projected = select(player, 'div.F-shade')[0].getText()
				name = select(player, 'div.Fz-sm a')[0].getText()
				scores[name] = {'score': score, 'projected': projected}
				matchup.append(name)
			matchups.append(matchup)

		self.scores = scores
		self.matchups = matchups

	def refresh(self):
		
		self.phantom.get(self.league_url)
		
		if ('login' in self.phantom.title.lower()) or ('sign in to yahoo' in self.phantom.title.lower()):
		
			submit_control = None
			
			for e in self.phantom.find_elements_by_tag_name('input'):
				
				# login
				if e.get_attribute('name') in ('login', 'id'):
					e.send_keys(YAHOO_USERNAME)
				
				# password
				if e.get_attribute('name') in ('passwd', 'password'):
					e.send_keys(simple_crypto.decrypt(YAHOO_PASSWORD))
				
				# 'remember me'
				if e.get_attribute('name') in ('persistent',):
					if e.get_attribute('value')=='y':
						self.phantom.get_element_by_id('pLabelC').click()
				
				# mobile login form?
				if e.get_attribute('name') in ('.save', '__submit'):
						submit_control = e

			# ugh it's a <button>
			if submit_control is None:
				for e in self.phantom.find_elements_by_tag_name('button'):
					if e.get_attribute('name') in ('.save', '__submit'):
						submit_control = e

			if submit_control is not None:
				submit_control.click()
				time.sleep(5)
			else:
				raise Exception('Submission control not found!')

			self.phantom.save_screenshot('/Users/tomlee/Desktop/ffball.png')

		self.last_refresh = time.time()
		self.html = self.phantom.page_source
	


if __name__ == '__main__':
	y = YahooFantasyFootball(YAHOO_LEAGUE_URL)
	y.refresh()	
	y.process()

	print y.scores
	for m in y.matchups:
		print m


	# f = open('output.html', 'w')
	# f.write(h)
	# f.close()
	# 	