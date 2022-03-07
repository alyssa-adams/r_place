import pickle
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

"""
# ---- count frequencies of rules between snapshots ----

# need to save each frequency count separately for memory handling

with open('rules.p', 'rb') as f:
    rules = pickle.load(f)

# for each dt, just get sorted list of rule freq
for t, dt in enumerate(rules.keys()):

    print(t)

    # save to dict for now, then after these are made, stitch together into one df for plotting
    freqs_all = {}

    # get frequency distribution
    freqs = list(dict(rules[dt]).values())
    freqs.sort(reverse=True)

    # add each value as row to df
    for i, f in enumerate(freqs):

        to_append = [dt, i, f]
        freqs_all[i] = to_append

    # pickle that df
    with open('freq_dfs/freqs_all_' + str(t) + '.p', 'wb') as handle:
        pickle.dump(freqs_all, handle)
"""

# ----- load in all those frequencies and stitch together into single df -----

files = os.listdir('freq_dfs')

# sort by number, not alphabetical
files = list(map(lambda x: (int(x.split('_')[2].split('.')[0]), x), files))
files.sort(key=lambda y: y[0])

# load in files
freqs = []

for file in files:

    file = file[1]

    file_n = int(file.split('_')[2].split('.')[0])

    # pickle that df
    with open(os.path.join('freq_dfs', file), 'rb') as f:
        freqs_all = pickle.load(f)

    # add to df
    f = pd.DataFrame.from_dict(freqs_all, orient='index', columns=['ts', 'rank', 'freq'])
    f['Time'] = file_n
    freqs.append(f)
    print(file)

# too many lines! Only take every 100th line
freqs = freqs[::10]

# cat list of dfs
df = pd.concat(freqs)
df = df.reset_index()

# plot as lineplot
sns.lineplot(data=df, x="rank", y="freq", hue="Time", palette="flare")

plt.xlabel("Ranked rule")
plt.ylabel("Frequency")
plt.xscale('log')
plt.yscale('log')

plt.savefig('rule_freq.png')
plt.clf()
