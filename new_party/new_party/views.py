from django.shortcuts import render


def permission_denied(request, exception, template_name='403.html'):
    return render(request, template_name)
