"""
Independent Script to handle nuking a Redditor.

Continually running. Every 5 seconds, it polls the database to see if any
redditor wants to be nuked. For every redditor that does it will delete all of
their comments and submissions.
"""

import time

import praw
import sqlite3

import authentication
from reddit_undo.settings import DATABASES


def initialize_reddit_session():
    UA = """Reddit Account Nuker by u/_Daimon_."""
    r = praw.Reddit(UA)
    r.set_oauth_app_info(client_id=authentication.CLIENT_ID,
                         client_secret=authentication.CLIENT_SECRET,
                         redirect_uri=authentication.REDIRECT_URI)
    return r


def run(reddit_session):
    scope = set(['identity', 'edit', 'history'])
    with sqlite3.connect(DATABASES['default']['NAME']) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Redditors")
        for row_id, username, access_token, gained_at in cur.fetchall():
            print row_id, username
            reddit_session.set_access_credentials(scope=scope,
                                                  access_token=access_token)
            redditor = reddit_session.get_me()
            while True:
#                del_submissions = [sub for sub in redditor.get_submitted(limit=5)]
#                del_comments = [com for com in redditor.get_comments(limit=5)]
                del_submissions = []
                del_comments = []
                if all([not del_submissions, not del_comments]):
                    break
                time.sleep(reddit_session.config.cache_timeout)
            cur.execute("DELETE FROM Redditors WHERE Id == {};".format(row_id))


if __name__ == '__main__':
    reddit_session = initialize_reddit_session()
    while True:
        print "Starting a run."
        run(reddit_session)
        time.sleep(5)
