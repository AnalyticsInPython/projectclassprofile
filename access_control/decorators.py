from functools import wraps
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect


def class_access_required(view_function):
    @wraps(view_function)
    def wrapped(request, *args, **kwargs):
        if not settings.REQUIRE_CLASS_LOGIN:
            return view_function(request, *args, **kwargs)

        if request.session.get(settings.ACCESS_SESSION_KEY):
            return view_function(request, *args, **kwargs)

        query = urlencode({"next": request.get_full_path()})
        return redirect(f"/login/?{query}")

    return wrapped
