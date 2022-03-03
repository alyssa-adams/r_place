import csv
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import pickle

# rules for r/place are here: https://www.redditinc.com/blog/how-we-built-rplace/
"""
The board must be 1000 tiles by 1000 tiles so it feels very large.
All clients must be kept in sync with the same view of the current board state, 
otherwise users with different versions of the board will have difficulty collaborating.
We should support at least 100,000 simultaneous users.
Users can place one tile every 5 minutes, so we must support an average update rate of 
100,000 tiles per 5 minutes (333 updates/s).
The project must be designed in such a way that it’s unlikely to affect the rest of the site’s normal function 
even with very high traffic to r/place.
The configuration must be flexible in case there are unexpected bottlenecks or failures. 
This means that board size and tile cooldown should be adjustable on the fly in case data sizes 
are too large or update rates are too high.
The API should be generally open and transparent so the reddit community can build on it 
(bots, extensions, data collection, external visualizations, etc) if they choose to do so.
"""

# get some nice results here: https://arxiv.org/pdf/1804.05962.pdf
# some nice analysis from Reddit: https://www.redditinc.com/blog/place-part-two/

# notes:
# do users stick to one or two places on the canvas? Jump to a new pattern? A few far patterns?
# compression of changes in an area between two snapshots, no changes is high compression

# get 2D CA rule frequency changes over time, overall and hour by hour

# import as df to sort by timestamp oldest to newest
df = pd.read_csv('place_tiles')
df = df.dropna()

# convert to timestamp, ints
df['ts'] = df['ts'].map(lambda x: datetime.strptime(x[:-4], '%Y-%m-%d %H:%M:%S.%f') if len(x[:-4]) > 19
            else datetime.strptime(x[:-4], '%Y-%m-%d %H:%M:%S'))
df['x_coordinate'] = df['x_coordinate'].map(lambda x: int(x))
df['y_coordinate'] = df['y_coordinate'].map(lambda x: int(x))
df['color'] = df['color'].map(lambda x: int(x))

# sort by time oldest to newest
df = df.sort_values(by=['ts'])
df = df.reset_index()

# make an empty image
canvas = np.empty((1000, 1000))
canvas[:] = np.NaN

# dictionary of snapshots
snapshots = {}

# set a time increment between images, in minutes
t_delta = 10

t_ten_start = df['ts'][0]

# loop over moves to take canvas snapshots at time increments
for index, row in df.iterrows():
    canvas[row['x_coordinate'], row['y_coordinate']] = row['color']

    # check to see if ten minutes have passed, if so then save image to dict
    if row['ts'] > t_ten_start + timedelta(minutes=t_delta):

        snapshots[row['ts']] = canvas
        t_ten_start = row['ts']

# pickle these snapshots
with open('snapshots.p', 'wb') as handle:
    pickle.dump(snapshots, handle)

# also pickle the df of actions
with open('df_actions.p', 'wb') as handle:
    pickle.dump(df, handle)
