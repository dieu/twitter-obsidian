import re
import requests

from twitter.bookmark import Bookmark

OBSIDIAN_DATE_FORMAT = "%Y-%m-%d"

def thread_template(bookmark: Bookmark, tail: list[Bookmark]) -> str:
    mentions = [mention['name'] for mark in [bookmark] + tail for mention in mark.mentions]
    tail_template = "\n".join([f""" 
{embed(bookmark)}

![](https://twitter.com/{bookmark.author.name}/status/{bookmark.tweet_id})
""" for bookmark in tail])
    
    hashtags = set(
        [hashtag.lower() for hashtag in bookmark.hashtags] + 
        [hashtag.lower() for bookmark in tail for hashtag in bookmark.hashtags if bookmark.hashtags]
    )
    
    return f"""---
author: {bookmark.author.name}
date: {bookmark.date_bookmarked.strftime(OBSIDIAN_DATE_FORMAT)}
tags: [{', '.join(hashtags)}]
mentions: [{', '.join(mentions)}]
---

{embed(bookmark)}

![](https://twitter.com/{bookmark.author.name}/status/{bookmark.tweet_id})

{tail_template}
"""

def single_template(bookmark: Bookmark) -> str:
    return f"""---
tags: [{', '.join(bookmark.hashtags)}]
author: {bookmark.author.name}
date: {bookmark.date_bookmarked.strftime(OBSIDIAN_DATE_FORMAT)}
mentions: [{', '.join([mention['name'] for mention in bookmark.mentions])}]
---

{embed(bookmark)}

![](https://twitter.com/{bookmark.author.name}/status/{bookmark.tweet_id})
"""

def embed(bookmark: Bookmark) -> str:
    oembed_url = f"https://publish.twitter.com/oembed?dnt=true&omit_script=1&url=https://twitter.com/{bookmark.author.name}/status/{bookmark.tweet_id}"
    oembed = requests.get(oembed_url).json()    
    original_html = oembed['html']
    extented_html = replace_content(original_html, bookmark)
    image_html = replace_image(extented_html, bookmark)
    return f"""
<details>
<summary>Tweet</summary>
{image_html.strip()}
</details>
""".strip()

def replace_content(html: str, bookmark: Bookmark) -> str:
    content = bookmark.content.replace("\n", "<br>")
    
    parts_to_replace = ""
    for part in content.split(" "):
        parts_to_replace += part + " "
        if parts_to_replace not in html:
            parts_to_replace = parts_to_replace[:-1]
            break
    parts_to_replace = parts_to_replace + "…"

    return html.replace(parts_to_replace, content)

def replace_image(html: str, bookmark: Bookmark) -> str:
    if not bookmark.images:
        return html
    else:
        matches = re.finditer(r'(<a href="(.*?)">(.*?)</a>)', html)
        html_with_local_images = html
        for match in matches:
            if 'pic.twitter.com' in match.group(3):
                img_url = requests.head(match.group(2)).headers['location']
                img_num = int(img_url.split("/photo/")[-1])
                if img_num in bookmark.images:
                    html_with_local_images = html_with_local_images.replace(
                        match.group(0), 
                        f"""<div><div src="{bookmark.images[img_num]}" class="internal-embed"></div></div>"""
                    )
        return html_with_local_images