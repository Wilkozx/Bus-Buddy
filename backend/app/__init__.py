from flask import Flask
from flask_cors import CORS

from db.database_connection import DatabaseConnection
from db.database_utils import setup_database, populate_database
from .routes import setup_routes

from apscheduler.schedulers.background import BackgroundScheduler
import logging as logger

scheduler = BackgroundScheduler()


def create_app():
    app = Flask(__name__)
    CORS(app)

    db = DatabaseConnection()
    setup_routes(app, db)
    setup_database(db)

    logger.getLogger(__name__)
    logger.basicConfig(level=logger.INFO)

    logger.info("Starting scheduler")

    def populate_database_wrapper():
        populate_database(db)

    scheduler.add_job(func=populate_database_wrapper,
                      trigger="interval", seconds=15)
    scheduler.start()

    return app
