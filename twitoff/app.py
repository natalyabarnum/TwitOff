from flask import Flask, render_template
from .models import DB, User, Tweet

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


    @app.route('/beef')
    def beef():
        return render_template('base.html', title='Beef Page')


    @app.route('/reset')
    def reset():
        # Drop all DB tables
        DB.drop_all()
        # Recreate all db tables according to schema in models.py
        DB.create_all()
        return "database has been reset"

    @app.route('/populate')
    def populate():
        # Creates two fake users in DB
        talya = User(id=1, username='Talya')
        DB.session.add(talya)
        brian = User(id=2, username='Brian')
        DB.session.add(brian)
        jordan = User(id=3, username='Jordan')
        DB.session.add(jordan)
        alina = User(id=4, username='Alina')
        DB.session.add(alina)
        anjanette = User(id=5, username='Anjanette')
        DB.session.add(anjanette)
        evan = User(id=6, username='Evan')
        DB.session.add(evan)
        
        # Create two fake tweets in DB
        tweet1 = Tweet(id=1, text="talya tweeted this", user=talya)
        DB.session.add(tweet1)
        tweet2 = Tweet(id=2, text="brian tweeted this", user=brian)
        DB.session.add(tweet2)
        tweet3 = Tweet(id=3, text="jordan tweeted this", user=jordan)
        DB.session.add(tweet3)
        tweet4 = Tweet(id=4, text="hi", user=alina)
        DB.session.add(tweet4)
        tweet5 = Tweet(id=5, text="o.o", user=anjanette)
        DB.session.add(tweet5)
        tweet6 = Tweet(id=6, text="loser", user=evan)
        DB.session.add(tweet6)

        # Save changes just made to DB
        # "commit" changes
        DB.session.commit()
        return "DB has been populated"
        
        
    return app