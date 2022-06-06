#!/usr/bin/env python

from flask import Response, jsonify
from flask import Flask
import os
import logging.config
import logging
import sqlite3

logging.config.fileConfig(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/logger.conf"))
logger = logging.getLogger(__name__)

APP_NAME = "DevNet Expert Storage Status API"

app = Flask(APP_NAME)


@app.route("/api/v1/status")
def get_status() -> Response:
    """Fetch the status from the database and display it."""

    db_file = os.environ.get("STORAGE_API_DB", "./storage.db")
    if not os.path.isfile(db_file):
        return jsonify({"result": "error", "msg": f"Database file {db_file} does not exist or is not a file"}), 500

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    results = []
    for row in cur.execute("SELECT * FROM storage_elements"):
        element = {}
        for key in row.keys():
            element[key] = row[key]

        results.append(element)

    cur.close()
    conn.close()

    return jsonify(results)


if __name__ == "__main__":
    app.run(port=os.environ.get("PORT", 80), host="0.0.0.0", threaded=True)
