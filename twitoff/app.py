from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user

def create_app():

    app = Flask(__name__)
    
    # DB config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # register DB with app
    DB.init_app(app)


    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home Page', users=users)


    @app.route('/reset')
    def reset():
        # Drop all DB tables
        DB.drop_all()
        # Recreate all db tables according to schema in models.py
        DB.create_all()
  
        return render_template('base.html', title='Reset Database')

    @app.route('/update')
    def update():
        # Get list of all users
        users = User.query.all()
        usernames = [user.username for user in users]

        for username in usernames:
            add_or_update_user(username)
            
        return render_template('base.html', title='Users updated')
    
    @app.route('/user', methods =['POST'])
    @app.route('/user/<username>', methods =['GET'])
    def user(username=None, message=''):
        # Assigning username
        username = username or request.values['user_name']
        
        try:
            # Displaying message after user has been added
            if request.method == 'POST':
                add_or_update_user(username)
                message = f'User {username} has been successfully added!'
            
            # Get tweets
            tweets = User.query.filter(User.username==username).one().tweets

        except Exception as e:
            message = f'Error adding {username}: {e}'
            tweets = []
        
        return render_template('user.html', title=username, tweets=tweets, message=message)
        
    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])
        hypo_tweet = request.values['tweet_text']
        
        if user0 == user1:
            message = 'Cannot compare user to themselves'
        else:
            pred = predict_user(user0, user1, hypo_tweet)
            
            # Get into if statement if pred is user1
            if pred:
                message = f'"{hypo_tweet}" is more likely to be said by {user1} than {user0}'
            else:
                message = f'"{hypo_tweet}" is more likely to be said by {user0} than {user1}'
        
        return render_template('prediction.html', title='Prediction', message=message)
        
    return app