from functools import wraps
from flask import request, g

from codes.response_code import FAIL, PARAMETER_MISSING, MISSING_TOKEN, INVALID_TOKEN
from codes.status_code import BAD_REQUEST, UNAUTHORIZED
from model.user import read_user_by_id


def verify_param(required, received):
    for req in required:
        if req in received:
            pass
        else:
            return req
    return None


def make_general_response(code, detail):
    response = {
        "response_code": code,
        "response_detail": detail
    }
    return response


def requires(fields, **agr):
    def inner(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            body = request.get_json()
            if body is None:
                response = make_general_response(FAIL, "FAIL")
                return response, BAD_REQUEST

            missing = verify_param(fields, body)
            if missing:
                response = make_general_response(PARAMETER_MISSING, missing + " is missing")
                return response, BAD_REQUEST
            else:
                return f(*args, **kwargs)

        return wrap

    return inner


def extract_if_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_id = kwargs["user_id"]
        try:
            user = read_user_by_id(user_id)
        except:
            user = None
        g.user = user
        if user is None:
            response = make_general_response(FAIL, "User doesn't exists")
            return response
        return f(*args, **kwargs)

    return wrap


def authorize_request(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None
        headers = request.headers
        if "x-access-token" in headers:
            token = headers["x-access-token"]
        if not token:
            response = make_general_response(MISSING_TOKEN, 'token is missing')
            return response, UNAUTHORIZED

        try:
            algorithms = ["HS256"]
            from controller import user
            valid, reason = user.validate_session_key(g.user, token)
            if not valid and reason == "Expired":
                response = make_general_response(INVALID_TOKEN, 'Session Expired.login Again')
                return response, UNAUTHORIZED
            if valid:  # db== data:
                return f(*args, **kwargs)
            response = make_general_response(INVALID_TOKEN, 'token is invalid')
            return response, UNAUTHORIZED
        except:
            response = make_general_response(INVALID_TOKEN, 'token is invalid')
            return response, UNAUTHORIZED

    return wrap
