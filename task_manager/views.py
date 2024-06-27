from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        context = {'label': 'Привет от выпускника школы Хекслета!',
                   'description': 'Я Прошла обучение по программе "Python - разработчик". \
                                   За время обучения, оформила четыре учебных проекта в GitHub. \
                                   Мне интересно расти и развиваться. \
                                   Сейчас в поиске работы на должность Python-разработчика. \
                                   Если у Вас есть какие-то предложения о работе, пишите мне. \
                                   Если хотите узнать, что я изучала в Хекслете, то жмите на кнопку.',
                   'button': 'Узнать больше'}
        return render(request, 'index.html', context=context)
