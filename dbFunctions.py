import sqlite3, random
f = "data/game.db"

#validate 
def validate(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    found = c.execute("SELECT count(*) FROM users WHERE user = '%s' AND password = '%s'" % (user, password)).fetchall()
    db.commit()
    db.close()
    return (found[0][0] == 1)

#checks for repeated usernames
def hasUsername(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    found = c.execute("SELECT count(*) FROM users WHERE user = '%s'" % (username)).fetchall()
    db.commit()
    db.close()
    return (found[0][0] == 1)

#generates a gameID
def newGameID():
    db = sqlite3.connect(f)
    c = db.cursor()
    max = c.execute("SELECT MAX(gameID) FROM games").fetchall()
    db.commit()
    db.close()
    if max[0][0] is None:
        return 0
    return max[0][0] + 1

#adds user to users table
def addUser(user, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES('%s', '%s')" % (user, password))
    db.commit()
    db.close()

#adds user who created to games with new gameID and sets user to dictator; adds white and black decks with gameID
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

#adds user to games
def addPlayer(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("INSERT INTO games VALUES('%s', '%s', '%s', '%s')" % (gameID, user, 0, 0))
    db.commit()
    db.close()

#chooses black card randomly and removes from deck; adds to cardsOnBoard
def drawBlack(gameID,user):
    db = sqlite3.connect(f)
    c = db.cursor()
    cards = c.execute("SELECT * FROM blackDecks WHERE gameID = '%s'" % (gameID)).fetchall()
    chosen = (random.choice(cards))
    c.execute("DELETE FROM blackDecks WHERE gameID = '%s' AND card = '%s'" % (chosen[0], chosen[1]))
    c.execute("INSERT INTO cardsOnBoard VALUES ('%s', '%s', '%s')" % (gameID, user, chosen[1]))
    db.commit()
    db.close()

#chooses white card randomly and removes from deck; adds to userCards
def drawWhite(gameID,user):
    db = sqlite3.connect(f)
    c = db.cursor()
    cards = c.execute("SELECT * FROM whiteDecks WHERE gameID = '%s'" % (gameID)).fetchall()
    chosen = (random.choice(cards))
    c.execute("DELETE FROM whiteDecks WHERE gameID = '%s' AND card = '%s'" % (chosen[0], chosen[1]))
    c.execute("INSERT INTO userCards VALUES ('%s', '%s', '%s')" % (gameID, user, chosen[1]))
    db.commit()
    db.close()

#given a card, deletes from userDecks and adds to cardsOn Board
def chooseCardToPlay(gameID,user,card):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("DELETE FROM userCards WHERE gameID = '%s' AND user = '%s' AND card = '%s'" % (gameID, user, card))
    c.execute("INSERT INTO cardsOnBoard VALUES('%s','%s','%s')" % (gameID, user, card))
    db.commit()
    db.close

#given a winning card, finds player who played it, updates their score, clears cardsOnBoard for that game, calls newDictator function
def chooseWinner(gameID, card):
    db = sqlite3.connect(f)
    c = db.cursor()
    player = c.execute("SELECT * FROM cardsOnBoard WHERE gameID = '%s' AND card = '%s'" % (gameID, card)).fetchall()[0][1]
    print player
    score = c.execute("SELECT * FROM games WHERE gameID = '%s' AND user = '%s'" % (gameID, player)).fetchall()[0][2]
    print score+1
    c.execute("UPDATE games SET score = '%s' WHERE gameID = '%s' and user = '%s'" % (score+1, gameID, player))
    c.execute("DELETE FROM cardsOnBoard WHERE gameID = '%s'" % (gameID))
    #newDictator(gameID)
    db.commit
    db.close

#sets next player as dictator
#def newDictator(gameID):
    
    
#addUser("Jim","password")
#addGame("Jim",['a','b','c'],['a','b','c'])
#addPlayer(0, "Bob")
#drawBlack(0,"Jim")
#chooseCardToPlay(0,"Jim","b")
chooseWinner(0,"c")
db = sqlite3.connect(f)
c = db.cursor()
c.execute("SELECT * FROM games")
data = c.fetchall()
print(data)
