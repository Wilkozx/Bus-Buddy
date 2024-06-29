import React, { useEffect } from 'react';
import { useState } from 'react';
import { useRef } from 'react';
import axios from 'axios';
import './App.css';

import * as L from 'leaflet';

function App() {

  useEffect(() => {
    const map = L.map('map').setView([52.651133231174704, -1.2406078784788304], 11);
    const busLayer = L.layerGroup();
    let buses = [];
  
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    let bus_icon = L.icon({
      iconUrl: 'bus.png',
      iconSize: [50, 50],
      iconAnchor: [25, 25],
      popupAnchor: [0, -25],
    });

    const fetchData = async () => {
      try {
        busLayer.clearLayers();
        const response = await axios.get(`http://localhost:5000/api/data/127`);
        buses = (response.data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery']['VehicleActivity']);
    
        for (let i = 0; i < buses.length; i++) {
              L.marker([buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude'], buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']], {icon: bus_icon}).addTo(busLayer).bindPopup(`Bus ${buses[i]['MonitoredVehicleJourney']['PublishedLineName']}`);
            }
          busLayer.addTo(map);
      }
      catch (error) {
        console.error(error);
      }
    };

    fetchData();
    const interval = setInterval(() => {
      fetchData();
    }, 15000);

    return () => {
      clearInterval(interval);
      map.off();
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
