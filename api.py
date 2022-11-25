import flask 
from flask import request
from flask.globals import g

import mysql.connector as MySQLConnector

def init_db():
    g.db = MySQLConnector.connect(
        host = "localhost",
        user = "root",
        password = "alunoaluno"
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
        ALTER TABLE pet 
        ADD CONSTRAINT FOREIGN KEY(id_responsavel) REFERENCES responsavel(id) 
    """)

    c.close()
    db.close()