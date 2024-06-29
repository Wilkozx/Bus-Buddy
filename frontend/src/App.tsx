import React, { useEffect } from 'react';
import './App.css';

import * as L from 'leaflet';

function App() {

  var customicon = L.icon({
    iconUrl: 'bus.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [0, -25],
  });

  useEffect(() => {
    const map = L.map('map').setView([51.505, -0.09], 13);
  
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);
  
    L.marker([51.505, -0.09], {icon: customicon}).addTo(map)
    return () => {
      map.remove();
    };
  }, []);
  
  return (
    <div className="App">
      <head>
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossOrigin=''/>
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossOrigin=''></script>
      </head>
      <div id='map'></div>
    </div>
  );
}

export default App;
