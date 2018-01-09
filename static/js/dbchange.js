var drawCard = function( e ) {
    
    $.ajax({
	url: '/drawCard',
	type: 'GET',
	data: {
	    "type": type //dictator or not?
	    "gameID": gameID
	    "user": user
	      },
	success: function(d) {
	    //display cards in hand here
	} //end success callback
    });//end ajax call
}; //end transmit function

var endTurn = function( e ) {
    
    $.ajax({
	url: '/endTurn',
	type: 'GET',
	data: {},
	success: function(d) {
	    if (d){
		drawCard;
	    }
	} //end success callback
    });//end ajax call
}; //end transmit function


var interval = 1000 * 1; //1 second

//button.addEventListener('click', transmit);

setInterval(transmit, interval);

