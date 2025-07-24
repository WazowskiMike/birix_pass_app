from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def master_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('is_master_authenticated'):
            login_url = reverse('login')
            return redirect(f'{login_url}?next={request.path}')
        return view_func(request, *args, **kwargs)
    return _wrapped