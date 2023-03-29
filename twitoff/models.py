from flask_sqlalchemy import SQLAlchemy

# Create DB object from SQLAl

DB = SQLAlchemy()


class User(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # username column
    username = DB.Column(DB.String, nullable=False)
    # most recent teweet id
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f'User: {self.username}'

class Tweet(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # text column
    text = DB.Column(DB.Unicode(300), nullable=False)
    # store word embeddings (vectorization)
    # PickleType stores entire arrays in DB
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id column (forreign / secondary key)
    user_id = DB.Column(DB.BigInteger,DB.ForeignKey('user.id'), nullable=False)
    # user column creates two-way link between user object and tweet object
    # tweet object is now connected to user object
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    
    def __repr__(self):
        return f'User: {self.text}'