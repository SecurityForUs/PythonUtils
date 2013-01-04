#!/usr/bin/env python

"""
This script was made to handle writing new posts for Pelican (using the RST format).

It makes use of asking only the essentials, and then storing the RST file in "content/".

Of course, this can be modified, but I'm too lazy right now to focus on that.

Once you run this script and give the information, you just need to open the file and enter the body of your post.

Pretty simple, nice and fluid IMO.

Creator: Eric Hansen <ehansen@securityfor.us>
"""

tags = raw_input("Enter a comma-separated list of tags/topics about this post: ")
title = raw_input("The title of this post is: ")
author = raw_input("The author is: ")
excerpt = raw_input("Summary of this post: ")

def make_slug(txt):
    import re
    tmp = txt
    text = str(tmp).lower()

    bad = re.compile("[^a-z0-9_\s-]")
    cleanse = re.compile("[\s-]+")
    convert = re.compile("[\s_]")

    slug = bad.sub("", text)
    slug = cleanse.sub(" ", slug)
    slug = convert.sub("-", slug)

    return slug

slug = make_slug(title)

cloud = tags.split(",")

for id,tag in enumerate(cloud):
    cloud[id] = make_slug(tag)

tags = ",".join(cloud)

from time import strftime

fn = "%s.rst" % (slug)

ts = strftime("%Y-%m-%d %H:%M")

msg = "%s\n" % (title)
msg = "%s%s\n" % (msg, "=" * len(title))
msg = "%s:date: %s\n" % (msg, ts)
msg = "%s:tags: %s\n" % (msg, tags)
msg = "%s:slug: %s\n" % (msg, slug)
msg = "%s:excerpt: %s\n" % (msg, excerpt)
msg = "%s:author: %s\n\n" % (msg, author)

# Update this to reflect the path of where your Pelican blog is
fp = open("content/%s" % (fn), "w")
fp.write(msg)
fp.close()

print "Blog template written to content/%s" % (fn)
