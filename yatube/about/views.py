from django.shortcuts import render
from django.views.generic import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/about_author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Об авторе проекта'
        context['hello'] = 'Привет, Я Ростислав'

        context['profession'] = 'Python Developer'
        context['photo'] = 'yatube/static/img/about/IMG_1562.JPG'
        context['tg'] = 'https://t.me/rostisluvvv'
        context['git'] = 'https://github.com/rostisluvvv'
        context['text'] = ('Недавно у меня появилась маленькая IT мечта, '
                           'на которую меня подталкнул мой куратор (скорей '
                           'всего, сам того не зная), '
                           'а эта мечта в свою очередь стала целью на 2023 '
                           'год устроиться в компанию "Циан" ')

        return context


class AboutTechView(TemplateView):
    template_name = 'about/about_tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'О технологиях проекта'
        context['hello'] = 'На этой странице я расскажу о технологиях проекта'
        context['text'] = ('<ul>DJANGO</ul>'
                           '<ul>CSS</ul>'
                           '<ul>HTML</ul>'
                           '<ul>JS</ul>'
             
                           '<ul>Bootstrap</ul>')
        context['text_2'] = ('Благодаря этому спринту я нашел свои '
                             'пробелы в знаниях, например я даже не знал '
                             'отличия forms.Form vs forms.ModelForm, но были '
                             'и моменты с которыми я уже работал '
                             'самостоятельно и выполняя этот спринт '
                             'закрепил знания')

        return context
