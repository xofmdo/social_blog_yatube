from django.utils import timezone


def year(request) -> dict:
    """Добавляет переменную с текущим годом."""
    year = timezone.now().year
    return {
        'year': year
    }
