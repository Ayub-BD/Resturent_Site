from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def manager_required(view_func):
    """
    Combines login_required with a staff/superuser check, so a logged-in
    customer (if that ever exists) still can't reach the dashboard --
    only accounts with is_staff/is_superuser (managers) can.
    """

    @wraps(view_func)
    @login_required(login_url="dashboard_login")
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("You do not have manager access.")
        return view_func(request, *args, **kwargs)

    return wrapper
