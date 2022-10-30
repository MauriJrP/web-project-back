from flask import Blueprint, jsonify, request
from src.models.InvalidToken import InvalidToken
from src.helpers import get_user, remove_user, encrypt_pwd, check_pwd
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, \
    jwt_required
from src.app import jwt
from flask_cors import cross_origin

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
@cross_origin(origin="*")
def login():
    """
    User login end-point accepts email and password.
    returns jwt_token
    """
    try:
        # print(request.get_json())
        email = request.json["email"]
        pwd = request.json["pwd"]

        if email and pwd:
            # check if user exists in database and password is correct
            user = list(filter(lambda x: x.email == email and check_pwd(pwd, x.pwd), User.get_all()))

            if len(user) > 0:
                token = create_access_token(identity=user[0].id)
                refresh_token = create_refresh_token(identity=user[0].id)
                return jsonify({"message": "success", "token": token, "refreshToken": refresh_token}), 200
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
        email = request.json["email"]
        pwd = encrypt_pwd(request.json['pwd'])
        address = request.json["address"]

        user = User(firstName, lastName, email, pwd, address)
        
        user.save()

        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid request"}), 400


@auth.route("/checkiftokenexpire", methods=["POST"])
@jwt_required()
def check_if_token_expire():
    """
    End-point for frontend to check if the token has expired or not
    """
    return jsonify({"success": True}), 200


@auth.route("/refreshtoken", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    End-point to refresh the token when required
    
    """
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)
    return jsonify({"token": token}), 200

@auth.route("/getcurrentuser")
@jwt_required()
def current_user():
    """
    End-point to handle collecting the current user information
    """
    uid = get_jwt_identity()
    user = User.get_one(uid)
    user = {"firstName": user.firstName, "lastName": user.lastName, "email": user.email, "address": user.address}
    return jsonify(user), 200


@auth.route("/logout/access", methods=["POST"])
@jwt_required()
def access_logout():
    """
    End-point to log the user out and Invalidate the token.
    """
    jti = get_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success":True}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@auth.route("/logout/refresh", methods=["POST"])
@jwt_required()
def refresh_logout():
    """
    End-point to invalidate the token.
    Can be used with both log the user out or for the frontend to call after refreshing the token.

    """
    
    jti = get_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@auth.route("/deleteaccount", methods=["DELETE"])
@jwt_required()
def delete_account():
    """
    End-point to handle removal of users
    """
    try:
        user = get_user(get_jwt_identity())
        remove_user(user.id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500