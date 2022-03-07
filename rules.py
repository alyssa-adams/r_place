import pickle
import numpy as np
import pandas as pd
from collections import Counter

# if frames are small, get rules
# also can get rule freq as a function of dt

with open('snapshots.p', 'rb') as f:
    snapshots = pickle.load(f)

rules = {}

# just look at rule changes frame by frame every 10 minutes
n = 1
for i, ts in enumerate(list(snapshots.keys())[1:]):  # skip the first one

    # get before/after image to get rule sets
    image_now = pd.DataFrame(snapshots[ts]).fillna(-1)
    image_now = image_now.astype(int)
    image_now = image_now.to_numpy()

    image_before = pd.DataFrame(snapshots[list(snapshots.keys())[i-1]]).fillna(-1)
    image_before = image_before.astype(int)
    image_before = image_before.to_numpy()

    # ignore edge cases
    image_now_trimmed = image_now[1:-1, 1:-1]  # n

    # rules used between these two images
    rules_dt = []

    # loop over cells
    for r, row in enumerate(image_now_trimmed):
        for c, cell in enumerate(row):

            # get rule outcome
            outcome = cell
 
            # get old state of itself + neighborhood of size n = 1

            # if no neighbors
            #if n == 0:
            #    neighborhood = image_before[row, cell]
            #    continue

            # can make neighbors n and see how results change with n

            # n = 1
            neighborhood = np.array([[image_before[r+1, c-1], image_before[r+1, c], image_before[r+1, c+1]],
                                     [image_before[r, c-1], image_before[r, c], image_before[r, c+1]],
                                     [image_before[r-1, c-1], image_before[r-1, c], image_before[r-1, c+1]]])

            # save rule to list
            rules_dt.append(str((neighborhood.tolist(), outcome)))

    # save to dict
    # have to save histogram instead (too big for memory)
    rules[ts] = Counter(rules_dt)
    print(ts)

# pickle the rules
with open('rules.p', 'wb') as handle:
    pickle.dump(rules, handle)
