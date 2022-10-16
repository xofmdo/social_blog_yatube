from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """ Выводит страницу с информацией об авторе. Еще в доработке шаблон!!!"""
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """ Выводит страницу с технологиями"""
    template_name = 'about/tech.html'
