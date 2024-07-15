import os
from flask import Flask, redirect, url_for, session, request, jsonify, g, json
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
CORS(app)
