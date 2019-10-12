import sentry
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from db import *


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


def verify_auth(auth, scope="core"):
    url = "http://nisb-auth.herokuapp.com/auth" + \
        "?auth=" + auth + \
        "&scope=" + scope
    r = requests.get(url)
    return r.status_code == 200

# Does nothing
@app.route('/')
def index():
    return jsonify({
        "status": "ok"
    })


@app.route("/members/count")
def members_count_controller():
    if not verify_auth(request.args.get("auth")):
        return jsonify({
            "status": "error",
            "error": "auth is not valid"
        }), 403

    return jsonify({"count": get_members_count()})


@app.route("/members", methods=["GET"])
def members_controller():
    if not verify_auth(request.args.get("auth")):
        return jsonify({
            "status": "error",
            "error": "auth is not valid"
        }), 403

    page_no = request.args.get("page_no", None)
    items_per_page = request.args.get("items_per_page", "50")

    members, err = get_members(page_no, items_per_page)
    if err:
        return jsonify({
            "status": "error",
            "error": err.message
        })
    return jsonify(members)


@app.route("/member", methods=["GET", "PUT", "POST", "DELETE"])
def member_controller():
    if not verify_auth(request.args.get("auth")):
        return jsonify({"status": "error", "error": "auth is not valid"}), 403
    # get member
    if request.method == "GET":
        email = request.args.get("email", "none")
        member, err = get_member(email)
        if err:
            return jsonify({
                "status": "error",
                "error": err.message
            })

        return jsonify(member)
    # update member
    elif request.method == "PUT":
        email = request.args.get("email", "none")
        member_dict = request.get_json()
        _, err = update_member(email, member_dict)
        if err:
            return jsonify({
                "status": "error",
                "error": err.message
            })
        return jsonify({"status": "ok"})

    elif request.method == "DELETE":
        email = request.args.get("email", "none")
        _, err = delete_member(email)
        if err:
            return jsonify({
                "status": "error",
                "error": err.message
            })
        return jsonify({"status": "ok"})

    elif request.method == "POST":
        member_dict = request.get_json()
        if not validate_member(member_dict):
            return jsonify({
                "status": "error",
                "error": "Invalid Input"
            }), 400
        _, err = add_member(member_dict)
        if err:
            return jsonify({
                "status": "error",
                "error": err.message
            })
        return jsonify({"status": "ok", "email": member_dict["email"]})


if __name__ == '__main__':
    # session["login"] = False
    app.run(host='0.0.0.0', debug=True)
