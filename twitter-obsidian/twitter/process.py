import json
import os
import logging

from collections.abc import Callable, Iterator

from twitter.bookmark import Bookmark
from twitter.markdown import thread_template, single_template

from ai.llama import tags

IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "svg", "webp"]

def walk_bookmark(folder_path: str) -> str:
    image_files = [
        # tweet_id, image_num, path
        (int(image.split('_')[-2]), int(image.split('_')[-1].split('.')[0]), image)
        for image in os.listdir(folder_path) if image.split('.')[-1] in IMAGE_EXTENSIONS
    ]
    bookmarks: list[Bookmark] = [
        Bookmark(json.load(open(os.path.join(folder_path, file), 'r'))) 
        for file in os.listdir(folder_path) if file.endswith("_metadata.json")
    ]
    for bookmark in bookmarks:
        bookmark.images = {
            image[1]: image[2] for image in image_files if image[0] == bookmark.tweet_id
        }
        
        if not bookmark.hashtags:
            bookmark.hashtags = tags(bookmark)
            logging.info(f"tags for {bookmark.tweet_id} are {bookmark.hashtags}")

    if len(bookmarks) > 1: 
        head = next((bookmark for bookmark in bookmarks if bookmark.tweet_id == bookmark.conversation_id), None)
        tail = [bookmark for bookmark in bookmarks if bookmark.tweet_id != bookmark.conversation_id]
        
        def sort_bookmarks(bookmarks: list[Bookmark], tweet_id: Bookmark) -> list[Bookmark]:
            sorted_bookmarks = []
            while bookmarks:
                for bookmark in bookmarks[:]:  
                    if bookmark.reply_id == tweet_id:
                        sorted_bookmarks.append(bookmark)
                        bookmarks.remove(bookmark) 
                        tweet_id = bookmark.tweet_id
                        break
            return sorted_bookmarks
        if head:
            sorted_tail = sort_bookmarks(tail, head.tweet_id)
        else:
            sorted_tail = tail
        return thread_template(head, sorted_tail)
    else:
        return single_template(bookmarks[0])

def walk_bookmarks(folder_path: str) -> Iterator[(str, str)]:
    logging.info(f"walking bookmarks in {folder_path}")
    yield from walk_folder(folder_path, walk_bookmark)

def walk_folder(folder_path: str, process_function: Callable[[str], str]) -> Iterator[(str, str)]:
    for root, dirs, files in os.walk(folder_path):
        sorted_dirs = sorted(dirs, key=lambda dir: os.path.getmtime(os.path.join(root, dir)))
        logging.info(f"walking sub-directories {len(sorted_dirs)} directories in {root}")
        for dir in sorted_dirs:
            absolute_path = os.path.join(root, dir)
            yield (absolute_path, process_function(absolute_path))