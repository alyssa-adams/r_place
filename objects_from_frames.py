import ast
import pickle
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, random

# load in polygon frames
with open('polygons.p', 'rb') as handle:
    polygons = pickle.load(handle)

# load in snapshots
with open('snapshots.p', 'rb') as handle:
    snapshots = pickle.load(handle)

# add into frames
frames = {}

# only do a few polygons
polygons = dict(random.sample(polygons.items(), 10))

# connect the dots between points in frames to get set of pixels
for polygon in polygons:

    corners = polygons[polygon]['path']
    frame_pixels = []
    previous_corner = False

    for corner in corners:

        # add corner pixel
        frame_pixels.append(corner)

        # skip connecting to first one (no previous corner)
        if previous_corner:

            # see if x changed
            if previous_corner[0] != corner[0]:

                # fill in pixels in-between
                pixel_path = [[x, corner[1]] for x in range(min(previous_corner[1], corner[1]), max(previous_corner[1], corner[1]))]

            # else its y that changed
            else:

                # fill in pixels in-between
                pixel_path = [[corner[0], y] for y in range(min(previous_corner[1], corner[1]), max(previous_corner[1], corner[1]))]

            # add the pixels
            [frame_pixels.append(pixel) for pixel in pixel_path]

        # reset the previous corner
        previous_corner = corner

    # get unique set of pixels in path
    frame_pixels = list(map(lambda y: ast.literal_eval(y), list(set(list(map(lambda x: str(x), frame_pixels))))))

    # throw away any that are above 1000
    frame_pixels = list(filter(lambda x: x[0] <= 1000 and x[1] <= 1000, frame_pixels))

    # save to dict
    frames[polygon] = frame_pixels

# scan the set of images for a not-changing frame
frame_changes = []

for frame in frames:

    frame_applied_last = False

    for s, snapshot in enumerate(snapshots):

        frame_applied_now = [snapshots[snapshot][pixel[0], pixel[1]] for pixel in frames[frame]]

        # skip first one since comparing change between befores and afters
        if frame_applied_last:

            # mark a pixel as 1 if it's different than the previous one
            frame_diff = [0 if frame_applied_now[pixel] == frame_applied_last[pixel] else 1 for pixel in range(len(frame_applied_now))]

            # get percent diff
            frame_diff = float(sum(frame_diff))/float(len(frame_diff))

            # save to list
            frame_changes.append([frame, s, frame_diff])

        frame_applied_last = frame_applied_now

# filter out empty ones, should be 681 changes between frames
#frame_changes = dict(filter(lambda elem: len(elem[1]) == 681, frame_changes.items()))

# turn into a df for plotting
df = pd.DataFrame(frame_changes, columns=['object', 'frame', 'diff'])

# plot as lineplot
sns.set(rc={'figure.figsize': (10, 5)})
sns.lineplot(data=df, x="frame", y="diff", hue="object", legend=False)
plt.xlabel("Time (10 minute increments)")
plt.ylabel("% change of object outline")

plt.savefig('objects.png')
plt.clf()
