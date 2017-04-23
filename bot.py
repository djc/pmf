import praw, feedparser
import ident
import sys, os, urllib

UA = 'MozillaPlanetFeeder-0.1, by /u/Manuzhai'
HEADERS = {'User-Agent': 'MozillaPlanetFeeder-0.1'}
REDIRECT_URI = 'http://dirkjan.ochtman.nl/reddit/'
SOURCE = 'http://planet.mozilla.org/atom.xml'
DEBUG = os.isatty(sys.stdout.fileno())
REDDITS = ['MozillaTech', 'mozilla']

def reddit():
	api = praw.Reddit(client_id=ident.CLIENT, client_secret=ident.SECRET,
	                  user_agent=UA, refresh_token=ident.REFRESH,
	                  disable_update_check=True)
	return api

def entries():
	if DEBUG: print('retrieving feed items...')
	feed = feedparser.parse(SOURCE)
	for entry in feed['entries']:
		yield entry['title'], entry['link']

def submitted(sub):
	if DEBUG: print('retrieving reddit items (%s)...' % r)
	return {item.url for item in sub.new(limit=100)}

def canonicalize(url):
	if 'feedproxy.google.com' not in url:
		return url
	try:
		req = urllib.request.Request(url, headers=HEADERS)
		return urllib.request.urlopen(req).url
	except urllib.error.URLError as e:
		return ''
	except urllib.error.HTTPError as e:
		return e.url

def wrangle(url):
	return url.replace('&', '&amp;')

def submit(sub, title, link):
	try:
		return sub.submit(title, url=link)
	except praw.errors.AlreadySubmitted:
		return None

if __name__ == '__main__':
	api = reddit()
	links = [(t, canonicalize(l)) for (t, l) in entries()]
	for r in REDDITS:
		sub = api.subreddit(r)
		done = submitted(sub)
		for title, link in links:
			if not link: continue
			if title and wrangle(link) not in done:
				res = submit(sub, title, link)
				if res is not None and DEBUG:
					print(res)
