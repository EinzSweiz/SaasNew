from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
LOGIN_URL = settings.LOGIN_URL


@login_required
def profile_list_view(request, *args, **kwargs):
    context = {
        'object_list': User.objects.filter(is_active=True)
    }
    return render(request, 'profile/list.html', context)

@login_required(login_url=LOGIN_URL)
def profile_view(request, username, *args, **kwargs):
    user = request.user
    # user_groups = user.groups.all()
    print(
        user.has_perm('subscriptions.basic'),
        user.has_perm('subscriptions.pro'),
        user.has_perm('subscriptions.advanced'),
        user.has_perm('subscriptions.basic_ai'),

    )
    # obj from Permission(django.contrib.auth.models) and from obj.content_type.app_label and .codename 
    print(user.has_perm('auth.view_user'))
    print(user.has_perm('visits.view_pagevisit'))


    user_obj = get_object_or_404(User, username=username)
    is_me = user_obj == user
    # if user_groups.filter(name__icontains='basic'):
    #     return HttpResponse('Congrats')
    if is_me:
        return HttpResponse(f'Hello: {user.username} - {is_me}')
    elif user.is_superuser:
        return HttpResponse('You are superuser that\'s why you have access to all users')
    else:
        return HttpResponse(f'Unfortunately you are not that user please try only with your username: {user.username}') 
