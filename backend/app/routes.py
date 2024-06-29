from flask import Blueprint, jsonify


def setup_routes(app):
    main = Blueprint("main", __name__)

    @main.route("/api/data", methods=["GET"])
    def get_data():
        return jsonify({"temp": "temp"})

    app.register_blueprint(main)