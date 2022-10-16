from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Создает и регистрирует дополнительный фильтр для шаблона"""
    return field.as_widget(attrs={'class': css})
