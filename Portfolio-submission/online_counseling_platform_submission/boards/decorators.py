from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Counselor

def counselor_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if isinstance(request.user, Counselor):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view
