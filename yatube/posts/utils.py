from django.core.paginator import Paginator


# можно вынести переменную в сеттинг, но это менее удобно для изменения отображения во время дебага

def get_page_obj(request, posts):
    """Создание пагинатора и возвращения определенного
    количества постов на страницу"""
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
