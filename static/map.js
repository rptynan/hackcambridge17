var Map;
var Us = {location: {lat:0, lng:0}, marker: undefined}
// I hope that it's resonable to assume he's at the Whitehouse, but I guess
// with the Donald you never know.
var Trump = {location: {lat:38.9, lng:-77.0}, marker: undefined}

function setTrumpLocation(location) {
    Trump.location = location;
    if (Trump.marker === undefined) {
        Trump.marker = new google.maps.Marker({
          position: location,
          map: Map
        });
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
}
