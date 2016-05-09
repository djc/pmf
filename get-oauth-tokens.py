import praw, ident, sys, bot

CLIENT_STATE = 'MozillaPlanetFeeder'
SCOPES = set(['read', 'submit'])

def main():
    api = praw.Reddit(bot.UA, 'reddit')
    api.set_oauth_app_info(ident.CLIENT, ident.SECRET, bot.REDIRECT_URI)
    url = api.get_authorize_url(CLIENT_STATE, SCOPES, True)
    print 'URL:', url
    code = raw_input('code: ')
    access_info = api.get_access_information(code)
    print access_info

if __name__ == '__main__':
    main()
