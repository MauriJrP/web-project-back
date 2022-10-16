from flask import Blueprint, jsonify, request

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET'])
def auth_get():
    return jsonify({'message': 'Hello World Get'})

@auth.route('/', methods=['POST'])
def auth_post():
    return jsonify({'message': 'Hello World Post'})

@auth.route('/', methods=['PUT'])
def auth_put():
    return jsonify({'message': 'Hello World Put'})

@auth.route('/', methods=['DELETE'])
def auth_delete():
    return jsonify({'message': 'Hello World Delete'})