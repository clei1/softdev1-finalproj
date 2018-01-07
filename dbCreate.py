import sqlite3, hashlib

f = "data/game.db"
db = sqlite3.connect(f)
c = db.cursor()

def tables():
    users = "CREATE TABLE IF NOT EXISTS users(user TEXT, password TEXT)"
    c.execute(users)

    games = "CREATE TABLE IF NOT EXISTS games(gameID INTEGER, user TEXT,  score INTEGER, dictator BOOLEAN, cards TEXT)"
    c.execute(games)

    decks = "CREATE TABLE IF NOT EXISTS decks(gameID INTEGER, white TEXT, black TEXT, onBoard TEXT)"
    c.execute(decks)

tables()

db.commit()
db.close()
