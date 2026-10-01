from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from . import views
from django.contrib.sitemaps.views import sitemap
from venue.sitemaps import StaticViewSitemap, HallSitemap

app_name = "venue"

sitemaps = {
    'static': StaticViewSitemap,
    'halls': HallSitemap,
}

urlpatterns = [
    # --- ГЛАВНАЯ СТРАНИЦА И ЕЁ ДУБЛЬ ---
    path('', views.home, name='home'),
    path('home/', RedirectView.as_view(url='/', permanent=True)), 
    
    # --- ЗАЛЫ ---
    path('halls/', views.hall_list, name='hall_list'),
    
    path('halls/<slug:slug>/', views.hall_detail, name='hall_detail'),

    # --- АФИША (СОБЫТИЯ) ---
    path('afisha/', views.poster_list, name='poster_list'),
    path('afisha/<slug:slug>/', views.poster_detail, name='poster_detail'),
    
    # --- МЕРОПРИЯТИЯ ---
    path('events/', views.events, name='events'),
    
    # --- МЕНЮ (ИМЕННО ЭТОГО НЕ ХВАТАЛО) ---
    path('menu/', views.menu, name='menu'),
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
