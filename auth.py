from flask import redirect, url_for, session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("web.login"))
        return f(*args, **kwargs)
    return decorated_function