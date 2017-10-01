/**
 * Created by chico_percedes on 2017-06-24.
 */
var tag;
$(function() {

    //hide all result divs
    hide(document.getElementById('anger_div'));
    hide(document.getElementById('contempt_div'));
    hide(document.getElementById('disgust_div'));
    hide(document.getElementById('fear_div'));
    hide(document.getElementById('happiness_div'));
    hide(document.getElementById('neutral_div'));
    hide(document.getElementById('sadness_div'));
    hide(document.getElementById('surprise_div'));

});

/**
 *
 */
function useHashtag(){
	hashtag = document.getElementById('hashtag').value;
	tag = hashtag;
	console.log(hashtag);
	var div = document.getElementById('showHash');
	var hide = document.getElementById('results');
	
	document.getElementById('results').style.display = "block";
	
    div.innerHTML = "";
	
	if(hashtag.charAt(0) != "#") {
		div.innerHTML = "#" + div.innerHTML + hashtag;
	} else {
		div.innerHTML = div.innerHTML + hashtag;
	}
	send();

}

function send() {
	console.log("inside send");
	    //hide all result divs
	    hide(document.getElementById('anger_div'));
	    hide(document.getElementById('contempt_div'));
	    hide(document.getElementById('disgust_div'));
	    hide(document.getElementById('fear_div'));
	    hide(document.getElementById('happiness_div'));
	    hide(document.getElementById('neutral_div'));
	    hide(document.getElementById('sadness_div'));
	    hide(document.getElementById('surprise_div'));

	    var params = {
	        // Request parameters
	    };

	    var instagram_clientid = "cdb6ebd6ab4841d3a518e9ecaef9213d";
	    var instagram_secretkey = "43ef1a2a7c484f17aeede55a343ba6fc";
	    var uri_redirect = "https://github.com/yxblee/AI-Global";
	    var insta_code = "https://github.com/yxblee/AI-Global?code=d8689bef17da47cea344ebc92e598f6b";
	    var insta_access_token = "5645620360.cdb6ebd.6d138fa6fac04089867a9ceae954de7d";

	    var insta_user_auth_url = "https://api.instagram.com/oauth/authorize/?client_id=cdb6ebd6ab4841d3a518e9ecaef9213d&redirect_uri=https://github.com/yxblee/AI-Global&response_type=code&scope=public_content";

	    var get_insta_token_curl = "    curl -F 'client_id=cdb6ebd6ab4841d3a518e9ecaef9213d' \
	    -F 'client_secret=43ef1a2a7c484f17aeede55a343ba6fc' \
	    -F 'grant_type=authorization_code' \
	    -F 'redirect_uri=https://github.com/yxblee/AI-Global' \
	    -F 'code=d8689bef17da47cea344ebc92e598f6b' \
	    https://api.instagram.com/oauth/access_token";

	    var jsonresults;

	    var instaresults;

	    //The following are instagram keys needed to trigger the API functions.
	    var token = '5645620360.cdb6ebd.6d138fa6fac04089867a9ceae954de7d',
	        hashtag= tag, // hashtag without # symbol
	        num_photos = 4;

	    //The following ajax queries the instagram api and return a jsonp with the picture details.
	    $.ajax({
	               url: 'https://api.instagram.com/v1/tags/' + hashtag + '/media/recent',
	               dataType: 'jsonp',
	               type: 'GET',
	               data: {access_token: token},
	               success: function(data){
	                   console.log(data);
	                   //The URL image data must be retrieved from the API call and saved as a text file to use
	                   //with cognitive services. Without this, it will not do the job.
	                   //instaresults = '{"url" : "' + data.data[0].images.standard_resolution.url + '" }';
	                   // console.log(instaresults);
	                   instaresultscall(data);

	                   // for(x in data.data){
	                   //     $('ul').append('<li><img src="'+data.data[x].images.standard_resolution.url+'"></li>');
	                   // }
	               },
	               error: function(data){
	                   console.log(data);
	               }
	           });

	    var urls = [];

	    function iterate_insta_data(data){
	        for (var i = 0; i < data.data.length(); i++){
	            instaresults = '{"url" : "' + data.data[i].images.standard_resolution.url + '" }';
	            urls[instaresults] = instaresults;
	        }
	    }

	    
	    /**
	     * instaresultscall is used to call a second ajax query that uses the json from instagram and analyzes
	     * the images(s) urls using the cognitive services API.
	     */
	    function instaresultscall(data){
	        //The following ajax queries the emotion API and detects faces on the picture passed.
          var faces = [];
          var count = 0;
          for (var i = 0; i < data.data.length ; i++){
            var link = '{"url" : "' + data.data[i].images.standard_resolution.url + '" }';
	         $.ajax({
                      async: false,
	                   url: "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize?" + $.param(params),
	                   beforeSend: function(xhrObj){
	                       // Request headers
	                       xhrObj.setRequestHeader("Content-Type","application/json");
	                       xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key","3fab902b4add4555bfd10686842091ee");
	                   },
	                   type: "POST",
	                   // Request body
	                   // data: '{ "url" : "http://static2.businessinsider.com/image/5087f99369bedd394700000d/obama-press-conference-obamacare-sad.jpg" }',
	                   data: link,
	               })
	            .done(function(data) {
	                console.log(data);
                  for(var j = 0; j < data.length ; j++){
                    faces[count++] = data[j];
                  }
	                
	            })
	            .fail(function(data) {
	                console.log(data);
	            });
        }
        console.log(faces);
        paramupdate(faces);
        appendhtml();
	    }

	    /**
	     *
	     * @param value
	     */
	    function paramupdate(value){
	        //here we need to iterate through all the faces totals and save the results
	        //in json results. So total average emotions are displayed.
	        var total;

	        var anger = 0;
	        var contempt = 0;
	        var disgust = 0;
	        var fear = 0;
	        var happiness = 0;
	        var neutral = 0;
	        var sadness = 0;
	        var surprise = 0;

	        for (var i = 0; i < value.length; i++){
	            anger += parseFloat(value[i].scores.anger);
	            // console.log(anger);
	            contempt += parseFloat(value[i].scores.contempt);
	            disgust += parseFloat(value[i].scores.disgust);
	            fear += parseFloat(value[i].scores.fear);
	            happiness += parseFloat(value[i].scores.happiness);
	            neutral += parseFloat(value[i].scores.neutral);
	            sadness += parseFloat(value[i].scores.sadness);
	            surprise += parseFloat(value[i].scores.surprise);
	        }

	        anger = 100 * anger / value.length;
	        contempt = 100 * contempt / value.length;
	        disgust = 100 * disgust / value.length;
	        fear = 100 * fear / value.length;
	        happiness = 100 * happiness / value.length;
	        neutral = 100 * neutral / value.length;
	        sadness = 100 * sadness / value.length;
	        surprise = 100 * surprise / value.length;


	        // jsonresults = value;
	        jsonresults = {
	            "anger" : anger,
	            "contempt" : contempt,
	            "disgust" : disgust,
	            "fear" : fear,
	            "happiness" : happiness,
	            "neutral" : neutral,
	            "sadness" : sadness,
	            "surprise" : surprise
	        }

	    }

	    /**
	     *
	     */
	    function appendhtml(){

	        // var anger = jsonresults[0].scores.anger;
	        // var contempt = jsonresults[0].scores.contempt;
	        // var disgust = jsonresults[0].scores.disgust;
	        // var fear = jsonresults[0].scores.fear;
	        // var happiness = jsonresults[0].scores.happiness;
	        // var neutral = jsonresults[0].scores.neutral;
	        // var sadness = jsonresults[0].scores.sadness;
	        // var surprise = jsonresults[0].scores.surprise;
	        var anger = jsonresults.anger;
	        var contempt = jsonresults.contempt;
	        var disgust = jsonresults.disgust;
	        var fear = jsonresults.fear;
	        var happiness = jsonresults.happiness;
	        var neutral = jsonresults.neutral;
	        var sadness = jsonresults.sadness;
	        var surprise = jsonresults.surprise;

	        $('#anger').html("<p>" + anger.toFixed(5) + "</p>");
	        $('#contempt').html("<p>" + contempt.toFixed(5) + "</p>");
	        $('#disgust').html("<p>" + disgust.toFixed(5) + "</p>");
	        $('#fear').html("<p>" + fear.toFixed(5) + "</p>");
	        $('#happiness').html("<p>" + happiness.toFixed(5) + "</p>");
	        $('#neutral').html("<p>" + neutral.toFixed(5) + "</p>");
	        $('#sadness').html("<p>" + sadness.toFixed(5) + "</p>");
	        $('#surprise').html("<p>" + surprise.toFixed(5) + "</p>");

	        var highestNum = Math.max(anger, contempt, disgust, fear, happiness, neutral, sadness, surprise);
	        var highest = "";

	        switch(highestNum){
	            case anger:
	                highest = " Anger"
	                show(document.getElementById('anger_div'));
	                break;
	            case contempt:
	                highest = " Contempt"
	                show(document.getElementById('contempt_div'));
	                break;
	            case disgust:
	                highest = " Disgust"
	                show(document.getElementById('disgust_div'));
	                break;
	            case fear:
	                highest = " Fear"
	                show(document.getElementById('fear_div'));
	                break;
	            case happiness:
	                highest = " Happiness"
	                show(document.getElementById('happiness_div'));
	                break;
	            case neutral:
	                highest = " Neutral"
	                show(document.getElementById('neutral_div'));
	                break;
	            case sadness:
	                highest = " Sadness"
	                show(document.getElementById('sadness_div'));
	                break;
	            case surprise:
	                highest = " Surprise"
	                show(document.getElementById('surprise_div'));
	                break;
	            default:
	                highest = " None! There may have been no faces in photos with this hashtag."
	        }

	        $('#highest').html("<p>Dominant Emotion:" + highest + "</p>");

	    };
}


function stopRKey(evt) {
  var evt = (evt) ? evt : ((event) ? event : null);
  var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
  if ((evt.keyCode == 13) && (node.type=="text"))  {return false;}
  if ((evt.keyCode == 32) && (node.type=="text"))  {return false;}
}

document.onkeypress = stopRKey;

function hide (elements) {
  elements = elements.length ? elements : [elements];
  for (var index = 0; index < elements.length; index++) {
    elements[index].style.display = 'none';
  }
}

function show (elements){
  elements = elements.length ? elements : [elements];
  for (var index = 0; index < elements.length; index++) {
    elements[index].style.display = 'block';
  }
}