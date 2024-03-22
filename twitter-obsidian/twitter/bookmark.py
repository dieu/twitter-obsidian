from datetime import datetime

class User:
    def __init__(self, user) -> None:
        self.id = user["id"]
        self.name = user["name"]
        self.nick = user["nick"]
        self.location = user["location"]
        self.date = user["date"]
        self.verified = user["verified"]
        self.profile_banner = user["profile_banner"]
        self.profile_image = user["profile_image"]
        self.favourites_count = user["favourites_count"]
        self.followers_count = user["followers_count"]
        self.friends_count = user["friends_count"]
        self.listed_count = user["listed_count"]
        self.media_count = user["media_count"]
        self.statuses_count = user["statuses_count"]
        self.description = user["description"]
        self.url = user.get("url", None)
    
    def __eq__(self, other):
        if isinstance(other, User):
            return (
                self.id == other.id and
                self.name == other.name and
                self.nick == other.nick and
                self.location == other.location and
                self.date == other.date and
                self.verified == other.verified and
                self.profile_banner == other.profile_banner and
                self.profile_image == other.profile_image and
                self.favourites_count == other.favourites_count and
                self.followers_count == other.followers_count and
                self.friends_count == other.friends_count and
                self.listed_count == other.listed_count and
                self.media_count == other.media_count and
                self.statuses_count == other.statuses_count and
                self.description == other.description and
                self.url == other.url
            )
        return False


class Bookmark:
    def __init__(self, bookmark) -> None:
        self.tweet_id = bookmark["tweet_id"]
        self.retweet_id = bookmark["retweet_id"]
        self.quote_id = bookmark["quote_id"]
        self.reply_id = bookmark["reply_id"]
        self.conversation_id = bookmark["conversation_id"]
        self.date = datetime.strptime(bookmark["date"], "%Y-%m-%d %H:%M:%S")
        self.author = User(bookmark["author"])
        self.user = User(bookmark["user"])
        self.lang = bookmark["lang"]
        self.source = bookmark["source"]
        self.sensitive = bookmark["sensitive"]
        self.favorite_count = bookmark["favorite_count"]
        self.quote_count = bookmark["quote_count"]
        self.reply_count = bookmark["reply_count"]
        self.retweet_count = bookmark["retweet_count"]
        self.hashtags = bookmark.get("hashtags", [])
        self.mentions = bookmark.get("mentions", [])
        self.content = bookmark["content"]
        self.quote_by = bookmark.get("quote_by", None)
        self.date_bookmarked = datetime.strptime(bookmark["date_bookmarked"], "%Y-%m-%d %H:%M:%S")
        if self.date_bookmarked >= self.date or self.date_bookmarked == datetime(1970, 1, 1, 0, 0):
            self.date_bookmarked = self.date
        else:
            self.date_bookmarked = bookmark["date_bookmarked"] 
        self.count = bookmark["count"]
        self.category = bookmark["category"]
        self.subcategory = bookmark["subcategory"]

    def __eq__(self, other):
        if isinstance(other, Bookmark):
            return (
                self.tweet_id == other.tweet_id and
                self.retweet_id == other.retweet_id and
                self.quote_id == other.quote_id and
                self.reply_id == other.reply_id and
                self.conversation_id == other.conversation_id and
                self.date == other.date and
                self.author == other.author and
                self.user == other.user and
                self.lang == other.lang and
                self.source == other.source and
                self.sensitive == other.sensitive and
                self.favorite_count == other.favorite_count and
                self.quote_count == other.quote_count and
                self.reply_count == other.reply_count and
                self.retweet_count == other.retweet_count and
                self.hashtags == other.hashtags and
                self.mentions == other.mentions and
                self.content == other.content and
                self.quote_by == other.quote_by and
                self.date_bookmarked == other.date_bookmarked and
                self.count == other.count and
                self.category == other.category and
                self.subcategory == other.subcategory
            )
        return False
