import os
import time
import praw
import json
import pickle
from datetime import datetime


with open('api_keys.json') as json_file:
    api_keys = json.load(json_file)

# run every hour, on the hour
while True:

    now = datetime.now()
    minute_int = now.minute

    # trigger every hour, at some minute
    if minute_int == 9:

        print('Start!')

        # make client
        reddit = praw.Reddit(client_id=api_keys['client_id'], client_secret=api_keys['client_secret'],
                             user_agent=api_keys['user_agent'])

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
        dt_string = now.strftime("%d-%m-%Y-%H:%M:%S")

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

        print('Success!')
