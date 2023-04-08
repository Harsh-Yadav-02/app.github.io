from flask import Flask, render_template, request
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    text = request.form['text']
    username = request.form['username']
    since = request.form['since']
    until = request.form['until']
    count = int(request.form['count'])
    retweet = request.form['retweet']
    replies = request.form['replies']
    
    tweets_list = []
    filename = ''
    
    def search(text, username, since, until, retweet, replies):
        global filename
        q = text
        if username != '':
            q += f" from:{username}"
        if until == '':
            until = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
            q += f" until:{until}"
        if since == '':
            since = datetime.datetime.strftime(datetime.datetime.strptime(until, '%Y-%m-%d') - datetime.timedelta(days=7), '%Y-%m-%d')
            q += f" since:{since}"
        if retweet == 'y':
            q += f" exclude:retweets"
        if replies == 'y':
            q += f" exclude:replies"
        if username != '' and text != '':
            filename = f"{since}_{until}_{username}_{text}.csv"
        elif username != "":
            filename = f"{since}_{until}_{username}.csv"
        else:
            filename = f"{since}_{until}_{text}.csv"
        print(q)
        
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
            if count != -1 and i >= count:
                break
            tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.lang, tweet.hashtags, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.media])
            
    search(text, username, since, until, retweet, replies)
    tweets_df = pd.DataFrame(tweets_list, columns=['DateTime', 'TweetId', 'Text', 'Username', 'Language', 'Hashtags', 'ReplyCount', 'RetweetCount', 'LikeCount', 'QuoteCount', 'Media'])
    
    tweets_df.to_csv(f'{filename}', index=False)
    
    # Uncomment the next line to display the results on a new web page
    return render_template('results.html', data=tweets_df)

if __name__ == '__main__':
    app.run(debug=True)







'''from flask import Flask, render_template, request
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import snscrape.modules.twitter as sntwitter
import datetime

# import additional libraries and functions as needed

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    print("Submit button clicked!")
    text = request.form['text']
    username = request.form['username']
    since = request.form['since']
    until = request.form['until']
    count = int(request.form['count'])
    retweet = request.form['retweet']
    replies = request.form['replies']
    
    print("Starting web scraping...")
    q = generate_query(text, username, since, until, retweet, replies)
    
    tweets_list1 = []
    
    if count == -1:
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
            tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.lang, tweet.hashtags, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.media])
    else:
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
            if i >= count:
                break
            tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.lang, tweet.hashtags, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.media])
    
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['DateTime', 'TweetId', 'Text', 'Username', 'Language', 'Hashtags', 'ReplyCount', 'RetweetCount', 'LikeCount', 'QuoteCount', 'Media'])
    
    filename = f"{text}.csv"
    tweets_df1.to_csv(filename, index=False)
    
    return "File Saved Successfully!!"
    #return render_template('results.html', data=tweets_df1)

def generate_query(text, username, since, until, retweet, replies):
    q = text
    if username != '':
        q += f" from:{username}"
    if until == '':
        until = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
        q += f" until:{until}"
    if since == '':
        since = datetime.datetime.strftime(datetime.datetime.strptime(until, '%Y-%m-%d') - datetime.timedelta(days=7), '%Y-%m-%d')
        q += f" since:{since}"
    if retweet == 'y':
        q += f" exclude:retweets"
    if replies == 'y':
        q += f" exclude:replies"
    return q

if __name__ == '__main__':
    app.run(debug=True)







from flask import Flask, render_template, request
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import snscrape.modules.twitter as sntwitter
import nltk

# import additional libraries and functions as needed

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    text = request.form['text']
    username = request.form['username']
    since = request.form['since']
    until = request.form['until']
    count = int(request.form['count'])
    retweet = request.form['retweet']
    replies = request.form['replies']
    

def search(text,username,since,until,retweet,replies):
    global filename
    q = text
    if username!='':
        q += f" from:{username}"
    if until=='':
        until = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
        q += f" until:{until}"
    if since=='':
        since = datetime.datetime.strftime(datetime.datetime.strptime(until, '%Y-%m-%d') - datetime.timedelta(days=7), '%Y-%m-%d')
        q += f" since:{since}"
    if retweet == 'y':
        q += f" exclude:retweets"
    if replies == 'y':
        q += f" exclude:replies"
    if username!='' and text!='':
        filename = f"{since}_{until}_{username}_{text}.csv"
    elif username!="":
        filename = f"{since}_{until}_{username}.csv"
    else:
        filename = f"{since}_{until}_{text}.csv"
        print(filename)
    q = search(text,username,since,until,retweet,replies)
    
    tweets_list1 = []
    
    if count == -1:
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
            tweets_list1.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username,tweet.lang,tweet.hashtags,tweet.replyCount,tweet.retweetCount, tweet.likeCount,tweet.quoteCount,tweet.media])
    else:
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
            if i>=count:
                break
            tweets_list1.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username,tweet.lang,tweet.hashtags,tweet.replyCount,tweet.retweetCount,tweet.likeCount,tweet.quoteCount,tweet.media])
    
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['DateTime', 'TweetId', 'Text', 'Username','Language','Hashtags','ReplyCount','RetweetCount','LikeCount','QuoteCount','Media'])
    filename = f"{text}.csv"
    tweets_df1.to_csv(f'{filename}',index = False)
    return "File Saved Sucessfully!!"
    #return render_template('results.html', data=tweets_df1)

if __name__ == '__main__':
    app.run(debug=True)'''
