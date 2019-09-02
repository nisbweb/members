from flask import Flask, request, jsonify
from db import *

app = Flask(__name__)

# Does nothing
@app.route('/')
def index():
    return jsonify({
        "status":"ok"
    })

@app.route("/member", methods=["GET","PUT","POST","DELETE"])
def member_controller():
    if request.method=="GET":
        email = request.args.get("email")
        member = get_member(email)
        return jsonify(member)
    elif request.method=="PUT":
        member_dict = request.get_json()
        update_member(member_dict)
        return jsonify({"status":"ok"})
    elif request.method=="DELETE":
        email = request.args.get("email")
        delete_member(email)
        return jsonify({"status":"ok"})
    elif request.method=="POST":
        member_dict = request.get_json()
        add_member(member_dict)
        return jsonify({"status":"ok"})
            

if __name__ == '__main__':
    # session["login"] = False

    app.run(host='0.0.0.0', debug=True)
