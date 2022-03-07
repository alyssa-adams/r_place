# reference this code for parsing: https://github.com/RolandR/place-atlas/blob/master/tools/redditcrawl.py

import json
import pickle
import re, json, ast

with open('raw_posts.pickle', 'rb') as handle:
    raw_posts = pickle.load(handle)

polygons = {}

for submissions in raw_posts:

    # convert to json
    submissions = json.loads(submissions)
    submissions = submissions['data']

    # skip if empty
    if len(submissions) > 0:

        # loop over submissions in this chunk
        for submission in submissions:

            try:
                submission = json.loads(submission['selftext'])
            except:
                continue

            name = submission['name']
            description = submission['description']
            website = submission['website']
            subreddit = submission['subreddit']
            center = submission['center']
            path = submission['path']

            # remove all the 0.5's
            center = ast.literal_eval(re.sub(r'\.5', '', str(center)))
            path = ast.literal_eval(re.sub(r'\.5', '', str(path)))

            # save polygon
            polygons[name] = {
                'description': description,
                'website': website,
                'subreddit': subreddit,
                'center': center,
                'path': path
            }

# pickle the polygons
with open('polygons.p', 'wb') as handle:
    pickle.dump(polygons, handle)