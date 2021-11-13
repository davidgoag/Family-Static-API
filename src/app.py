"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/members', methods=['GET'])
# def handle_hello():

#     # this is how you can use the Family datastructure by calling its methods
#     members = jackson_family.get_all_members()
#     response_body = {
#         "hello": "world",
#         "family": members
#     }
# return jsonify(response_body), 200

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    res = {
        "message": "Ok",
        "Family members": members
    }
    return jsonify(res), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        res = {
            "message": "Ok",
            "Family member": member
        }
        return jsonify(res), 200

    res = {"message": "User not found",}
    return jsonify(res), 404

@app.route('/member/', methods=['POST'])
def add_member():
    added_member = json.loads(request.data)
    members = jackson_family.add_member(added_member)
    
    res = {
        "message": "Ok",
        "Family members": members
    }
    return jsonify(res), 200
    
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    members = jackson_family.delete_member(member_id)
    res = {
        "message": "Ok",
        "Family member": members
    }
    return jsonify(res), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
