# Create a bus table containing an id,
from flask import jsonify
import requests
import xmltodict
import os
from dotenv import load_dotenv
from db.database_connection import DatabaseConnection
import logging as logger

from flask_socketio import SocketIO


def setup_database(db):
    # function for later use with getting datasets to populate the database everyday at 06:00 or on startup.
    return
def populate_database_data(db):


def populate_database(db, server):
def populate_buses(db, server):
    logger.getLogger(__name__)
    load_dotenv()
    api_key = os.getenv("API_KEY")
    try:
        logger.info("Retrieving data...")
        url = "https://data.bus-data.dft.gov.uk/api/v1/datafeed/?boundingBox=-13.865213794609623,59.065758757501534,2.741947697247088,50.18291484670497&api_key=" + api_key
        try:
            xml_response = requests.get(url)
        except Exception as e:
            logger.error("Unable to retrieve data")
            return
        json_response = xmltodict.parse(xml_response.text)

        # logger.info("Data retrieved, Parsing data...")
        bus_data = []
        for bus in json_response["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]["VehicleActivity"]:
            vehicleuniqueid = bus["MonitoredVehicleJourney"]["VehicleRef"]
            destinationname = bus["MonitoredVehicleJourney"]["DestinationName"] if "DestinationName" in bus["MonitoredVehicleJourney"] else None
            publishedlinename = bus["MonitoredVehicleJourney"][
                "PublishedLineName"] if "PublishedLineName" in bus["MonitoredVehicleJourney"] else None
            bearing = bus["MonitoredVehicleJourney"]["Bearing"] if "Bearing" in bus["MonitoredVehicleJourney"] else None
            latitude = bus["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
            longitude = bus["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
            recordedattime = bus["RecordedAtTime"]
            validuntiltime = bus["ValidUntilTime"]

            bus_data.append((vehicleuniqueid, destinationname, publishedlinename, bearing,
                            latitude, longitude, recordedattime, validuntiltime))
        # logger.info("Data parsed, Inserting data...")
        try:
            db.execute_query("TRUNCATE TABLE buses RESTART IDENTITY CASCADE")
        except Exception as e:
            logger.warning("unable to truncate table")
            return
        cursor = db.connection.cursor()
        cursor.executemany(
            "INSERT INTO buses (VehicleUniqueId, DestinationName, PublishedLineName, Bearing, Latitude, Longitude, RecordedAtTime, ValidUntilTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", bus_data)
        db.connection.commit()
        # logger.info("Data inserted")
    except Exception as e:
        logger.error("Unable to populate database" + str(e))
    finally:
        logger.info("Database populated")
        try:
            logger.info("Notifying clients of update...")
            server.emit("update_buses")
        except Exception as e:
            logger.error("Unable to notify clients" + str(e))
