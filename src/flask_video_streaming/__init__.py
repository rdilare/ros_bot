#!/usr/bin/env python2

from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketApp=SocketIO(app)
