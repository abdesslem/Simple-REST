from werkzeug.exceptions import Unauthorized

from config import ADMIN_APIKEY

tokeninfo = {ADMIN_APIKEY: {"uid": 1}}


def check(token, required_scopes):
    if not tokeninfo.get(token, None):
        raise Unauthorized("Invalid token")

    return tokeninfo
