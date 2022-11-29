import flask 
from flask import request
from flask.globals import g

import mysql.connector as MySQLConnector

def init_db():
    g.db = MySQLConnector.connect(
        host = "localhost",
        user = "root",
        password = "alunoaluno",
        database = "bemtivi"
    )
    return g.db

def get_db():
    if "db" not in g:
        g.db = init_db()

    return g.db

def init_app():
    app = flask.Flask(__name__)

    with app.app_context():
        init_db()

    return app

app = init_app()

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@app.route("/")
def index():
    db = get_db()

    return "Is connected? %s" %("Yes" if db.is_connected else "No")

@app.route("/createtbs")
def create_table():

    db = get_db()
    c = db.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS tweet (
            id int not null auto_increment,
            content text,
            retweet tinyint(1),
            owner int,
            parent int,
            primary key(id)
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id int not null auto_increment,
            nickname varchar(64),
            email varchar(64),
            password varchar(64),
            primary key(id)
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS user_likes(
            user_id int not null,
            tweet_id int not null,
            primary key(user_id, tweet_id)
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS user_follows(
            user_follows_id int not null,
            user_id int not null,
            primary key(user_follows_id, user_id)
        );
    """)
    
    c.execute("""
        ALTER TABLE tweet 
        ADD CONSTRAINT FOREIGN KEY(owner) REFERENCES user(id); 
    """)

    c.execute("""
        ALTER TABLE tweet
        ADD CONSTRAINT FOREIGN KEY(parent) REFERENCES tweet(id);
    """)

    c.execute("""
        ALTER TABLE user_likes
        ADD CONSTRAINT FOREIGN KEY(user_id) REFERENCES user(id);
    """)

    c.execute("""
        ALTER TABLE user_likes
        ADD CONSTRAINT FOREIGN KEY(tweet_id) REFERENCES tweet(id);
    """)

    c.execute("""
        ALTER TABLE user_follows
        ADD CONSTRAINT FOREIGM KEY(user_follows_id) REFERENCES user(id);
    """)

    c.execute("""
        ALTER TABLE user_follows
        ADD CONSTRAINT FOREIGN KEY(user_id) REFERENCES user(id);
    """)
    

    c.close()
    db.close()

@app.route("/insertinto")
def insert_into():
    
    db = get_db()
    c = db.cursor()

    users = [
        (1,"vinicius7m","vinicius@gmail.com","123456"),
        (2,"user1","user@gmail.com","123456"),
        (3,"user12","user1@gmail.com","123456"),
        (4,"user123","user12@gmail.com","123456"),
    ]

    tweets = [
        (1, "Teste de post", 0, 1, "NULL"),
        (2, "Teste de post 1", 0, 2, "NULL"),
        (3, "Teste de post 2", 0, 3, 1),
        (4, "Teste de post 3", 0, 4, 2)
    ]

    user_likes = [
        (1, 2),
        (1, 3),
        (2, 4),
        (4, 1)        
    ]

    user_follows = [
        (1, 3),
        (1, 2),
        (2, 4),
        (4, 1)
    ]

    sql_users = "INSERT INTO user VALUES(%s,%s,%s,%s)"
    sql_tweets = "INSERT INTO user VALUES(%s,%s,%s,%s,%s)"
    sql_likes = "INSERT INTO user VALUES(%s,%s)"
    sql_follows = "INSERT INTO user VALUES(%s,%s)"

    c.executemany(sql_users, users)
    c.executemany(sql_tweets, tweets)
    c.executemany(sql_likes, user_likes)
    c.executemany(sql_follows, user_follows)

    db.commit()

    c.close()
    db.close()

    return c.rowcount