import json
from flask import Blueprint, request

if __name__ == "__main__":
    import users
    import calculator_service as CS
else:
    from . import users
    from . import calculator_service as CS

bp = Blueprint('retirement_calculator', __name__, url_prefix = '/retirement_calculator')

@bp.route('/<string:id>', methods = ["GET"])
def get_retirement_calc_by_id(id):
    try:
        user = users.get_user_by_id(int(id))
    except:
        user = None
    if not user:
        # log the error message, gussy up this response with appropriate http error codes and stuff
        return json.dumps({'error': "user could not be found"})
    try:
        res = get_retirement_calc(user)
    except:
        # log the error message, gussy up this response with appropriate http error codes and stuff
        res = {'error': "error on server"}
    
    return json.dumps(res)

@bp.route('/', methods = ["POST"])
def get_retirement_calc():
    try:
        user = users.User(**request.json)
    except:
        # log the error message, gussy up this response with appropriate http error codes and stuff
        return json.dumps({'error': "cannot parse request as user object"})
    try:
        res = get_retirement_calc(user)
    except:
        # log the error message, gussy up this response with appropriate http error codes and stuff
        res = {'error': "error on server"}
    return json.dumps(res)


def get_retirement_calc(
    user: users.User
) -> dict:
    saved, needed = CS.retirement_info_by_user(user)
    return {
        "saved": saved,
        "needed": needed
    }