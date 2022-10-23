from flask import Blueprint, jsonify, request
from src.models import InvalidToken
from src.helpers import get_users, get_user, add_user, remove_user, encrypt_pwd, check_pwd
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, \
    jwt_required
from src.app import jwt

from src.models.User import User


auth = Blueprint('auth', __name__)

@jwt.token_in_blocklist_loader
def check_if_blacklisted_token(data, decrypted):
    """
    Decorator designed to check for blacklisted tokens
    """
    jti = decrypted['jti']
    return InvalidToken.is_invalid(jti)

@auth.route("/login", methods=["POST"])
def login():
    """
    User login end-point accepts email and password.
    returns jwt_token
    """
    try:
        # print(request.json)
        username = request.json["username"]
        pwd = request.json["pwd"]
        print(username, pwd)
        if username and pwd:
            user = list(filter(lambda x: x["username"] == username and check_pwd(pwd, x["pwd"]), get_users()))
            if len(user) == 1:
                token = create_access_token(identity=user[0]["id"])
                refresh_token = create_refresh_token(identity=user[0]["id"])
                return jsonify({"token": token, "refreshToken": refresh_token}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401
        else:           
            return jsonify({"error": "Invalid credentials"}), 401
    except:
        return jsonify({"error": "Invalid request"}), 400

@auth.route("/register", methods=["POST"])
def register():
    """
    End-point to handle user registration, encrypting the password and validating the email
    """
    try:
        firstName = request.json["firstName"]
        lastName = request.json["lastName"]
        pwd = encrypt_pwd(request.json['pwd'])
        email = request.json["email"]
        address = request.json["address"]

        user = User(firstName, lastName, pwd, email, address)
        
        print(f'Users: {user.get_all()}')
        user.save()
        print(f'Users: {user.get_all()}')

        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid request"}), 400
