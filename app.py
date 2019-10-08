from flask import Flask, request, jsonify
from db import *
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def verify_auth(auth):
    r = requests.get("http://nisb-auth.herokuapp.com/auth?auth="+auth)
    return r.status_code == 200

# Does nothing
@app.route('/')
def index():
    return jsonify({
        "status": "ok"
    })


@app.route("/members", methods=["GET"])
def members_controller():
    if not verify_auth(request.args.get("auth")):
        return jsonify({"status": "error", "error": "auth is not valid"}), 403
    members = get_members()
    if members:
        return jsonify(members)
    return jsonify({
        "status": "error",
        "error": "no member exists"
    })


@app.route("/member", methods=["GET", "PUT", "POST", "DELETE"])
def member_controller():
    if not verify_auth(request.args.get("auth")):
        return jsonify({"status": "error", "error": "auth is not valid"}), 403
    if request.method == "GET":
        email = request.args.get("email")
        member = get_member(email)
        if member:
            return jsonify(member)
        else:
            return jsonify({
                "status": "error",
                "error": "member not found"
            })

    elif request.method == "PUT":
        member_dict = request.get_json()
        update_member(member_dict)
        return jsonify({"status": "ok"})

    elif request.method == "DELETE":
        email = request.args.get("email")
        delete_member(email)
        return jsonify({"status": "ok"})

    elif request.method == "POST":
        member_dict = request.get_json()
        add_member(member_dict)
        return jsonify({"status": "ok"})


if __name__ == '__main__':
    # session["login"] = False

    app.run(host='0.0.0.0', debug=True)
