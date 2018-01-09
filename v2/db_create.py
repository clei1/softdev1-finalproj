import sqlite3, hashlib

f = "data/game.db"
db = sqlite3.connect(f)
c = db.cursor()

def tables():
    users = "CREATE TABLE IF NOT EXISTS users(user TEXT, password TEXT)"
    c.execute(users)

    games = "CREATE TABLE IF NOT EXISTS games(gameID INTEGER, user TEXT, score INTEGER, dictator BOOLEAN)"
    c.execute(games)

    userCards = "CREATE TABLE IF NOT EXISTS userCards(gameID INTEGER, user TEXT, card TEXT)"
    c.execute(userCards)

    whiteDecks = "CREATE TABLE IF NOT EXISTS whiteDecks(gameID INTEGER, card TEXT)"
    c.execute(whiteDecks)

    blackDecks = "CREATE TABLE IF NOT EXISTS blackDecks(gameID INTEGER, card TEXT)"
    c.execute(blackDecks)

    cardsOnBoard = "CREATE TABLE IF NOT EXISTS cardsOnBoard(gameID INTEGER, user TEXT, card TEXT)"
    c.execute(cardsOnBoard)

tables()

db.commit()
db.close()
