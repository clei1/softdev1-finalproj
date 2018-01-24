function getGames(user, gameType){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("games").innerHTML = this.responseText;
	}
    };
    xhttp.open('POST', "/gamelist", true);
    var formData = new FormData();
    formData.append('user',user);
    formData.append('gameType', gameType);
    xhttp.send(formData);
}

function createDisplay(user){
    document.getElementById("games").innerHTML="<div id='create'><div class='game'><form action='/create' method='POST'><p><div class='title'>" + user + "'s Game (1/<input type='number' name='playerlim' step='1' min='3' max='10'>)</div><b>Players: </b>" + user + "<br><b>Goal: </b><input type='number' name='scorelim' step='1' min='3'></p><button type='submit'>CREATE GAME</button></form></div>"  
}
