from flask import Blueprint, request, jsonify, g

from controller.request_response_auth import requires, make_general_response, authorize_request, extract_if_user
from controller.user import sign_up_user, login_user, user_exist
from codes.response_code import FAIL
from codes.status_code import BAD_REQUEST, OK

user_views = Blueprint("user_views", __name__, url_prefix='')


@user_views.route("/signup", methods=["POST"])
@requires(["email", "password"])
def sign_up():
    request_body = request.get_json()
    email = request_body.pop("email")
    password = request_body.pop("password")
    return sign_up_user(email, password, **request_body), OK


@user_views.route("/login", methods=["POST"])
@requires(["email", "password"])
def login():
    request_body = request.get_json()
    email = request_body["email"]
    password = request_body["password"]
    user = user_exist(email)
    if user:
        return (login_user(user, password)), OK
    else:
        response = make_general_response(FAIL, "User don't exist.Sign up first")
        return response, BAD_REQUEST


@user_views.route("/get_user/<user_id>", methods=["GET"])
@extract_if_user
@authorize_request
def read_user(user_id):
    user = g.user
    sensitive_list = ["email", "password", "_id", "session_key"]
    for item in sensitive_list:
        if item in user:
            user.pop(item)
    return jsonify(user)
