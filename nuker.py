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
from account_deleter.settings import DATABASES


def main():
    reddit_session = initialize_reddit_session()
    print "Initialized and starting main loop"
    while True:
        run(reddit_session)
        time.sleep(5)


def initialize_reddit_session():
    """Return a connected reddit session."""
    r = praw.Reddit("Reddit Account Nuker by u/_Daimon_.")
    r.set_oauth_app_info(client_id=authentication.CLIENT_ID,
                         client_secret=authentication.CLIENT_SECRET,
                         redirect_uri=authentication.REDIRECT_URI)
    return r


def run(reddit_session):
    """Delete all content made by redditors in the database."""
    scope = set(['identity', 'edit', 'history'])
    with sqlite3.connect(DATABASES['default']['NAME']) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Redditors")
        for row_id, username, access_token, gained_at in cur.fetchall():
            print "Starting nuking of {} at row_id {}".format(username, row_id)
            reddit_session.set_access_credentials(scope=scope,
                                                  access_token=access_token)
            redditor = reddit_session.get_me()
            limit = 900
            while True:
                submissions = list(redditor.get_submitted(limit=limit)) or []
                comments = list(redditor.get_comments(limit=limit)) or []
                for sub in submissions:
                    sub.delete()
                for com in comments:
                    com.delete()
                print "Subs", submissions
                print "Com", comments
                if not (len(submissions) == limit or len(comments) == limit):
                    break
                wait_time = reddit_session.config.cache_timeout
                wait_string = "Maybe more content. Waiting "
                wait_string += "{} secs, then deleting ".format(wait_time)
                print wait_string + "another batch."
                time.sleep(wait_time)
            cur.execute("DELETE FROM Redditors WHERE Id == {};".format(row_id))
            print "Succesfully nuked {}".format(username)


if __name__ == '__main__':
    main()
