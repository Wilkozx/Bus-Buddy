import requests
import xmltodict
import os
from dotenv import load_dotenv
import logging as logger
import zipfile
import urllib.request


def populate_database_data(db):
    if not os.path.exists('timetable_data'):
        get_dataset_from_api()
    else:
        logger.info("Timetable data already exists")


def get_dataset_from_api():
    try:
        url = "https://data.bus-data.dft.gov.uk/timetable/download/bulk_archive/EM"
        filename = "catalogue.zip"
        logger.info("Retrieving timetable data")
        response = urllib.request.urlretrieve(url, filename)
        logger.info("Timetable Data retrieved, parsing...")

        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall("timetable_data")

        unzip_recursive("timetable_data")

        i = 0
        for file in os.listdir("timetable_data"):
            for file2 in os.listdir("timetable_data/" + file):
                if file2.endswith(".xml"):
                    i += 1
        logger.info(f"Found {i} xml files in timetable data")
    finally:
        logger.info("Timetable Data retrieved")
        os.remove(filename)


def unzip_recursive(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            unzip_recursive(item_path)

        elif item_path.endswith(".zip"):
            with zipfile.ZipFile(item_path, 'r') as zip_ref:
                zip_ref.extractall(directory)
                os.remove(item_path)
                logger.info(f"Unzipped {item_path}")




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
