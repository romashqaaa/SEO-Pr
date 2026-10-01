from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Hall

class StaticViewSitemap(Sitemap):
    """Карта для статических страниц сайта"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Только публичные страницы. Без дублей и служебных страниц!
        return [
            'venue:home',
            'venue:hall_list',
            'venue:menu',
            'venue:events',
            'venue:gallery',
            'venue:contacts',
        ]

    def location(self, item):
        return reverse(item)


class HallSitemap(Sitemap):
    """Карта для страниц конкретных залов"""
    changefreq = 'daily'
    priority = 1.0  # Максимальный приоритет для коммерческих страниц

    def items(self):
        # Отдаём только активные/доступные залы (если есть поле is_active)
        # Если такого поля нет — используем Hall.objects.all()
        if hasattr(Hall, 'is_active'):
            return Hall.objects.filter(is_active=True)
        return Hall.objects.all()

    def lastmod(self, obj):
        # Используем дата-штамп последнего изменения зала
        return obj.updated_at