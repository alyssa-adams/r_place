import re
import os
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ---- count frequencies of rules between snapshots ----

ns = [2]

for n in ns:

    # list files for this n
    files = list(os.listdir('pickles/rules'))
    files = list(filter(lambda x: re.search('_n' + str(n), x), files))

    rules = {}

    # stitch together all the different rules pickles into a single dict
    for file in files:
        with open('pickles/rules/' + str(file), 'rb') as f:
            print(file)
            if file == 'rules_n2_2017_448.p': continue
            data = pickle.load(f)
            ts = data['ts']

        rules[ts] = data

    # for each dt, just get sorted list of rule freq
    for t, ts in enumerate(rules.keys()):

        print(t)

        # save to dict for now, then after these are made, stitch together into one df for plotting
        freqs_all = {}

        # get frequency distribution
        freqs = list(dict(rules[ts]['rule_freq']).values())
        freqs.sort(reverse=True)

        # other information
        n_tiles = rules[ts]['n_tiles']
        n_users = rules[ts]['n_users']

        # add each value as row to df
        for i, f in enumerate(freqs):

            to_append = [ts, i, f, n_tiles, n_users]
            freqs_all[i] = to_append

        # pickle that df
        with open('freq_dfs/freqs_all_' + str(t) + '_n' + str(n) + '.p', 'wb') as handle:
            pickle.dump(freqs_all, handle)

    # stitch these together
    files = os.listdir('freq_dfs')

    # only get the files for this n
    files = list(filter(lambda x: re.search('_n' + str(n), x), files))

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
        f = pd.DataFrame.from_dict(freqs_all, orient='index', columns=['ts', 'rank', 'freq', 'n_pixels', 'n_users'])
        f['Snapshot'] = file_n
        freqs.append(f)
        print(file)

    # ----- Now we make a plot -----

    # too many lines! Only take every 10th line
    freqs = freqs[::10]

    # cat list of dfs
    df = pd.concat(freqs)
    df = df.reset_index()

    # plot as many lineplots
    sns.lineplot(data=df, x="rank", y="freq", hue="Snapshot", size="n_users", palette="Spectral", alpha=0.8)
    plt.title("n = " + str(n))
    plt.xlabel("Ranked rule")
    plt.ylabel("Frequency")
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('figures/rule_freq_n' + str(n) + '_users.png')
    plt.clf()

    # plot as many lineplots
    sns.lineplot(data=df, x="rank", y="freq", hue="Snapshot", size="n_pixels", palette="Spectral", alpha=0.8, sizes=(.1, 2))
    plt.title("n = " + str(n))
    plt.xlabel("Ranked rule")
    plt.ylabel("Frequency")
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('figures/rule_freq_n' + str(n) + '_pixels.png')
    plt.clf()
