"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object*
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member', methods=['POST'])
def new_member():
    body = request.json
    if body.get("first_name", False) == False:
        return "First name is required", 400
    
    if body.get("age", False) == False:
        return "Age is required", 400
    
    if body.get("lucky_numbers", False) == False:
        return "Lucky numbers are required", 400
    
    new_person = jackson_family.add_member(body)
    return jsonify(new_person), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    delete = jackson_family.delete_member(member_id)
    if delete == None:
        return "Member not found", 404
    return jsonify(
        {
            "done": True
        }
    ), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):

    search_member = jackson_family.get_member(member_id)

    if search_member == None:
        return "Member not found",
    
    return search_member, 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)