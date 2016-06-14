import praw, feedparser
import urlparse
import ident
import sys, os, urllib2

UA = 'MozillaPlanetFeeder-0.1, by /u/Manuzhai'
HEADERS = {'User-Agent': 'MozillaPlanetFeeder-0.1'}
REDIRECT_URI = 'http://dirkjan.ochtman.nl/reddit/'
SOURCE = 'http://planet.mozilla.org/atom.xml'
DEBUG = os.isatty(sys.stdout.fileno())
REDDITS = ['MozillaTech', 'mozilla']

def reddit():
	api = praw.Reddit(UA, 'reddit', disable_update_check=True)
	api.set_oauth_app_info(ident.CLIENT, ident.SECRET, 'something')
	api.set_access_credentials({'read', 'submit'}, ident.ACCESS,
	                           ident.REFRESH)
	api.refresh_access_information()
	return api

def entries():
	if DEBUG: print 'retrieving feed items...'
	feed = feedparser.parse(SOURCE)
	for entry in feed['entries']:
		yield entry['title'], entry['link']

def submitted(api, r):
	mt = api.get_subreddit(r)
	if DEBUG: print 'retrieving reddit items (%s)...' % r
	return {item.url for item in mt.get_new(limit=100)}

def canonicalize(url):
	if 'feedproxy.google.com' not in url:
		return url
	try:
		return urllib2.urlopen(urllib2.Request(url, headers=HEADERS)).url
	except urllib2.URLError as e:
		return ''
	except urllib2.HTTPError as e:
		return e.url

def wrangle(url):
	return url.replace('&', '&amp;')

def submit(api, r, title, link):
	try:
		return api.submit(r, title, url=link)
	except praw.errors.AlreadySubmitted:
		return None

if __name__ == '__main__':
	api = reddit()
	links = [(t, canonicalize(l)) for (t, l) in entries()]
	for r in REDDITS:
		done = submitted(api, r)
		for title, link in links:
			if not link: continue
			if title and wrangle(link) not in done:
				res = submit(api, r, title, link)
				if res is not None and DEBUG:
					print res
