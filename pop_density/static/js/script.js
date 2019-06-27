mapboxgl.accessToken = '';

    // Set bounds to Africa
    var bounds = [
        [-42.322110, -37.119575], // Southwest coordinates
        [36.536829, 62.075966]  // Northeast coordinates
    ];

	var map = new mapboxgl.Map({
	  container: 'map', // container id
	  style: 'mapbox://styles/loriches/cjcbs8fn8024t2rlqpcin80xg', // replace this with your style URL
      center: [3.687646, 22.829351], 
      zoom: 2,
      maxBounds: bounds
	});

	map.on('load', function () {

        //globals for the choropleth https://bl.ocks.org/hrecht/82b6440ed3b982a6f594
        var COLORS = ["#fff7ec","#fee8c8","#fdbb84","#fc8d59","#d7301f","#7f0000"],
        BREAKS = [0, 5, 10, 50, 100, 500],
        FILTERUSE;

        // legend
        for (i = 0; i < BREAKS.length; i++) {
          var layer = BREAKS[i];
          var color = COLORS[i];
          var item = document.createElement('div');
          var key = document.createElement('span');
          key.className = 'legend-key';
          key.style.backgroundColor = color;

          var value = document.createElement('span');
          value.innerHTML = layer;
          item.appendChild(key);
          item.appendChild(value);
          legend.appendChild(item);
        }

        // data
   		map.addSource("data", {
        "type": "geojson",
        "data": 'http://localhost:5000/data'
    	});
    	map.addLayer({
        "id": "boundary",
        "type": "fill",
        "source": "data",
        "paint": {
        	"fill-color": {
        		property: 'mean',
        		stops: [
                    [BREAKS[0], COLORS[0]],
                    [BREAKS[1], COLORS[1]],
                    [BREAKS[2], COLORS[2]],
                    [BREAKS[3], COLORS[3]],
                    [BREAKS[4], COLORS[4]],
                    [BREAKS[5], COLORS[5]]
                    ]
             },
            "fill-outline-color": "#888888",
            "fill-opacity": 0.4
            },
        "filter": ["==", "$type", "Polygon"]
        });

        // tooltip
        map.on('mousemove', function(e) {
          var states = map.queryRenderedFeatures(e.point, {
            layers: ['boundary']
          });

          if (states.length > 0) {
            document.getElementById('pd').innerHTML = '<h3><strong>Number of People living in ' + states[0].properties.admin2Name + '</strong></h3><p><strong><em>' + Math.round(states[0].properties.sum) + '</strong> people </em></p>';
          } else {
            document.getElementById('pd').innerHTML = '<p>Hover over a state!</p>';
          }
        });

});
