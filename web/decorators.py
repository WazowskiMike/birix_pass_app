from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def master_required(view_func):
    """
    Декоратор, который проверяет, установлен ли в сессии флаг
    is_master_authenticated. Если нет — перенаправляет на login-путь.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        # Проверяем в сессии признак авторизации
        if not request.session.get('is_master_authenticated'):
            # Перенаправляем на страницу логина с параметром next
            login_url = reverse('login')
            return redirect(f'{login_url}?next={request.path}')
        return view_func(request, *args, **kwargs)
    return _wrapped