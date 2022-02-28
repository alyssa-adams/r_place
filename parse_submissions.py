# reference this code for parsing: https://github.com/RolandR/place-atlas/blob/master/tools/redditcrawl.py

import json
import pickle

with open('raw_posts.pickle', 'rb') as handle:
    raw_posts = pickle.load(handle)



for submission in reddit.subreddit('placeAtlas').new(limit=220):
    # print(dir(submission))
    if (submission.link_flair_text == "New Entry"):
        text = submission.selftext
        text = text.replace("\"id\": 0,", "\"id\": 0,\n\t\t\"submitted_by\": \"" + submission.author.name + "\",")

        lines = text.split("\n")

        for i, line in enumerate(lines):
            if ("\"id\": 0" in line):
                lines[i] = line.replace("\"id\": 0", "\"id\": " + str(startId))
                startId = startId + 1

        text = "\n".join(lines)

        outfile.write(text + ",")
        print("written " + submission.title)
    else:
        print("skipped " + submission.title)