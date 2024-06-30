# Create a bus table containing an id,
from flask import jsonify
import requests
import xmltodict
import os
from dotenv import load_dotenv
from db.database_connection import DatabaseConnection
import logging as logger


def setup_database(db):
    db.execute_query(
        "CREATE TABLE IF NOT EXISTS buses (id SERIAL PRIMARY KEY, VehicleUniqueId VARCHAR(255), BlockRef VARCHAR(255), DestinationAimedArrivalTime VARCHAR(255), DestinationName VARCHAR(255), DestinationRef VARCHAR(255), DirectionRef VARCHAR(255), LineRef VARCHAR(255), OperatorRef VARCHAR(255), OriginAimedDepatureTime VARCHAR(255), OriginName VARCHAR(255), OriginRef VARCHAR(255), PublishedLineName VARCHAR(255), Bearing VARCHAR(255), Latitude VARCHAR(255), Longitude VARCHAR(255), RecordedAtTime VARCHAR(255), ValidUntilTime VARCHAR(255), InsertedAtTime VARCHAR(255), UpdatedAtTime VARCHAR(255))"
    )


def populate_database(db):
    logger.getLogger(__name__)
    load_dotenv()
    api_key = os.getenv("API_KEY")
    try:
        logger.info("Retrieving data...")
        try:
            db.execute_query("TRUNCATE TABLE buses RESTART IDENTITY CASCADE")
        except Exception as e:
            logger.warning("unable to truncate table")
            return
        url = "https://data.bus-data.dft.gov.uk/api/v1/datafeed/?boundingBox=-1.466675,52.539197,-0.997009,52.802761&api_key=" + api_key
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
            destinationname = bus["MonitoredVehicleJourney"]["DestinationName"]
            publishedlinename = bus["MonitoredVehicleJourney"]["PublishedLineName"]
            bearing = bus["MonitoredVehicleJourney"]["Bearing"] if "Bearing" in bus["MonitoredVehicleJourney"] else None
            latitude = bus["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
            longitude = bus["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
            recordedattime = bus["RecordedAtTime"]
            validuntiltime = bus["ValidUntilTime"]

            bus_data.append((vehicleuniqueid, destinationname, publishedlinename, bearing,
                            latitude, longitude, recordedattime, validuntiltime))
        # logger.info("Data parsed, Inserting data...")
        cursor = db.connection.cursor()
        cursor.executemany(
            "INSERT INTO buses (VehicleUniqueId, DestinationName, PublishedLineName, Bearing, Latitude, Longitude, RecordedAtTime, ValidUntilTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", bus_data)
        db.connection.commit()
        # logger.info("Data inserted")
    except Exception as e:
        logger.error("Unable to populate database")
    finally:
        logger.info("Database populated")
