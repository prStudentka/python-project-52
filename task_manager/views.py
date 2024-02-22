from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View
from django.http import HttpResponse


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={'label':'Привет от Хекслета!', 'description':'Практические курсы по программированию', 'button': 'Узнать больше'})


def rollbar_index(request):
    a = None
    a.hello() # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")