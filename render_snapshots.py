import pickle
import re

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap


with open('snapshots.p', 'rb') as f:
    snapshots = pickle.load(f)

snapshot_ns = [150, 200, 250, 300, 350, 400]

"""
index	color code
0	#FFFFFF
1	#E4E4E4
2	#888888
3	#222222
4	#FFA7D1
5	#E50000
6	#E59500
7	#A06A42
8	#E5D900
9	#94E044
10	#02BE01
11	#00E5F0
12	#0083C7
13	#0000EA
14	#E04AFF
15	#820080
"""

colors = ['#FFFFFF', '#E4E4E4', '#888888', '#222222', '#FFA7D1', '#E50000', '#E59500', '#A06A42', '#E5D900',
    '#94E044', '#02BE01', '#00E5F0', '#0083C7', '#0000EA', '#E04AFF', '#820080']
cmap = LinearSegmentedColormap.from_list('yes', colors, N=16)
cmap.set_bad(color='grey')

fig = plt.figure(figsize=(20, 30))
fig.subplots_adjust(hspace=0.1, wspace=0.1)

for i, sn in enumerate(snapshot_ns, start=1):

    canvas = snapshots[list(snapshots.keys())[sn]]['canvas_now']
    ax = fig.add_subplot(3, 2, i)
    plt.imshow(canvas, cmap=cmap)
    plt.axis('off')
    plt.title('Snapshot ' + str(sn), fontsize=40)

plt.savefig('snapshots.png')
