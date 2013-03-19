import praw, feedparser
import urlparse
import ident

UA = 'MozillaPlanetFeeder-0.1, by /u/Manuzhai'
SOURCE = 'http://planet.mozilla.org/atom.xml'

def reddit():
	api = praw.Reddit(UA, 'reddit')
	api.set_oauth_app_info(ident.CLIENT, ident.SECRET, 'something')
	api.refresh_access_information(ident.REFRESH)
	return api

def entries():
	print 'retrieving feed items...'
	feed = feedparser.parse(SOURCE)
	for entry in feed['entries']:
		yield entry['title'], entry['link']

def submitted(api):
	mt = api.get_subreddit('MozillaTech')
	print 'retrieving reddit items...'
	return {item.url for item in mt.get_new(limit=100)}

def wrangle(url):
	return url.replace('&', '&amp;')

def submit(api, title, link):
	return api.submit('MozillaTech', title, url=link)

if __name__ == '__main__':
	api = reddit()
	done = submitted(api)
	for title, link in entries():
		if title and wrangle(link) not in done:
			print submit(api, title, link)
