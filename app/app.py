from flask import Flask, make_response, request
import socket
import pymysql
import os

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=3306,
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "secret"),
        database=os.environ.get("DB_NAME", "practice"),
    )


@app.route("/")
def home():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    client_ip = request.remote_addr

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE counter SET hits = hits + 1 WHERE id = 1")
    cursor.execute(
        "INSERT INTO access_log (access_time, client_ip, internal_ip) VALUES (NOW(), %s, %s)",
        (client_ip, ip),
    )
    connection.commit()
    connection.close()

    response = make_response(ip)
    response.set_cookie("server_ip", ip, max_age=300)
    return response


@app.route("/showcount")
def showcount():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT hits FROM counter WHERE id = 1")
    row = cursor.fetchone()
    connection.close()
    return str(row[0])


app.run(host="0.0.0.0", port=5000)    # CHANGED