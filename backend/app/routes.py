from flask import Blueprint, jsonify
import os
from dotenv import load_dotenv
import requests
import xmltodict


def setup_routes(app):
    main = Blueprint("main", __name__)

    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    @main.route("/api/data", methods=["GET"])
    def get_data():
        url = "https://data.bus-data.dft.gov.uk/api/v1/datafeed/?boundingBox=-1.466675,52.539197,-0.997009,52.802761&api_key=" + api_key
        xml_response = requests.get(url)
        json_response = xmltodict.parse(xml_response.text)        
        return jsonify(json_response)

    app.register_blueprint(main)