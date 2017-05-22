import config
import praw
import time
import urllib2
import json

r = praw.Reddit(username = config.username, password = config.password, client_id = config.client_id, client_secret = config.client_secret, user_agent = config.user_agent)

subreddit = r.subreddit('all')
alreadydone = []
i = 0
keywords = ['donald', 'trump']

def comment():
    global i
    lis = []
    try:
        all_comments = subreddit.comments(limit = None)
        for comment in all_comments:
            commentbody = comment.body.lower()
            has_keyword = any(string in commentbody for string in keywords)
            if has_keyword and str(comment.author) != config.username and comment.id not in alreadydone and str(comment.author) != "AutoModerator":
                alreadydone.append(comment.id)
                i += 1
                getresponse = urllib2.urlopen("https://api.whatdoestrumpthink.com/api/v1/quotes/random")
                data = json.load(getresponse)
                response = "'" + data["message"] + "'" + " - The D Man Himself"
                comment.reply(response)
                print 'comment ' + str(i) + ' successful!'
    except Exception as error:
        print 'Error recieved'
        print error
print 'searching for keywords'
while True:
    comment()
