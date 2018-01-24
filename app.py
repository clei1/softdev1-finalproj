from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils.db_func import *
from utils.auth_func import *
import os, sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/', methods=['GET', 'POST'])
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if loggedin():
        return redirect(url_for('main'))
    if request.method == 'POST':
        user = request.form['username']
        if log(user, encrypt(request.form['password'])):
            return redirect(url_for('main'))
        else:
            flash('Try again.')
    return render_template('login.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    if loggedin():
        session.pop('user')
        flash('Successfully logged out.')
    else:
        flash('You are not logged in.')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if loggedin():
        flash('You already have an account.')
        return redirect(url_for('main'))
    if request.method == 'POST':
        user = request.form['username']
        if hasUsername(user):
            flash('Username is already in use.')
        elif request.form['password'] != request.form['repeat']:
            flash('Passwords do not match.')
        else:
            password = encrypt(request.form['password'])
            addUser(user, password)
            flash('Successfully registered as ' + user + '.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if loggedin():
        user = session['user']
        if hasCurrent(user):
            #displays current games if user is currently part of any games
            return render_template('main.html', user=user, current = getCurrent(user))
        elif hasJoin(user):
            #user has no current games
            #displays avaliable games
            return render_template('main.html', user=user, join = getJoin(user))
        else:
            #user has no current games, no avaliable games
            #displays create game form
            return render_template('main.html', user=user, create = True)
    return redirect(url_for('login'))

@app.route('/create', methods=['POST'])
def create():
    if loggedin():
        addGame(session['user'], int(request.form['playerlim']), int(request.form['scorelim']))
        return redirect(url_for('main'))
    return redirect(url_for('login'))

def status(user, gameID):
    if not enoughPeople(gameID):
        return "Waiting for players..."
    if isDictator(gameID, user):
        if playedCard(gameID):
            return "Select a winning card."
        else:
            return "You are the Card Czar."
    else:
        if not userPlayed(gameID, user):
            return "Select a card to play."
        else:
            return "Waiting for players..."

@app.route('/play', methods=['POST'])
def play():
    if loggedin():
        user = session['user']
        gameID = int(request.form["gameID"])
        if "join" in request.form and notInGame(gameID, user):
            addPlayer(gameID, user)
        if gameEnded(gameID):
            #print "ending game"
            endGame(gameID)
            #print "endedGame: " + str(gameID)
            flash("That game is over. Please select the view button to look at stats.")
            #return redirect(url_for('main'))
        st = status(user, gameID)
        dt = isDictator(gameID, user)
        yc = None
        if (not dt) and userPlayed(gameID, user):
            yc = getPlayerWhite(gameID, user)
        return render_template('play.html', status=st, dictator=dt, blackCard=getBlack(gameID), cards=getWhite(gameID), whitecards=cardsInDeck(gameID, user), yourcard=yc, user=user, gameID=gameID, allplayed = playedCard(gameID), enoughPlayers=enoughPeople(gameID))
    return redirect(url_for('login'))

@app.route('/view', methods=['POST'])
def view():
    if loggedin():
        gameID = request.form['gameID']
        stats = getStats(gameID)
        return render_template('view.html', stats = stats)

#HELPER FUNCTIONS FOR AJAX CALLS
#==========================================
#helper function for gamelist
def gameHTML(gameType, word, games):
    join = ""
    page = "play"
    if gameType == "join":
        join = '<input type="hidden" value="join" name="join"/>'
    if gameType == "view":
        page = "view"
    i = "<div id='" + gameType + "'>" 
    for g in games:
        s="<div class='game'><p><div class='title'>%s's Game (%d/%d)</div><b>Players: </b>%s<br><b>Goal: </b>%d</p><form action='/%s' method='POST'>%s<button class='g' type='submit' name='gameID' value=%d>%s</button></form></div>" % (g['player'], g['current'], g['total'], g['players'], g['goal'], page, join, g['gameID'], word)
        i += s;
    if len(games) == 0:
        i += "<p></p>"
    i += "</div>"
    return i

def usersBoard(gameID, user):
    allplayed = playedCard(gameID)
    dt = isDictator(gameID, user)
    yc = None
    if userPlayed(gameID, user):
        yc = getPlayerWhite(gameID, user)
    cards = getWhite(gameID)
    i = ""
    for c in cards:
        i += '<div class="card"'
        if allplayed and dt:
            i += 'onclick="roundCard(' + "'" + str(gameID) + "','" + c + "')"
        i += '">'
        if allplayed or yc == c:
            i += c
        i += "</div>"
    return i

def usersCard(gameID, user):
    dt = isDictator(gameID, user)
    played = userPlayed(gameID, user)
    whitecards = cardsInDeck(gameID, user)
    i = ""
    for w in whitecards:
        i +="<div class='white'"
        if not played and not dt and enoughPeople(gameID):
            i += "onclick=" + '"playCard(' + "'" + str(gameID) + "','" + w + "')" + '"'
        i += ">" + w
        i += "</div>"
    return i   

def winningCard(gameID, card):
    #print "WINNING CARD FUNCTION"
    cards = getWhite(gameID)
    i = ""
    for c in cards:
        i += '<div class="card"'
        if c == card:
          i += 'id="winningcard"'
          addCard(gameID, card, 1)
        else:
            addCard(gameID, c, 0)
        i += '">'
        i += c
        i += "</div>"
    return i

def endGameDisplay(gameID):
    stat = getStats(gameID)
    i = "<div id='ending'><table><tr><th>User</th><th>Score</th> </tr>"
    for s in stat:
        i += "<tr><td>"+ s['user'] +"</td><td>"+ str(s['score']) + "</td></tr>"
    i += "</table></div>"
    return i

#AJAX CALLS
#==========================================
@app.route('/gamelist', methods=['POST'])
def gamelist():
    user = request.form['user']
    gameType = request.form['gameType']
    games = None; word = None;
    if gameType == 'current':
        word = 'PLAY'
        games = getCurrent(user)
    elif gameType == 'join':
        word = 'JOIN'
        games = getJoin(user)
    elif gameType == 'view':
        word = 'VIEW STATS'
        games = getFinished(user)
    return gameHTML(gameType, word, games)

@app.route('/playcard', methods=['POST'])
def playCard():
    user = session['user']
    gameID = int(request.form['gameID'])
    card = request.form['card']
    chooseCardToPlay(gameID, user, card)
    drawWhite(gameID, user)
    return usersCard(gameID, user)

@app.route('/board', methods=['POST'])
def board():
    user = session['user']
    gameID = int(request.form['gameID'])
    return usersBoard(gameID, user)

@app.route('/status', methods=['POST'])
def statusUpdate():
    user = session['user']
    gameID = int(request.form['gameID'])
    return status(user, gameID)

@app.route('/round', methods=['POST'])
def roundEnd():
    gameID = int(request.form['gameID'])
    card = request.form['card']
    display = winningCard(gameID, card)
    #resets everything
    chooseWinner(gameID, card)
    dt = newDictator(gameID)
    drawBlack(gameID, dt)
    if gameEnded(gameID):
        endGame(gameID)
    return display

@app.route('/cardupdate', methods=['POST'])
def userUpdate():
    gameID = int(request.form['gameID'])
    user = session['user']
    html = usersCard(gameID, user)
    return html

@app.route('/blackcard', methods=['POST'])
def blackUpdate():
    gameID = int(request.form['gameID'])
    return getBlack(gameID)

@app.route('/displayStatus', methods=['POST'])
def displayStatus():
    gameID = int(request.form['gameID'])
    if not enoughPeople(gameID):
        #print "not enough people"
        return "not enough people"
    if gameEnded(gameID):
        #print "endGame"
        return "endGame"
    user = session['user']
    if checkGame(gameID):
        if checkSeen(gameID, user):
            if allSeen(gameID):
                clearRound(gameID)
                removeCards(gameID)
            return "normal"
        else:
            #print "winning board"
            return "winningboard"
    else:
        print "normal"
        return "normal"

@app.route('/winninground', methods=['POST'])
def winninground():
    user = session['user']
    gameID = int(request.form['gameID'])
    i = ""
    if checkGame(gameID):
        addSeen(gameID, user)
        card = getWinningCard(gameID)
        cards = getAllCards(gameID)
        for c in cards:
            #print c
            i += '<div class="card"'
            if c == card:
                i += 'id="winningcard"'
            i += '">'
            i += c
            i += "</div>"
        #print "allSeen: " + str(allSeen(gameID))
        if allSeen(gameID):
            clearRound(gameID)
            removeCards(gameID)
    return i

@app.route('/endGame', methods=['POST'])
def end():
    gameID = int(request.form['gameID'])
    return endGameDisplay(gameID);
    
#==========================================
if __name__ == '__main__':
    app.run(debug = True)
