var mymap = L.map('map').setView([39.82, -98.58], 3);

L.tileLayer('https://api.mapbox.com/styles/v1/makhil2008/ckhh79k950azd1ap7dvsrbne8/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibWFraGlsMjAwOCIsImEiOiJja2hlYW9kdDcwMG9tMnJwMWtvajNjcTY2In0.6hOdLp27pGk_qC1HMojKbg'
    , {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>,' +
        ' Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 20,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    accessToken: 'pk.eyJ1IjoibWFraGlsMjAwOCIsImEiOiJja2hlYW9kdDcwMG9tMnJwMWtvajNjcTY2In0.6hOdLp27pGk_qC1HMojKbg'
}).addTo(mymap);

var mapCircles = []

function drawMapLocations(data) {
    var colors = ["#003f5c","#2f4b7c","#665191","#a05195","#d45087", "#f95d6a", "#ff7c43", "#ffa600"];

    locations = data.locations;
    var sumLat = 0.0;
    var sumLong = 0.0;

    locations.forEach(function(l) {
        var color = colors[Math.floor(Math.random() * colors.length)];
        sumLat += l.lat;
        sumLong += l.long;
        var circle = L.circle([l.lat,l.long,], {
            color: color,
            fillColor: color,
            fillOpacity: 0.5,
            radius: 100000
            }).bindTooltip(l.text, { className: "my-label", offset: [0, 0] }).addTo(mymap);
        mapCircles.push(circle)
    });

    mymap.panTo(new L.LatLng(sumLat/locations.length, sumLong/locations.length));
}
