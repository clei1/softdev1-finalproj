import sqlite3, hashlib

f = "../data/game.db"
db = sqlite3.connect(f)
c = db.cursor()

def tables():
    users = "CREATE TABLE IF NOT EXISTS users(user TEXT, password TEXT)"
    c.execute(users)

    games = "CREATE TABLE IF NOT EXISTS games(gameID INTEGER, user TEXT, score INTEGER, dictator BOOLEAN, roundDone BOOLEAN, total INT, goal INT, status INT)"
    c.execute(games)

    userCards = "CREATE TABLE IF NOT EXISTS userCards(gameID INTEGER, user TEXT, card TEXT)"
    c.execute(userCards)

    whiteDecks = "CREATE TABLE IF NOT EXISTS whiteDecks(gameID INTEGER, card TEXT)"
    c.execute(whiteDecks)

    blackDecks = "CREATE TABLE IF NOT EXISTS blackDecks(gameID INTEGER, card BLOB)"
    c.execute(blackDecks)

    cardsOnBoardWhite = "CREATE TABLE IF NOT EXISTS cardsOnBoardWhite(gameID INTEGER, user TEXT, card TEXT)"
    c.execute(cardsOnBoardWhite)

    cardsOnBoardBlack = "CREATE TABLE IF NOT EXISTS cardsOnBoardBlack(gameID INTEGER, user TEXT, card TEXT)"
    c.execute(cardsOnBoardBlack)

    currentRound = "CREATE TABLE IF NOT EXISTS currentRound(gameID INTEGER, card TEXT, winning BOOLEAN)"
    c.execute(currentRound)

    seen = "CREATE TABLE IF NOT EXISTS seen(gameID INTEGER, numPlayers INTEGER,  user TEXT)"
    c.execute(seen)

    

tables()

db.commit()
db.close()
