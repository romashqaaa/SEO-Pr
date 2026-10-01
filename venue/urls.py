from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.sitemaps.views import sitemap
from venue.sitemaps import StaticViewSitemap, HallSitemap

app_name = "venue"

sitemaps = {
    'static': StaticViewSitemap,
    'halls': HallSitemap,
}

urlpatterns = [
    path("", views.home, name="home"),

    # SEO-ЗАДАНИЕ (дубли страниц):
    # Главная страница доступна по двум адресам: / и /home/. Для поисковика это
    # два разных URL с одинаковым контентом — дубль.
    # ПОДСКАЗКА: варианты решения — 301-редирект (RedirectView с permanent=True)
    # или <link rel="canonical">. Что лучше в этом случае и почему?
    path("home/", views.home, name="home_duplicate"),

    path("halls/", views.hall_list, name="hall_list"),
    # SEO-ЗАДАНИЕ (ЧПУ): замените <int:pk> на <slug:slug> (см. venue/models.py)
    path("halls/<int:pk>/", views.hall_detail, name="hall_detail"),

    path("menu/", views.menu, name="menu"),
    path("events/", views.events, name="events"),
    path("afisha/", views.poster_list, name="poster_list"),
    # SEO-ЗАДАНИЕ (ЧПУ): и здесь <int:pk> → <slug:slug>
    path("afisha/<int:pk>/", views.poster_detail, name="poster_detail"),
    path("gallery/", views.gallery, name="gallery"),
    path("contacts/", views.contacts, name="contacts"),
    path("booking/", views.booking, name="booking"),
    path(
        'robots.txt',
        TemplateView.as_dict(
            template_name='robots.txt',
            content_type='text/plain'
        ) if hasattr(TemplateView, 'as_dict') else TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain'
        ),
        name='robots',
    ),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
]
