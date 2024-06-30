from flask import Blueprint, jsonify
import os
from dotenv import load_dotenv
import requests
import xmltodict


def setup_routes(app, db):
    main = Blueprint("main", __name__)

    load_dotenv()
    api_key = os.getenv("API_KEY")

    @main.route("/api/data/<string:bus_number>", methods=["GET"])
    def get_bus_data(bus_number):
        url = "https://data.bus-data.dft.gov.uk/api/v1/datafeed/?boundingBox=-1.466675,52.539197,-0.997009,52.802761&api_key={}&lineRef={}".format(
            api_key, bus_number)
        xml_response = requests.get(url)
        json_response = xmltodict.parse(xml_response.text)
        return jsonify(json_response)

    @main.route("/api/data", methods=["GET"])
    def get_test_data():
        result = db.execute_query("SELECT * FROM buses")

        formatted_result = []
        for row in result:
            bus_data = {
                "id": row[0],
                "vehicle_unique_id": row[1],
                "block_ref": row[2],
                "destination_aimed_arrival_time": row[3],
                "destination_name": row[4],
                "destination_ref": row[5],
                "direction_ref": row[6],
                "line_ref": row[7],
                "operator_ref": row[8],
                "origin_aimed_depature_time": row[9],
                "origin_name": row[10],
                "origin_ref": row[11],
                "published_line_name": row[12],
                "bearing": row[13],
                "latitude": row[14],
                "longitude": row[15],
                "recorded_at_time": row[16],
                "valid_until_time": row[17],
                "inserted_at_time": row[18],
                "updated_at_time": row[19],
            }
            formatted_result.append(bus_data)

        return jsonify(formatted_result)

    app.register_blueprint(main)
