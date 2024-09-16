from django.shortcuts import render
from visits.models import PageVisit
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

LOGIN_URL = settings.LOGIN_URL

def home_view_page(request, *args, **kwargs):
    PageVisit.objects.create()
    queryset = PageVisit.objects.all()
    count = queryset.count
    context = {
        'title': 'Home',
        'queryset': queryset,
        'count': count
    }
    return render(request, 'home.html', context)

VALID_CODE = "1234"

def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    if request.method == 'POST':
        user_pw_sent = request.POST.get('code')
        if user_pw_sent == VALID_CODE:
            request.session['protected_page_allowed'] = 1
    if is_allowed:
        return render(request, 'protected/view.html', {})
    return render(request, 'protected/entry.html', {})

@login_required
def user_only_view(request, *args, **kwargs):
    return render(request, 'protected/user-only.html', {})

@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, 'protected/staff_only.html', {})