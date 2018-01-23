import sqlite3, random
f = "data/game.db"

with open("utils/blackcards.txt") as fb:
    blacks = fb.readlines()
blacks = [x.strip() for x in blacks]

with open("utils/whitecards.txt") as fb:
    whites = fb.readlines()
whites = [x.strip() for x in whites] 

#validate 
def validate(user, password):
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
def addGame(user, total, goal):
    db = sqlite3.connect(f)
    c = db.cursor()
    id = newGameID()
    c.execute("INSERT INTO games VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (id, user, 0, 1, 0, total, goal, 0))
    for each in whites:
        c.execute("INSERT INTO whiteDecks VALUES('%s', '%s')" % (id, each))
    for each in blacks:
        c.execute("INSERT INTO blackDecks VALUES('%s', '%s')" % (id, each))
    db.commit()
    db.close()
    drawBlack(id, user)
    drawHand(id, user)

#adds user to games
def addPlayer(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    total = c.execute("SELECT * FROM games WHERE gameID = '%s'" % (gameID)).fetchall()[0][5]
    goal = c.execute("SELECT * FROM games WHERE gameID = '%s'" % (gameID)).fetchall()[0][6]
    c.execute("INSERT INTO games VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (gameID, user, 0, 0, 0, total, goal, 0))
    count = c.execute("SELECT count(*) FROM games WHERE gameID = '%s'" % (gameID)).fetchall()[0][0]
    if count == total:
        c.execute("UPDATE games SET status = '%s' WHERE gameID = '%s'" % (1, gameID))
    db.commit()
    db.close()
    drawHand(gameID, user)

#chooses black card randomly and removes from deck; adds to cardsOnBoard
def drawBlack(gameID,user):
    db = sqlite3.connect(f)
    c = db.cursor()
    cards = c.execute("SELECT * FROM blackDecks WHERE gameID = '%s'" % (gameID)).fetchall()
    chosen = (random.choice(cards))
    c.execute("DELETE FROM blackDecks WHERE gameID = '%s' AND card = '%s'" % (chosen[0], chosen[1]))
    c.execute("INSERT INTO cardsOnBoardBlack VALUES ('%s', '%s', '%s')" % (gameID, user, chosen[1]))
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
    c.execute("INSERT INTO cardsOnBoardWhite VALUES('%s','%s','%s')" % (gameID, user, card))
    db.commit()
    db.close()
    
#given a winning card, finds player who played it, updates their score, clears cardsOnBoard for that game, calls newDictator function
def chooseWinner(gameID, card):
    db = sqlite3.connect(f)
    c = db.cursor()
    player = c.execute("SELECT * FROM cardsOnBoardWhite WHERE gameID = '%s' AND card = '%s'" % (gameID, card)).fetchall()[0][1]
    score = c.execute("SELECT * FROM games WHERE gameID = '%s' AND user = '%s'" % (gameID, player)).fetchall()[0][2]
    c.execute("UPDATE games SET score = '%s' WHERE gameID = '%s' AND user = '%s'" % (score+1, gameID, player))
    c.execute("UPDATE games SET roundDone = 1 WHERE gameID = '%s'" % (gameID))
    c.execute("DELETE FROM cardsOnBoardWhite WHERE gameID = '%s'" % (gameID))
    c.execute("DELETE FROM cardsOnBoardBlack WHERE gameID = '%s'" % (gameID))
    #newDictator(gameID)
    if gameEnded(gameID):
        c.execute("UPDATE games SET status = '%s' WHERE gameID = '%s'" % (2, gameID))
    db.commit()
    db.close()

#determines if everyone has played a card
def playedCard(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    players = c.execute("SELECT count(*) FROM games WHERE gameID = '%s'" % (gameID)).fetchall()
    cards = c.execute("SELECT count(*) FROM cardsOnBoardWhite WHERE gameID = '%s'" % (gameID)).fetchall()
    db.commit()
    db.close()
    return players[0][0]-1 == cards[0][0]

#Returns true if user has played a card
def userPlayed(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    count = c.execute("SELECT count(*) FROM cardsOnBoardWhite WHERE gameID = '%s' AND user = '%s'" % (gameID, user)).fetchall()[0][0]
    db.commit()
    db.close()
    return count > 0

#sets next player as dictator
def newDictator(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    dictator = c.execute("SELECT * FROM games WHERE gameID = '%s' AND dictator = '%s'" % (gameID, 1)).fetchall()[0]
    c.execute("DELETE FROM games WHERE gameID = '%s' AND dictator = '%s'" % (gameID, 1))
    c.execute("INSERT INTO games VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (dictator[0], dictator[1], dictator[2], 0, dictator[4], dictator[5], dictator[6], dictator[7]))
    newdict = c.execute("SELECT * FROM games WHERE gameID = '%s'" % (gameID)).fetchall()[0][1]
    c.execute("UPDATE games SET dictator = '%s' WHERE gameID = '%s' AND user = '%s'" % (1, gameID, newdict))
    db.commit()
    db.close()

#returns cards in users hand
def cardsInDeck(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    cards = []
    lines = c.execute("SELECT * FROM userCards WHERE gameID = '%s' AND user = '%s'" % (gameID, user)).fetchall()
    db.commit()
    db.close()
    for each in lines:
        cards.append(each[2])
    return cards

#returns boolean to check if game is over
def gameEnded(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    goal = c.execute("SELECT * FROM games WHERE gameID = '%s'" % (gameID)).fetchall()[0][6]
    count = c.execute("SELECT count(*) FROM games WHERE gameID = '%s' AND score = '%s'" % (gameID, goal)).fetchall()[0][0]
    db.commit()
    db.close()
    return count > 0

#checks to see if enough people joined game
def enoughPeople(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    total = c.execute("SELECT * FROM games WHERE gameID = '%s'" % (gameID)).fetchall()[0][5]
    count = c.execute("SELECT count(*) FROM games WHERE gameID = '%s'" % (gameID)).fetchall()[0][0]
    db.commit()
    db.close()
    return count == total

#returns if winner has been chosen for the round
def winnerChosen(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    bool = c.execute("SELECT * FROM games WHERE gameID = '%s'" % (gameID)).fetchall()[0][4]
    c.execute("UPDATE games SET roundDone = '%s' WHERE gameID = '%s'" % (0, gameID))
    db.commit()
    db.close()
    return bool == 1

#initial draw x number of cards
def drawHand(gameID, user):
    i = 0
    while i < 10:
        drawWhite(gameID,user)
        i  = i + 1

#return all white cards on board
def getWhite(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    cards = []
    lines = c.execute("SELECT * FROM cardsOnBoardWhite WHERE gameID = '%s'" % (gameID)).fetchall()
    db.commit()
    db.close()
    for each in lines:
        cards.append(each[2])
    return cards

#Returns the white card that given user has played in given game
def getPlayerWhite(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    card = c.execute("SELECT * FROM cardsOnBoardWhite WHERE gameID = '%s' AND user = '%s'" % (gameID, user)).fetchall()
    db.commit()
    db.close()
    return card[0][2]

#return all black cards on board
def getBlack(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    card = c.execute("SELECT * FROM cardsOnBoardBlack WHERE gameID = '%s'" % (gameID)).fetchall()
    db.commit()
    db.close()
    return card[0][2]

#Returns all games given user is currently in
def getCurrent(user):
    db = sqlite3.connect(f)
    c = db.cursor()
    lines = c.execute("SELECT * FROM games WHERE user = '%s' AND status = '%s' OR user = '%s' AND status = '%s'" % (user, 1, user, 0)).fetchall()
    result = []
    for each in lines:
        d = {}
        d["gameID"] = each[0]
        players = c.execute("SELECT * FROM games WHERE gameID = '%s'" % (each[0])).fetchall()
        d["player"] = players[0][1]
        count = c.execute("SELECT count(*) FROM games WHERE gameID = '%s'" % (each[0])).fetchall()[0][0]
        d["current"] = count
        d["total"] = each[5]
        playersString = ""
        for line in players:
            playersString += line[1] + ", "
        playersString = playersString[:len(playersString)-2]
        d["players"] = playersString
        d["goal"] = each[6]
        result.append(d)
    db.commit()
    db.close()
    return result

#Returns whether user has current game
def hasCurrent(user):
    db = sqlite3.connect(f)
    c = db.cursor()
    count = c.execute("SELECT count(*) FROM games WHERE user = '%s' AND status = '%s' OR user = '%s' AND status = '%s'" % (user, 1, user, 0)).fetchall()[0][0]
    db.commit()
    db.close()
    return count > 0

#Returns whether user is dictator
def isDictator(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    count = c.execute("SELECT count(*) FROM games WHERE gameID = '%s' AND user = '%s' AND dictator = '%s'" % (gameID, user, 1)).fetchall()[0][0]
    db.commit()
    db.close()
    return count > 0

#Checks if given user is not in given game
def notInGame(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    count = c.execute("SELECT count(*) FROM games WHERE gameID = '%s' AND user = '%s'" % (gameID, user)).fetchall()[0][0]
    db.commit()
    db.close()
    return count == 0
    
#Return all games that given user can join
def getJoin(user):
    db = sqlite3.connect(f)
    c = db.cursor()
    lines = c.execute("SELECT * FROM games WHERE status = '%s'" % (0)).fetchall()
    result = []
    ids = []
    for each in lines:
        if notInGame(each[0], user) and each[0] not in ids:
            d = {}
            d["gameID"] = each[0]
            ids.append(each[0])
            players = c.execute("SELECT * FROM games WHERE gameID = '%s'" % (each[0])).fetchall()
            d["player"] = players[0][1]
            count = c.execute("SELECT count(*) FROM games WHERE gameID = '%s'" % (each[0])).fetchall()[0][0]
            d["current"] = count
            d["total"] = each[5]
            playersString = ""
            for line in players:
                playersString += line[1] + ", "
            playersString = playersString[:len(playersString)-2]
            d["players"] = playersString
            d["goal"] = each[6]
            result.append(d)
    db.commit()
    db.close()
    return result

def hasJoin(user):
    db = sqlite3.connect(f)
    c = db.cursor()
    result = getJoin(user)
    db.commit()
    db.close()
    return len(result) > 0

#Return all games that given user has finished
def getFinished(user):
    db = sqlite3.connect(f)
    c = db.cursor()
    lines = c.execute("SELECT * FROM games WHERE user = '%s' AND status = '%s'" % (user, 2)).fetchall()
    result = []
    for each in lines:
        d = {}
        d["gameID"] = each[0]
        players = c.execute("SELECT * FROM games WHERE gameID = '%s'" % (each[0])).fetchall()
        d["player"] = players[0][1]
        count = c.execute("SELECT count(*) FROM games WHERE gameID = '%s'" % (each[0])).fetchall()[0][0]
        d["current"] = count
        d["total"] = each[5]
        playersString = ""
        for line in players:
            playersString += line[1] + ", "
        playersString = playersString[:len(playersString)-2]
        d["players"] = playersString
        d["goal"] = each[6]
        result.append(d)
    db.commit()
    db.close()
    return result

#Adds given user to seen table
def addSeen(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    numPlayers = c.execute("SELECT count(*) FROM games WHERE gameID = '%s'" % (gameID)).fetchall()[0][0]
    c.execute("INSERT INTO seen VALUES ('%s', '%s', '%s')" % (gameID, numPlayers, user))
    db.commit()
    db.close()

#Checks if given user is in seen table
def checkSeen(gameID, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    count = c.execute("SELECT count(*) FROM seen WHERE gameID = '%s' AND user = '%s'" % (gameID, user)).fetchall()[0][0]
    db.commit()
    db.close()
    return count > 0

#Removes all lines with given gameID from seen table
def clearRound(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("DELETE FROM seen WHERE gameID = '%s'" % (gameID))
    db.commit()
    db.close()

#Adds card to currentRound table (winning is boolean)
def addCard(gameID, card, winning):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("INSERT INTO currentRound VALUES ('%s', '%s', '%s')" % (gameID, card, winning))
    db.commit()
    db.close()

#Returns the winning card in given game
def getWinningCard(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    card = c.execute("SELECT * FROM currentRound WHERE gameID = '%s' AND winning = '%s'" % (gameID, 1)).fetchall()[0][1]
    db.commit()
    db.close()
    return card

#Removes all lines with given gameID from currentRound table
def removeCards(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("DELETE FROM currentRound WHERE gameID = '%s'" % (gameID))
    db.commit()
    db.close()

#Gets all cards in current round
def getAllCards(gameID):
    db = sqlite3.connect(f)
    c = db.cursor()
    allCards = ""
    cards = c.execute("SELECT * FROM currentRound WHERE gameID = '%s'" % (gameID)).fetchall()
    for card in cards:
        allCards += card[1] + ", "
    allCards = allCards[:len(allCards)-2]
    db.commit()
    db.close()
    return allCards

#addUser("Jim","password")
#addUser("Bob","password")
#addUser("Mary","password")
#addUser("Sam", "password")
#addGame("Jim", 3, 2)
#addPlayer(0, "Bob")
#addPlayer(0, "Sam")
#addPlayer(0, "Mary")
#addSeen(0,"Jim")
#drawBlack(0, "Jim")
#drawWhite(0, "Bob")
#drawWhite(0, "Bob")
#drawWhite(0, "Sam")
#drawWhite(0, "Sam")
#drawWhite(0, "Mary")
#drawWhite(0, "Mary")
#chooseCardToPlay(0,"Bob","Golden showers.")
#chooseCardToPlay(0,"Mary","A wheelchair death race.")
#chooseCardToPlay(0,"Sam","Fading away into nothingness.")
#print playedCard(0)
#print cardsInDeck(0,"Bob")
#chooseWinner(0,"Your mum.")
#print winnerChosen(0)
#print enoughPeople(1)
#print getPlayerWhite(0,"Bob")
#newDictator(0)
#print isDictator(0,"Jim")
#print isDictator(0,"Mary")
#print getDictator(0,"Bob")
#print hasCurrent("Jim")
#print hasJoin("Bob")
#print getBlack(0)
#print cardsInDeck(0,"Bob")
#print checkSeen(0, "Bob")
#clearRound(0)
#addCard(1,"LOL",1)
#addCard(0,"another",0)
#addCard(0,"etc",0)
#print getAllCards(1)
#print getWinningCard(1)
#removeCards(1)
'''
db = sqlite3.connect(f)
c = db.cursor()
c.execute("SELECT * FROM currentRound")
data = c.fetchall()
print(data)
print getCurrent("Bob")
print getFinished("Bob")
print getJoin("Bob")
'''

