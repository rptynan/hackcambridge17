var Map;
var Us = {location: {lat:0, lng:0}, marker: undefined};
// I hope that it's resonable to assume he's at the Whitehouse, but I guess
// with the Donald you never know.
var Trump = {location: {lat:38.9, lng:-77.0}, marker: undefined};
var IconsBase = $SCRIPT_ROOT + '/static/icons/';
var Flights = [];

var INFO_WINDOW_WIDTH = $(window).width() / 3;


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
                '<h1 class="info-header">The Donald</h1>'+
                '<div class="info-wrapper">'+
                '<div class="info-right">'+
                '<img style="height: 8em; width: auto" '+
                'src="static/img/trump_profile.jpg" />'+
                '</div>'+
                '<div class="info-left">'+
                '<p><b>The Donald</b>, also referred to as <b>TrumpyWumpy</b>,'+
                '<b>Trumplestiltskin</b>, <b>El Presidente</b>, is a large '+
                'sandstone rock formation and a man you wouldn\'t want to '+
                'meet in a dark alley after a night out (or ever really).'+
                'It has many springs, waterholes, rock caves and ancient '+
                'paintings.'+
                '</div>'+
                '</div>'+
                '</div>',
            maxWidth: INFO_WINDOW_WIDTH,
        });
        Trump.marker.addListener(
            'click',
            () => Trump.infowindow.open(Map, Trump.marker)
        );
    }
    else {
        Trump.marker.setPosition(location);
    }
    // Update flights now that we've moved
    fetchUpdatedFlights();
}


function setOurLocation(location) {
    Us.location = location;
    if (Us.marker === undefined) {
        Us.marker = new google.maps.Marker({
            position: location,
            icon: IconsBase + 'exit.svg',
            map: Map,
        });
        Us.infowindow = new google.maps.InfoWindow({
            content: '<div class="infowindow-content">'+
                '<h1 class="info-header">You</h1>'+
                '<div class="info-wrapper">'+
                '<p><b>You</b>, an upper-middle-class liberal, afraid for '+
                'your life. First Brexit, now this? And the righter-wingers '+
                'had a summit in Germany? That\'s it, I\'m off to Australia, '+
                'at least they have a liberal government.'+
                '</div>'+
                '</div>',
            maxWidth: INFO_WINDOW_WIDTH,
        });
        Us.marker.addListener(
            'click',
            () => Us.infowindow.open(Map, Us.marker)
        );
    }
    else {
        Us.marker.setPosition(location);
    }
    // Update flights now that we've moved
    fetchUpdatedFlights();
}

function fetchUpdatedFlights() {
    $.getJSON(
        $SCRIPT_ROOT + '/flightlocations',
        {'json': JSON.stringify(
            {'our_location': Us.location, 'trump_location': Trump.location}
        )},
        data => updateFlights(data)
    );
}

function updateFlights(flights) {
    // Delete old markers
    for (let i = 0; i < Flights.length; i++) {
        Flights[i].setMap(null);
    }
    Flights = [];
    // Add new ones
    for (let i = 0; i < flights.length; i++) {
        let loc = new google.maps.LatLng(flights[i]['lat'], flights[i]['lng']);
        Flights.push(new google.maps.Marker({
            position: loc,
            icon: IconsBase + 'flight.svg',
            title: flights[i]['Name'],
            map: Map,
        }));
        Flights[i].infowindow = new google.maps.InfoWindow({
            content: '<div class="infowindow-content">'+
                '<h1 class="info-header">You</h1>'+
                '<div class="info-wrapper">'+
                '<p><b>You</b>, an upper-middle-class liberal, afraid for '+
                'your life. First Brexit, now this? And the righter-wingers '+
                'had a summit in Germany? That\'s it, I\'m off to Australia, '+
                'at least they have a liberal government.'+
                '</div>'+
                '</div>',
            maxWidth: INFO_WINDOW_WIDTH,
        });
        Flights[i].addListener(
            'click',
            () => Flights[i].infowindow.open(Map, Flights[i])
        );
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
    Map.addListener(
        'click',
        event => setOurLocation(event.latLng)
    );

    // Get the Donald's position
    $.getJSON($SCRIPT_ROOT + '/donaldslocation', data => setTrumpLocation(data))

    // Get the flights will be set when Donald's or User's location comes back
}
