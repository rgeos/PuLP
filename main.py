#!/usr/bin/env python

# Set the path
import os
import sys

from flask_script import Manager, Server

from voting.app import run_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

manager = Manager(run_app)

# Turn on debugger by default and reloader
manager.add_command("run", Server(
	use_debugger=True,
	use_reloader=True,
	host='0.0.0.0',
	port=8001
))

if __name__ == "__main__":
	manager.run()
