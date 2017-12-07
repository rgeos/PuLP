#!/usr/bin/env python

from flask import Flask

from voting.blueprints.page import page
from voting.extensions import db


def run_app():
	app = Flask(__name__)

	app.config.from_object('config.settings')
	app.logger.setLevel(app.config['LOG_LEVEL'])

	# blueprints
	app.register_blueprint(page)

	# extensions
	db.init_app(app)

	return app

