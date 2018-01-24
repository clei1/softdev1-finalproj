function playCard(gameID, card){
    //user's cards gets updated
    var usersCard = new XMLHttpRequest();
    usersCard.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("whitecards").innerHTML = this.responseText;
	}
    };
    usersCard.open('POST', "/playcard", true);
    var formData = new FormData();
    formData.append('gameID', gameID);
    formData.append('card', card);
    usersCard.send(formData);

    //board gets updated
    var boardCards = new XMLHttpRequest();
    boardCards.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("playedcards").innerHTML = this.responseText;
	}
    };
    boardCards.open('POST', "/board", true);
    boardCards.send(formData);

    //status gets updated
    var status = new XMLHttpRequest();
    status.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("status").innerHTML = this.responseText;
	}
    };
    status.open('POST', "/status", true);
    status.send(formData); 
}

function restofupdate(formData){
    var boardCards = new XMLHttpRequest();
    boardCards.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("playedcards").innerHTML = this.responseText;
	}
    };
    boardCards.open('POST', "/board", true);
    boardCards.send(formData);
    
    var usercard = new XMLHttpRequest();
    usercard.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("whitecards").innerHTML = this.responseText;
	}
    };
    usercard.open('POST', '/cardupdate', true);
    usercard.send(formData);
    
    var status = new XMLHttpRequest();
    status.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("status").innerHTML = this.responseText;
	}
    };
    status.open('POST', "/status", true);
    status.send(formData);

    //blackcard gets updated
    var black = new XMLHttpRequest();
    black.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("blackcard").innerHTML = this.responseText;
	}
    };
    black.open('POST', "/blackcard", true);
    black.send(formData);
}

function displayWinningRound(formData){
    //board gets updated
    var boardCards = new XMLHttpRequest();
    boardCards.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("playedcards").innerHTML = this.responseText;
	}
    };
    boardCards.open('POST', "/winninground", true);
    boardCards.send(formData);
}

function endGame(formData){
    var stats = new XMLHttpRequest();
    stats.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("content").innerHTML = this.responseText;
	}
    };
    stats.open('POST', '/endGame', true);
    stats.send(formData);
}

function update(gameID){
    var ds = new XMLHttpRequest();
    ds.onreadystatechange = function(){
	if (this.readyState == 4 && this.status == 200){
	    if (this.responseText == "normal"){
		restofupdate(formData);
	    }
	    else if (this.responseText == "winningboard"){
		console.log("this actually worked?");
		displayWinningRound(formData);
	    }
	    else if (this.responseText == "endGame"){
		endGame(formData);
	    }
	}
    };
    ds.open('POST', "/displayStatus", true);
    var formData = new FormData();
    formData.append('gameID', gameID);
    ds.send(formData);
}

function roundCard(gameID, card){
    var endRound = new XMLHttpRequest();
    endRound.onreadystatechange=function(){
	if (this.readyState == 4 && this.status == 200){
	    document.getElementById("playedcards").innerHTML = this.responseText;
	}
    };
    endRound.open('POST', "/round", true);
    var formData = new FormData();
    formData.append('gameID', gameID);
    formData.append('card', card);
    endRound.send(formData);
}
