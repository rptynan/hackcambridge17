var Map;
var Us = {location: {lat:0, lng:0}, marker: undefined}
// I hope that it's resonable to assume he's at the Whitehouse, but I guess
// with the Donald you never know.
var Trump = {location: {lat:38.9, lng:-77.0}, marker: undefined}
var IconsBase = $SCRIPT_ROOT + '/static/icons/';


function setTrumpLocation(location) {
    Trump.location = location;
    if (Trump.marker === undefined) {
        Trump.marker = new google.maps.Marker({
            position: location,
            title: 'The Donald',
            icon: IconsBase + 'trump.svg',
            map: Map,
        });
        Trump.infowindow = new google.maps.InfoWindow({
            content: '<div class="infowindow-content">'+
                '<div style="float:left">'+
                '<h1 id="firstHeading" class="firstHeading">The Donald</h1>'+
                '<p><b>The Donald</b>, also referred to as <b>TrumpyWumpy</b>,'+
                '<b>Trumplestiltskin</b>, <b>El Presidente</b>, is a large '+
                'sandstone rock formation and a man you wouldn\'t want to '+
                'meet in a dark alley after a night out (or ever really).'+
                'It has many springs, waterholes, rock caves and ancient '+
                'paintings.'+
                '</div>'+
                '<div style="float:right">'+
                '<img style="width: auto" src="static/img/trump_profile.jpg" />'+
                '</div>'+
                '</div>',
            maxWidth: $(window).width() / 3,
        });
        Trump.marker.addListener(
            'click',
            () => Trump.infowindow.open(Map, Trump.marker)
        );
    }
    else {
        Trump.marker.setPosition(location);
    }
}

function setOurLocation(location) {
    Us.location = location;
    if (Us.marker === undefined) {
        Us.marker = new google.maps.Marker({
            position: location,
            icon: IconsBase + 'exit.svg',
            map: Map
        });
    }
    else {
        Us.marker.setPosition(location);
    }
}

function initMap() {
    // Ask for geo permission
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition((position) => setOurLocation(
            {lat: position.coords.latitude, lng: position.coords.longitude}
        ));
    }

    // Make map
    Map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: Us.location,
        mapTypeControl: false,
        streetViewControl: false,
    });

    // Get the Donald's position
    $.getJSON($SCRIPT_ROOT + '/donaldslocation', data => setTrumpLocation(data))
}
