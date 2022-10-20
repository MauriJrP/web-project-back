from flask import Blueprint, jsonify, request
from src.models import InvalidToken
from src.helpers import get_users, get_user, add_user, remove_user, encrypt_pwd, check_pwd
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, \
    jwt_required
from src.app import jwt


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
                return jsonify({"token": token, "refreshToken": refresh_token})
            else:
                return jsonify({"error": "Invalid credentials"})
        else:           
            return jsonify({"error":"Invalid Form"})
    except:
        return jsonify({"error": "Invalid request"})

@auth.route("/register", methods=["POST"])
def register():
    """
    End-point to handle user registration, encrypting the password and validating the email
    """
    try:
        pwd = encrypt_pwd(request.json['pwd'])
        username = request.json['username']
        
        users = get_users()
        print(users)
        # if len(list(filter(lambda x: x["username"] == username, users))) == 1:         
        #     return jsonify({"error": "Invalid Form"})
        # add_user(username, pwd)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})


# @auth.route('/', methods=['GET'])
# def auth_get():
#     return jsonify({'message': 'Hello World Get'})