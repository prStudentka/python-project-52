from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={'label':'Привет от Хекслета!', 'description':'Практические курсы по программированию', 'button': 'Узнать больше'})
