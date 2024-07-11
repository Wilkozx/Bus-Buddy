import React, { useEffect } from "react";

import * as L from "leaflet";
import { fetchData } from "../services/busDataService";
import { io } from "socket.io-client";

function BusLayer(props: any) {
  useEffect(() => {
    let mapRef = props.mapRef || null;
    const busLayer = L.layerGroup();
    let buses: any[] = [];

    const URL = "http://localhost:5000";
    const socket = io(URL);

    socket.on("connect", () => {
      console.log("Connected to server");
    });

    const getBusData = async () => {
      let endpoint =
        `/api/data?` +
        "latitude=" +
        mapRef.getBounds().getSouthWest().lat +
        "&longitude=" +
        mapRef.getBounds().getSouthWest().lng +
        "&latitude2=" +
        mapRef.getBounds().getNorthEast().lat +
        "&longitude2=" +
        mapRef.getBounds().getNorthEast().lng;

      try {
        const response = await fetchData(endpoint);
        buses = response;
      } catch (error) {
        console.error(error);
      }
    };

    const updateBuses = () => {
      if (!mapRef) {
        return;
      }
      if (mapRef.getZoom() < 12) {
        let renderer = L.canvas({ padding: 0.5 });
        getBusData().then(() => {
          busLayer.clearLayers();
          for (let i = 0; i < buses.length; i++) {
            if (buses[i]["bearing"] === null) {
              continue;
            }
            let latitudedetail = buses[i]["latitude"];
            let longitudedetail = buses[i]["longitude"];

            let bus_canvas_icon = L.circleMarker(
              [latitudedetail, longitudedetail],
              {
                renderer: renderer,
                radius: 2,
                color: "blue",
              }
            ).addTo(busLayer);
          }
          busLayer.addTo(mapRef);
        });
      } else {
        getBusData().then(() => {
          busLayer.clearLayers();
          for (let i = 0; i < buses.length; i++) {
            if (buses[i]["bearing"] === null) {
              continue;
            }
            let latitudedetail = buses[i]["latitude"];
            let longitudedetail = buses[i]["longitude"];
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

            L.marker([latitudedetail, longitudedetail], { icon: bus_div_icon })
              .addTo(busLayer)
              .bindPopup(popup);
          }
          busLayer.addTo(mapRef);
        });
      }
    };

    updateBuses();
    if (mapRef) {
      busLayer.addTo(mapRef);

      socket.on("update_buses", updateBuses);
      mapRef.on("moveend", updateBuses);
    }
    return () => {
      busLayer.clearLayers();
    };
  });

  return (
    <div className="App2">
      <div id="map2"></div>
    </div>
  );
}

export default BusLayer;
