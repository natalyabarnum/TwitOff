from os import getenv
import not_tweepy as tweepy
from .models import DB, Tweet, User
import spacy

# API keys
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Connect to twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username):
    '''take username and pull tweets from the API for user.
    If it already exists, check to see if there are any new
    tweets from user that we don't have and add new tweets
    '''
    try:
        # Get user info
        twitter_user = TWITTER.get_user(screen_name=username)
        
        # Checking if user exists in DB
        # Is there a user with same ID
        # If user doesn't exists, create one
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, username=username)

        # Add user to DB
        # Won't readd user
        DB.session.add(db_user)
        
        # Get user tweets (in list)
        tweets = twitter_user.timeline(count=200,
                                    exclude_replies=True,
                                    include_rts=False,
                                    tweet_mode='extended',
                                    since_id=db_user.newest_tweet_id)

        # Update newest_tweet id if there are new tweets
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        
        # Add indiviudal tweets to DB
        for tweet in tweets:
            tweet_vector = vectorize_tweets(tweet.full_text)
            db_tweet = Tweet(id=tweet.id,
                            text=tweet.full_text[:300],
                            vect=tweet_vector,
                            user_id=db_user.id)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print("Error processing {username}: {e}")
        raise e
    
    else:
        # Commit changes
        DB.session.commit()
        
nlp = spacy.load('my_model/')

# Function returns word embedding
def vectorize_tweets(tweet_text):
    return nlp(tweet_text).vector