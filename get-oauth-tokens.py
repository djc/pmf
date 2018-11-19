import praw, ident, sys, bot

CLIENT_STATE = 'MozillaPlanetFeeder'
SCOPES = set(['read', 'submit'])

def main():
    api = praw.Reddit(client_id=ident.CLIENT, client_secret=ident.SECRET,
                      user_agent=bot.UA, redirect_uri=bot.REDIRECT_URI)
    url = api.auth.url(SCOPES, CLIENT_STATE, 'permanent')
    print('URL:', url)
    code = input('code: ')
    print(api.auth.authorize(code))
    print(api.user.me())

if __name__ == '__main__':
    main()
