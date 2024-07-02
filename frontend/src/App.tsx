import React, { useEffect } from "react";
import axios from "axios";
import "./App.css";

import * as L from "leaflet";

function App() {
  useEffect(() => {
    const map = L.map("map").setView(
      [52.651133231174704, -1.2406078784788304],
      12
    );

    const busLayer = L.layerGroup();
    let buses = [];
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    const fetchData = async () => {
      try {
        const API_URL = "http://172.26.30.1:5000" || "http://localhost:5000";
        const response = await axios.get(
          `${API_URL}/api/data?` +
            "latitude=" +
            map.getBounds().getNorthEast().lat +
            "&longitude=" +
            map.getBounds().getNorthEast().lng +
            "&latitude2=" +
            map.getBounds().getSouthWest().lat +
            "&longitude2=" +
            map.getBounds().getSouthWest().lng
        );
        buses = response.data;

        // TODO: add a expiry timer for buses that constantly return undefined for their bearing ( means they offline 90$ of the time) ~ 10 min / chance they are just waiting at bus station
        busLayer.clearLayers();
        for (let i = 0; i < buses.length; i++) {
          if (buses[i]["bearing"] === null) {
            continue;
          }

          let latitude = buses[i]["latitude"];
          let longitude = buses[i]["longitude"];
          let bearing = buses[i]["bearing"];
          let destination = buses[i]["destination_name"];
          let line = buses[i]["published_line_name"];
          let company = buses[i]["operator_ref"];

          let bus_div_icon = L.divIcon({
            className: "bus-icon",
            html:
              "<img src=" +
              "arriva.png" +
              ' width="50" height="50" style="transform: rotate(' +
              (bearing - 90) +
              'deg); ">',
            iconSize: [50, 50],
            iconAnchor: [25, 25],
            popupAnchor: [0, -25],
          });

          var popup = L.popup()
            .setLatLng([52.651133231174704, -1.2406078784788304])
            .setContent(
              "<div><h3>" +
                line +
                "</h3><p>destination: " +
                destination +
                "</p><p>bearing:" +
                bearing +
                "</p></div>"
            );

          L.marker([latitude, longitude], { icon: bus_div_icon })
            .addTo(busLayer)
            .bindPopup(popup);
        }
        busLayer.addTo(map);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
    const interval = setInterval(() => {
      fetchData();
    }, 5000);

    return () => {
      clearInterval(interval);
      map.off();
      map.remove();
    };
  }, []);

  return (
    <div className="App">
      <head>
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossOrigin=""
        />
        <script
          src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
          integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
          crossOrigin=""
        ></script>
      </head>
      <div id="map"></div>
    </div>
  );
}

export default App;
