import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
import traceback

from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    try:
        if not err:
            print(token)
            return token
        else:
            server.logger.error(f"Error while logging: {err}\n{traceback.format_exc()}")
            return f"failed login: {err}", 401
    except Exception:
        server.logger.exception("Uncatched error in /login route")
        return "Internal server error", 500

@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    access = json.loads(access) #converts json string to python object

    if access["admin"]:
        if len(request.files) != 1:
            return "exactly one file required", 400
        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)
            if err:
                return err
        
        return "success!", 200
    else:
        return "not authorized", 401

@server.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host = "0.0.0.0", port=8080, debug=True)
