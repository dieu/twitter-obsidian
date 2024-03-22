#!/usr/bin/env python3
import os
import sys
import logging

from twitter.process import walk_bookmarks

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    bookmarks_dir = sys.argv[1]
    tweet_dir = sys.argv[2]
    if not os.path.exists(bookmarks_dir):
        print(f"No bookmark folder found {bookmarks_dir}")
        sys.exit(1)
    elif not os.path.exists(tweet_dir):
        print(f"No tweet folder found {tweet_dir}")
        sys.exit(1)
    else:
        for (bookmark_dir, bookmark) in walk_bookmarks(bookmarks_dir):
            logging.info(f"processing {len(bookmark)} bytes from {bookmark_dir}")
            relative_dir = os.path.relpath(bookmark_dir, bookmarks_dir)
            tweet_md = os.path.join(tweet_dir, relative_dir) + ".md"

            os.makedirs(os.path.dirname(tweet_md), exist_ok=True)
            
            logging.info(f"writing {len(bookmark)} bytes to {tweet_md}")

            with open(tweet_md, "w") as md_file:
                md_file.write(bookmark)
            sys.exit(1)
 