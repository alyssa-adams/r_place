import pickle
import numpy as np
import pandas as pd
from collections import Counter


# if frames are small, get rules
# also can get rule freq as a function of dt

with open('pickles/snapshots_2017.p', 'rb') as f:
    snapshots = pickle.load(f)

# just look at rule changes frame by frame every 10 minutes
ns = [1, 2]  # neighborhood size of nearest-neighbor rule space

for n in ns:

    for i, ts in enumerate(list(snapshots.keys()), start=1):  # skip the first one [1:340]

        # get before/after image to get rule sets
        image_now = pd.DataFrame(snapshots[ts]['canvas_now']).fillna(-1)
        image_now = image_now.astype(int)
        image_now = image_now.to_numpy()

        image_before = pd.DataFrame(snapshots[list(snapshots.keys())[i-1]]['canvas_now']).fillna(-1)
        image_before = image_before.astype(int)
        image_before = image_before.to_numpy()

        # other information
        n_tiles = snapshots[ts]['n_tiles']
        n_users = snapshots[ts]['n_users']

        # ignore edge cases
        image_now_trimmed = image_now[n:-n, n:-n]

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
                if n == 1:
                    neighborhood = np.array([[image_before[r+1, c-1], image_before[r+1, c], image_before[r+1, c+1]],
                                             [image_before[r, c-1], image_before[r, c], image_before[r, c+1]],
                                             [image_before[r-1, c-1], image_before[r-1, c], image_before[r-1, c+1]]])
                if n == 2:
                    neighborhood = np.array([[image_before[r+2, c-2], image_before[r+2, c-1], image_before[r+2, c], image_before[r+2, c+1], image_before[r+2, c+2]],
                                             [image_before[r+1, c-2], image_before[r+1, c-1], image_before[r+1, c], image_before[r+1, c+1], image_before[r+1, c+2]],
                                             [image_before[r, c-2], image_before[r, c-1], image_before[r, c], image_before[r, c+1], image_before[r, c+2]],
                                             [image_before[r-1, c-2], image_before[r-1, c-1], image_before[r-1, c], image_before[r-1, c+1], image_before[r-1, c+2]],
                                             [image_before[r-2, c-2], image_before[r-2, c-1], image_before[r-2, c], image_before[r-2, c+1], image_before[r-2, c+2]]])

                # save rule to list
                rules_dt.append(str((neighborhood.tolist(), outcome)))

        # save to dict
        # have to save histogram instead (too big for memory)
        data = {'rule_freq': Counter(rules_dt), 'n_tiles': n_tiles, 'n_users': n_users, 'ts': ts}
        print(ts)

        # pickle the rules
        with open('pickles/rules/rules_n' + str(n) + '_2017_' + str(i) + '.p', 'wb') as handle:
            pickle.dump(data, handle)

        # stitch these together into a single dic later-- pickle cannot handle so much memory
