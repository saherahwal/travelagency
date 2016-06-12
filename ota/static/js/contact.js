$(document).ready(function () {

        var initGoogleMap = function initialize() {
            var secheltLoc = new google.maps.LatLng(47.682100100, -122.103158800);

            var myMapOptions = {
                zoom: 15
                , center: secheltLoc
                , mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var theMap = new google.maps.Map(document.getElementById("map_canvas"), myMapOptions);


            var marker = new google.maps.Marker({
                map: theMap,
                draggable: true,
                position: new google.maps.LatLng(47.682100100, -122.103158800),
                visible: true
            });

            var boxText = document.createElement("div");
            boxText.innerHTML = "<strong>Book Your Travel</strong><br>17756 NE 90th St.,<br>Redmond, WA";

            var myOptions = {
                content: boxText
                , disableAutoPan: false
                , maxWidth: 0
                , pixelOffset: new google.maps.Size(-140, 0)
                , zIndex: null
                , closeBoxURL: ""
                , infoBoxClearance: new google.maps.Size(1, 1)
                , isHidden: false
                , pane: "floatPane"
                , enableEventPropagation: false
            };

            google.maps.event.addListener(marker, "click", function (e) {
                ib.open(theMap, this);
            });

            var ib = new InfoBox(myOptions);
            ib.open(theMap, marker);
        }

        //
        // Call initialize
        //
        initGoogleMap();

});