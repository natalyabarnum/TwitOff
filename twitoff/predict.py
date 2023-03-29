from sklearn.linear_model import LogisticRegression
import numpy as np
from .models import User
from .twitter import vectorize_tweets

def predict_user(user0_username, user1_username, hypo_tweet):
    # Grab users from DB
    user0 = User.query.filter(User.username==user0_username).one()
    user1 = User.query.filter(User.username==user1_username).one()
    
    # Get word embed
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])
    
    # Vertically stacking arrays (X_train set)
    X_train = np.vstack([user0_vects, user1_vects])
    
    # Making zeros and ones (Y_train set)
    zeros = np.zeros(user0_vects.shape[0])
    ones = np.ones(user1_vects.shape[0])
    
    y_train = np.concatenate([zeros, ones])
    
    # Performing Log Reg
    log_reg = LogisticRegression().fit(X_train, y_train)
    
    # Vectorize hypo_tweet
    hypo_tweet_vect = vectorize_tweets(hypo_tweet)
    hypo_vect_reshape = hypo_tweet_vect.reshape(1,-1)
    
    # Make prediction
    pred = log_reg.predict(hypo_vect_reshape)
    return pred[0]