from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        context = {'label': 'Привет от Хекслета!',
                   'description': 'Практические курсы по программированию',
                   'button': 'Узнать больше'}
        return render(request, 'index.html', context=context)
