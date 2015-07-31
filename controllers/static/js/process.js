function getRecommend() {
	var ele = document.getElementById("result");
	if (ele.style.display != "none") {
		var result = document.getElementById("resultTrack");
		result.innerHTML = "";
		ele.style.display = "none";
	}


	var artist1 = document.getElementById("artist-1").value;
	var track1 = document.getElementById("track-1").value;
	var artist2 = document.getElementById("artist-2").value;
	var track2 = document.getElementById("track-2").value;
	var artist3 = document.getElementById("artist-3").value;
	var track3 = document.getElementById("track-3").value;

	var artistList = [];
	var songList = [];
	var query = "http://127.0.0.1:5000/mood/recommend/";

	if (artist1 != "" && track1 != "") {
		artistList.push(artist1);
		songList.push(track1);
	}
	if (artist2 != "" && track2 != "") {
		artistList.push(artist2);
		songList.push(track2);
	}
	if (artist3 != "" && track3 != "") {
		artistList.push(artist3);
		songList.push(track3);
	}

	var artists = "";
	var songs = "";
	for (i = 0; i < artistList.length; i++) {
		artists += artistList[i];
		songs += songList[i];

		if ((i + 1) != artistList.length) {
			artists += "&";
			songs += "&";
		}
	}

	query += artists + "/" + songs;

	var req = new XMLHttpRequest();

	//req.open("GET", query, true);
	//req.send();

	//alert(req.responseText)

	var resultJSON = {"artist":"Jason Mraz", "song":"I'm Yours", "cover_url":"http://akamai-b.cdn.cddbp.net/cds/2.0/cover/AF0A/365F/FDE4/F518_medium_front.jpg"};
	//var ele = document.getElementById("result");
	var result = document.getElementById("resultTrack");
	var coverArt = document.getElementById("resultArt");
	//result.className = "track";
	//result.appendChild(document.createTextNode(resultJSON.song + " - " + resultJSON.artist));
	result.innerHTML = resultJSON.song + " - " + resultJSON.artist;
	ele.style.display = "block";
	/*
	// Create the callback
	req.onreadystatechange = function() {
		if (req.readyState==4 && req.status == 200) {
		// Request successful, read the response
		
		var ele = document.getElementById("recommend");
		ele.innerHTML = "<pre>"+req.responseText+"</pre>";
		ele.style.display = "block";

		//var textresponse = req.responseText;
		//var resultJSON = JSON.parse(textresponse);
		var resultJSON = JSON.parse(req.responseTex);
		alert(Object.keys(resultJSON));
		
		var ele = document.getElementById("playlist");
		var result = document.createElement('li');
		result.className = "track";
		result.appendChild(document.createTextNode(resultJSON.song + " - " + resultJSON.artist));
		ele.appendChild(result);
		}
	}
	*/

	//alert(query)
}

