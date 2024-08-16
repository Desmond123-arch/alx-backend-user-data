#!/usr/bin/env python3
""" Contains the flask app instance """
from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """ Flask route for home page"""
    return jsonify({"message": "Bienvenue"})
