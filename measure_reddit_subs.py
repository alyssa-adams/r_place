from datetime import datetime
import time
import pickle
import praw
import os

# place_posts
# personal use script
# sPqxFkV3XZL6hGxEgf6oow
# secret: raxVHkjrp5hsNsxQjWwjo6izyXRRTg

minute_int = 0

# run every hour, on the hour
while True:

    now = datetime.now()
    minute_int = now.minute

    if minute_int == 0:

        # make client
        reddit = praw.Reddit(client_id='sPqxFkV3XZL6hGxEgf6oow', client_secret='raxVHkjrp5hsNsxQjWwjo6izyXRRTg', user_agent='place_posts')

        # save results to list
        types = ['hot', 'new', 'top', 'rising']
        raw_posts = {}

        for type in types:

            if type == 'hot':
                posts = reddit.subreddit('place').hot(limit=1000)
            elif type == 'new':
                posts = reddit.subreddit('place').new(limit=1000)
            elif type == 'rising':
                posts = reddit.subreddit('place').rising(limit=1000)
            elif type == 'top':
                posts = reddit.subreddit('place').top(limit=100, time_filter='hour')
            else:
                posts = None

            raw_posts[type] = list(posts)

            # don't ddos api
            time.sleep(1)
            print('.')

        # get current time
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # pickle dict of posts
        with open(os.path.join('2022_place_posts', dt_string), 'wb') as handle:
            pickle.dump(raw_posts, handle)

        # also get the hot 1000 posts containing r/place
        types = ['hot', 'top']
        raw_posts = {}

        for type in types:
            posts = reddit.subreddit("all").search("r/place", sort=types, limit=None, time_filter='hour')
            raw_posts[type] = list(posts)

        # pickle list of lists
        with open(os.path.join('2022_mentioned_posts', dt_string), 'wb') as handle:
            pickle.dump(raw_posts, handle)

        time.sleep(60)


