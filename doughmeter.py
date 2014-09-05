#!/home/pi/.virtualenvs/doughmeter/bin/python

import yahoofantasyfootball
import time
import datetime
import settings
import sys
import os
import simple_crypto

TRAVIS = os.environ.get('CONTINUOUS_INTEGRATION', 'False').upper() == 'TRUE'

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

def note_error():
    FAILURE_LOCKFILE = '/home/pi/Devel/doughmeter/FAILURE_LOCKFILE'
    if not os.path.exists(FAILURE_LOCKFILE):
        os.system("echo 'Error running doughmeter. Please fix me.' | mail -s '[doughmeter] Error' thomas.j.lee@gmail.com'")
        os.system("touch %s" % FAILURE_LOCKFILE)

def main():
    """
    >>> (rank, score) = main()
    >>> (rank > 0) and (rank < 100)
    True
    >>> (score > -5000) and (score < 500)
    True
    """

    c = None
    y = None
    
    DEBUG = ('--debug' in sys.argv) or TRAVIS
    USEPINS = (not '--nopin' in sys.argv) and not TRAVIS

    if not TRAVIS:
        if DEBUG:
            print 'Initializing... (DEBUG)'
        else:
            print 'Initializing...'
            os.system('sudo killall phantomjs') # kill some zombies
    
    if USEPINS:
        import calibrate
        c = calibrate.load_calibrators()
    
    y = yahoofantasyfootball.YahooFantasyFootball(settings.YAHOO_LEAGUE_URL, settings.YAHOO_USERNAME, simple_crypto.decrypt(settings.YAHOO_PASSWORD))

    while True:
        if DEBUG and not TRAVIS:
            print 'reloading HTML & processing it...'
        y.refresh()        
        if DEBUG and not TRAVIS:
            print y.scores
        
        score = None
        try:
            score = y.get_score_differential(settings.TEAM_NAME)
        except:
            if DEBUG:
                print 'Failed to extract score'
            score = None
            note_error()

        try:
            rank = y.get_standing(settings.TEAM_NAME)
        except:
            if DEBUG and not TRAVIS:
                print 'Failed to extract rank'
            rank = None
            note_error()

        if score is not None:
            if DEBUG and not TRAVIS:
                print 'Score differential: %d' % (score)
            if USEPINS:
                if score<0:
                    c[6].set(0)
                    c[5].set(abs(score))
                else:
                    c[5].set(0)
                    c[6].set(abs(score))

        if rank is not None:
            if DEBUG and not TRAVIS:
                print 'Rank: %d' % (rank)
            if USEPINS:
                c[1].set(rank)

        if TRAVIS:
            return (rank, score)
            break

        delay = calculate_sleep_delay()
        if DEBUG and not TRAVIS:
            print 'Sleeping for %d seconds...' % delay
        time.sleep(delay)

if __name__ == '__main__':    
    if TRAVIS:
        import doctest
        sys.exit(doctest.testmod()[0])
    else:
        main()
    
    
    
