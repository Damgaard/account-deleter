# Copyright (C) 2013 Andreas Damgaard Pedersen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

import time

import praw
import requests
import sqlite3

import authentication
from account_deleter.settings import DATABASES

UA = """Reddit Account Nuker by u/_Daimon_."""


def authorization_url():
    """The url users will be sent to to authorize us to nuke their account."""
    base_url = 'https://ssl.reddit.com/api/v1/authorize/'
    # The state parameter is to protect against CSRF. But we don't care about
    # that. Pretty hard to do anything bad to an already nuked account.
    params = {'client_id': authentication.CLIENT_ID, 'response_type': 'code',
              'redirect_uri': authentication.REDIRECT_URI,
              'state': 'Dont Care', 'scope': 'identity,history',
              'refreshable': 'temporary'}
    request = requests.Request('GET', base_url, params=params)
    return request.prepare().url


def index(request):
    """Requesting the home page."""
    context = {'auth_url': authorization_url()}
    return render(request, 'deleter/index.html', context)


def insert_into_db(reddit_session, username):
    """Insert information about the soon to be nuked user to the database."""
    # TODO: Unhardcode database name
    with sqlite3.connect(DATABASES['default']['NAME']) as con:
        cur = con.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS
                    Redditors(Id INTEGER PRIMARY KEY AUTOINCREMENT,
                              Username TEXT, Access_token TEXT, Gained_at INT)
        """)
        access_token = reddit_session.access_token
        now = int(time.time())
        query = """INSERT INTO Redditors(Username, Access_token, Gained_at)
                   VALUES ('{}' , '{}', {});""".format(username, access_token,
                                                       now)
        cur.execute(query)


def nuking_account(request):
    """The page where we reply with success/failure."""
    user = None
    error_message = None
    try:
        r = praw.Reddit(UA)
        r.set_oauth_app_info(client_id=authentication.CLIENT_ID,
                             client_secret=authentication.CLIENT_SECRET,
                             redirect_uri=authentication.REDIRECT_URI)
        r.get_access_information(request.GET['code'])
        user = r.get_me().name
        insert_into_db(r, user)
    except praw.errors.OAuthInvalidGrant:
        error_message = ("Cannot exchange code. Did you accept within 60 "
                         "minutes or have you already used this code?")
    except MultiValueDictKeyError:
        error_message = ("Didn't receive all parameters. Did you visit this "
                         "page directly?")
    except Exception:
        if settings.DEBUG:
            raise
        else:
            error_message = "Unknown error type encountered. Try again?"
    context = {'identity': user, 'error_message': error_message}
    return render(request, 'deleter/nuking_account.html', context)
