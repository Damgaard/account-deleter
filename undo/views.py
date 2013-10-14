from django.shortcuts import render

import requests

import authentication


def authorization_url():
    """The url users will be sent to to authorize us to nuke their account."""
    base_url = 'https://ssl.reddit.com/api/v1/authorize/'
    # The state parameter is to protect against CSRF. But we don't care about
    # that. Pretty hard to do anything bad to an already nuked account.
    params = {'client_id': authentication.CLIENT_ID, 'response_type': 'code',
              'redirect_uri': authentication.REDIRECT_URI,
              'state': 'Dont Care', 'scope': ['identity', 'edit', 'history'],
              'refreshable': 'temporary'}
    request = requests.Request('GET', base_url, params=params)
    return request.prepare().url


def index(request):
    context = {'auth_url': authorization_url()}
    return render(request, 'undo/index.html', context)
