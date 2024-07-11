import React, { useEffect } from "react";
import "./styles/map.css";

import * as L from "leaflet";
import BusLayer from "./components/BusLayer";

function Map() {
  const [mapRef, setMapRef] = React.useState<L.Map | null>(null);

  useEffect(() => {
    const map = L.map("map", {
      preferCanvas: true,
    }).setView([52.645813588435104, -1.2753865644869717], 12);
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    setMapRef(map);

    return () => {
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

export default Map;
