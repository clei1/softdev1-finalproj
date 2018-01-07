import sqlite3
f = "data/game.db"

def validate(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    found = c.execute("SELECT count(*) FROM users WHERE user = '%s' AND password = '%s'" % (user, password)).fetchall()
    db.commit()
    db.close()
    return (found[0][0] == 1)

def hasUsername(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    found = c.execute("SELECT count(*) FROM users WHERE user = '%s'" % (username)).fetchall()
    db.commit()
    db.close()
    return (found[0][0] == 1)

def newGameID():
    db = sqlite3.connect(f)
    c = db.cursor()
    max = c.execute("SELECT MAX(gameID) FROM games").fetchall()
    db.commit()
    db.close()
    return maxID[0][0] + 1

def addUser(user, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES('%s', '%s')" % (user, password))
    db.commit()
    db.close()

def addGame(user, whites, blacks):
    db = sqlite3.connect(f)
    c = db.cursor()
    id = newGameID()
    c.execute("INSERT INTO games VALUES('%s', '%s', '%s', '%s', '%s')" % (id, user, 0, TRUE, ''))
    c.execute("INSERT INTO decks VALUES('%s', '%s', '%s', '%s')" % (id, whiteDeck, blackDeck, ''))
    db.commit()
    db.close()

def addPlayer(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("INSERT INTO games VALUES('%s', '%s', '%s', '%s', '%s')" % (gameID, user, 0, FALSE, ''))
    db.commit()
    db.close()
