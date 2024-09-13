from django.shortcuts import render
from visits.models import PageVisit



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