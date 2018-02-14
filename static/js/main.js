
//var timestamp = ["1518585580", "1518585582", "1518585584", "1518585585", "1518585586", "1518585587", "1518585589", "1518585590", "1518585591", "1518585592", "1518585594", "1518585622", "1518585628", "1518585629", "1518585645", "1518585705", "1518585740", "1518585761", "1518585762", "1518585765", "1518585766"];

$(document).ready(function() {
    var menu = document.getElementsByClassName('menu')[0];
    if (window.location.pathname == '/') {
        menu.style.display = 'none';
    }else{
        menu.style.display = 'block';
    }
});

function sendDataToServer(first_value, last_value) {
    var script_root = getScriptRoot();
    $.getJSON(script_root + '/', {
        first: first_value,
        last: last_value,
        success: function(){
            showGraphOptions();
        }
    });
    return false;
}

var slider = document.getElementById('slider');
slider.style.width = '60%';
slider.style.margin = 'auto';

noUiSlider.create(slider, {
	start: [20, 80],
	connect: true,
	range: {
		'min': 0,
		'max': 100
	}
});

function convertTimestamp(){
    var timestamp = getTimestamp();
    for(var i = 0 ; i < timestamp.length; i++){
        var integer_time = parseInt(timestamp[i]);
        var date = new Date(integer_time*1000);
        var hours = date.getHours();
        var minutes = "0" + date.getMinutes();
        var seconds = "0" + date.getSeconds();
        // Display time in 10:30:23 format
        var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
        console.log(timestamp[i] + " : " + formattedTime);
    }
}

function onSelectAllData() {
    var timestamp = getTimestamp();
    console.log(timestamp);
    sendDataToServer(0,timestamp.length);
}

function getIndexOfElement(element) {
    var index =  timestamp.indexOf(element);
    return index;
}

function showGraphOptions() {
    var menu = document.getElementsByClassName('menu')[0];
    menu.style.display = 'block';
}

function openSelectMenu() {

}