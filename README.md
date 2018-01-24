# bakedHotCheetos pd8
### Bermet Kalmakova, Connie Lei, Henry Zheng
Cards For Humanity

## Demonstration Video
[Youtube [OLD LOGIN SCREEN]](https://youtu.be/VCHi5z_EZEE)

[Login Screenshot](https://imgur.com/sxfwsZc)

## Description
Multiplayer Cards Against Humanity

Each round, one player asks a question from a black card, and everyone else answers with their favorite white card. It's up to the Card Czar to decide whose White Card was the best. You repeat this process until one player collects the goal number of points and wins the game!

## Dependencies
* `from flask import Flask, render_template, request, session, redirect, url_for, flash`
  * requires `pip install flask`
* [`python2.7`](https://www.python.org/download/releases/2.7/)
* `import os, sqlite3`

## Launch Instructions
0. Enter your terminal and go into the directory that you want to have this program in
2. Enter this command to clone our repo
```
git clone https://github.com/clei1/softdev1-finalproj.git
```
3. Run your virtualenv from wherever you have it (if needed)
```
. <PATH_TO_VIRTUALENV>/bin/activate
```
4. Go into the softdev1-finalproj folder using this command
```
cd softdev1-finalproj/
```
5. Run the program
```
python app.py
```
6. Go to localhost:5000 in your web browser and enjoy the site!


## How to Have Fun
Note: You might have to log out and log into other accounts repeatedly to test.
* Login and create a game!
* Have other users on the same computer join your game under the Join tab!
* The game should start as soon as the required number of players have joined.
* Play the game!
  * If you are the Card Czar, wait for other players to choose their white cards to play.
  * If you are not the Card Czar, play a card that best completes the black card (click on a card).
* Once all non-CardCzar players have chosen their respective white cards to play, Card Czar can now choose a winner (click on a card).
* Round has ended. Click on the screen to begin the next round. The Card Czar should be the next player.
* Repeat until goal has been reached. Winner has won!
* Play again if you'd like :)
* Have fun!

## Notes
* Safari Private Browsing works best! (Use Safari if you want to test more than two accounts at the same time)
* Does not work in Firefox -- Tested on Chromium and Safari.
* Chrome incognito windows saves sessions until you close all of the incognito windows.
