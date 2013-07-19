import praw, feedparser
import urlparse
import ident
import sys, os, urllib2

UA = 'MozillaPlanetFeeder-0.1, by /u/Manuzhai'
HEADERS = {'User-Agent': 'MozillaPlanetFeeder-0.1'}
SOURCE = 'http://planet.mozilla.org/atom.xml'
DEBUG = os.isatty(sys.stdout.fileno())

def reddit():
	api = praw.Reddit(UA, 'reddit', disable_update_check=True)
	api.set_oauth_app_info(ident.CLIENT, ident.SECRET, 'something')
	api.refresh_access_information(ident.REFRESH)
	return api

def entries():
	if DEBUG: print 'retrieving feed items...'
	feed = feedparser.parse(SOURCE)
	for entry in feed['entries']:
		yield entry['title'], entry['link']

def submitted(api):
	mt = api.get_subreddit('MozillaTech')
	if DEBUG: print 'retrieving reddit items...'
	return {item.url for item in mt.get_new(limit=100)}

def canonicalize(url):
	if 'feedproxy.google.com' not in url:
		return url
	try:
		return urllib2.urlopen(urllib2.Request(url, headers=HEADERS)).url
	except urllib2.HTTPError as e:
		return e.url

def wrangle(url):
	return url.replace('&', '&amp;')

def submit(api, title, link):
	try:
		return api.submit('MozillaTech', title, url=link)
	except praw.errors.AlreadySubmitted:
		return None

if __name__ == '__main__':
	api = reddit()
	done = submitted(api)
	for title, link in entries():
		link = canonicalize(link)
		if title and wrangle(link) not in done:
			res = submit(api, title, link)
			if res is not None and DEBUG:
				print res
