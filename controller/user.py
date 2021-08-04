from hashlib import sha256
from jwt import encode, decode
from model.user import read_user_by_email, write_user, update_user_session_key
import datetime
from flask import current_app
from config.config import TOKEN_EXPIRY_SECONDS
from controller.request_response_auth import make_general_response
from codes.response_code import FAIL, SUCCESS
from codes.status_code import UNAUTHORIZED, OK
import base64


def user_exist(email):
    user = read_user_by_email(email)
    if user:
        return user
    return False


def sign_up_user(email, password, **kwargs):
    user = read_user_by_email(email)
    user_already_exist = True
    if not user:
        create_new_user(email, password, **kwargs)
        user = read_user_by_email(email)
        if user:
            response = make_general_response(SUCCESS, f"New User Signed Up with id {user['_id']}")
            return response
        else:
            return make_general_response(FAIL, "fail")
    return login_user(user, password, sign_up_flow=user_already_exist)


def validate_session_key(user,session_key):
    algorithms = ["HS256"]
    data = decode(session_key, current_app.config["SECRET_KEY"], algorithms=algorithms)
    if user["email"] != data["email"]:
        return False, UNAUTHORIZED
    if data["expires_at"] < datetime.datetime.now().isoformat():
        return False, "Expired"
    return True, OK


def login_user(user, password, sign_up_flow=False):
    session_key = None
    if user["password"] == sha256(password.encode("ascii")).hexdigest():
        user = read_user_by_email(user["email"])
    else:
        if sign_up_flow:
            msg = "User Already existed."
        else:
            msg =  "Wrong Login Attempt"
        response = make_general_response(FAIL,msg)
        return response
    if user.get("session_key", None):
        encoded_session_key = user["session_key"]
        session_key = base64.b64decode(encoded_session_key).decode("ascii")
        valid, reason= validate_session_key(user,session_key)
        if not valid and reason == "Expired":
            session_key = generate_jwt_session_key(user)
    else:
        session_key = generate_jwt_session_key(user)
    if not session_key:
        response = make_general_response(FAIL, "Failed")
        return response
    else:
        encoded_session_key = base64.b64encode(session_key.encode("ascii"))
        update_user_session_key(user, encoded_session_key)
    if sign_up_flow:
        msg = "User Already existed. User logged in successfully"
    else:
        msg = "Login Successful"
    response = make_general_response(SUCCESS, msg)
    response["session_key"] = session_key
    response["id"] = str(user["_id"])
    return response


def generate_jwt_session_key(user):
    current_time = datetime.datetime.now()
    expiry_time = current_time + datetime.timedelta(seconds=TOKEN_EXPIRY_SECONDS)
    data = {
        "email": user["email"],
        "login_at": current_time.isoformat(),
        "expires_at": expiry_time.isoformat()
    }
    session_key = encode(data, current_app.config["SECRET_KEY"])
    return session_key


def create_new_user(email, password, **kwargs):
    user = {
        "email": email,
        "password": sha256(password.encode("ascii")).hexdigest()
    }
    user.update(**kwargs)
    return write_user(user)
