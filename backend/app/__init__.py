from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from db.database_connection import DatabaseConnection
from db.database_utils import setup_database, populate_database
from db.database_utils import populate_buses, populate_database_data
from .routes import setup_routes

from apscheduler.schedulers.background import BackgroundScheduler
import logging as logger

scheduler = BackgroundScheduler()


def create_app():
    app = Flask(__name__)
    server = SocketIO(app, cors_allowed_origins="*")

    CORS(app)

    db = DatabaseConnection()
    setup_routes(app, db)

    logger.getLogger(__name__)
    logger.basicConfig(level=logger.INFO)

    def populate_database_wrapper():
        populate_database(db, server)
        populate_buses(db, server)

    logger.info("Starting scheduler")
    scheduler.add_job(func=populate_database_wrapper,
                      trigger="interval", seconds=15)
    scheduler.start()

    return app
