import json
import requests
import time
import pickle

start = 1483232400
end = 1646011617
epochs = end-start
n_months_since_april_2017 = 57
n_slices = n_months_since_april_2017*30  # to ensure we are getting at least 1000 posts per day
epochs_per_slice = epochs / n_slices

# save results to list
raw_posts = []

for _ in range(n_slices):

    start_epoch = start
    end_epoch = int(start_epoch + epochs_per_slice)

    url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=placeAtlas&sort=desc&sort_type=created_utc&after=' \
          + str(start_epoch) + '&before=' + str(end_epoch) + '&size=10000'
    r = requests.get(url)
    posts = r.text
    raw_posts.append(posts)

    # reset start place
    start = end_epoch

    # don't ddos reddit
    time.sleep(1)
    print('.')

# pickle list
with open('pickles/atlas_posts.p', 'wb') as handle:
    pickle.dump(raw_posts, handle)
