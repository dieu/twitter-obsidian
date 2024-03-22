import ollama
import logging
import time
import json

from twitter.bookmark import Bookmark

TEXT_MODEL = "gemma:2b"

def tags(bookmark: Bookmark):
    start_time = time.perf_counter()
    response = ollama.chat(
        model=TEXT_MODEL, 
        format='json',
        options=ollama.Options(
            temperature=0,
            seed=123
        ),
        messages=[
            {
                'role': 'assistant',
                'content': 'What hashtags should I use for this tweet?',
            },
            {
                'role': 'user',
                'content': bookmark.content,
            }
        ]
    )
    end_time = time.perf_counter()
    try:
        tags = [hashtag.replace('#', '') for hashtag in json.loads(response['message']['content'])['hashtags']]
    except json.JSONDecodeError:
        tags = []
    logging.info(f"for generated {tags} in {end_time - start_time:0.4f} seconds")
    return tags