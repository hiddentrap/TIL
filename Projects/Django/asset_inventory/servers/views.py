# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    return render(request, 'servers.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })
