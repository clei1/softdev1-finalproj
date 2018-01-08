import sqlite3, random
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
    if max[0][0] is None:
        return 0
    return max[0][0] + 1

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
    c.execute("INSERT INTO games VALUES('%s', '%s', '%s', '%s')" % (id, user, 0, 1))
    for each in whites:
        c.execute("INSERT INTO whiteDecks VALUES('%s', '%s')" % (id, each))
    for each in blacks:
        c.execute("INSERT INTO blackDecks VALUES('%s', '%s')" % (id, each))
    db.commit()
    db.close()

def addPlayer(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("INSERT INTO games VALUES('%s', '%s', '%s', '%s')" % (gameID, user, 0, 0))
    db.commit()
    db.close()

def drawBlack(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    cards = c.execute("SELECT * FROM blackDecks WHERE gameID = '%s' AND user = '%s'" % (gameID, user)).fetchall()
    print cards
    db.commit()
    db.close()

addGame("Jim", "a,b,c", "a,b,c")
addPlayer(0, "Bob")
db = sqlite3.connect(f)
c = db.cursor()
c.execute("SELECT * FROM games")
data = c.fetchall()
print(data)
