from django.shortcuts import resolve_url
from django.http import HttpResponse

def bx_redirect(to, *args, **kwargs):
    """
    Редиректит либо через window.top, если мы в iframe, 
    либо обычный window.location для прямого доступа.
    Принимает всё то же, что и django.shortcuts.redirect.
    """
    url = resolve_url(to, *args, **kwargs)
    html = f"""
    <html><head></head><body>
      <script>
        const target = "{url}";
        // если наша страница в iframe – лезем наверх
        if (window.top !== window.self) {{
          window.top.location.href = target;
        }} else {{
          window.location.href = target;
        }}
      </script>
    </body></html>
    """
    return HttpResponse(html)