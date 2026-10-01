import datetime

from django.contrib import messages
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import FAQ, EventFormat, Hall, MenuPackage, Poster, Review

# ПОДСКАЗКА (общая): мета-теги удобно формировать во view и передавать в шаблон,
# например: context["meta_title"] = f"{hall.name} — зал до {hall.capacity_banquet} гостей | Подземка"
# А в base.html выводить {{ meta_title|default:"..." }}. Либо переопределять блоки в шаблонах.


def home(request):
    reviews = Review.objects.filter(is_published=True)
    context = {
        "halls": Hall.objects.filter(is_active=True),
        "formats": EventFormat.objects.all()[:6],
        "packages": MenuPackage.objects.filter(is_featured=True)[:3],
        "reviews": reviews[:6],
        "rating": reviews.aggregate(avg=Avg("rating"))["avg"],
        "reviews_count": reviews.count(),
        "faqs": FAQ.objects.all(),
        "posters": upcoming_posters()[:6],
        "form": BookingForm(),
    }
    return render(request, "venue/home.html", context)


def hall_list(request):
    return render(request, "venue/hall_list.html", {
        "halls": Hall.objects.filter(is_active=True),
    })


def hall_detail(request, slug=None, pk=None):
    # Если передан старый ID, делаем 301 редирект
    if pk:
        hall = get_object_or_404(Hall, pk=pk)
        return redirect(hall.get_absolute_url(), permanent=True)
    
    # Ищем зал по slug. Если не найден, Django автоматически выдаст 404 страницу
    hall = get_object_or_404(Hall, slug=slug)
    
    # ОБЯЗАТЕЛЬНО должен быть return render(...)!
    return render(request, 'venue/hall_detail.html', {'hall': hall})


def upcoming_posters():
    """Будущие события + регулярные (у них заполнено поле schedule)."""
    return Poster.objects.filter(is_published=True).filter(
        Q(date__gte=datetime.date.today()) | ~Q(schedule=""),
    )


def poster_list(request):
    return render(request, "venue/poster_list.html", {
        "posters": upcoming_posters(),
    })


def poster_detail(request, slug=None, pk=None):
    if pk:
        poster = get_object_or_404(Poster, pk=pk)
        return redirect(poster.get_absolute_url(), permanent=True)
        
    poster = get_object_or_404(Poster, slug=slug)
    return render(request, 'venue/poster_detail.html', {'poster': poster})


def menu(request):
    return render(request, "venue/menu.html", {
        "packages": MenuPackage.objects.all(),
    })


def events(request):
    return render(request, "venue/events.html", {
        "formats": EventFormat.objects.all(),
        "halls": Hall.objects.filter(is_active=True),
    })


def gallery(request):
    # Фото галереи пока лежат в static/img. ПОДСКАЗКА: у картинок нет alt — проверьте шаблон!
    photos = [
        {"src": "img/hall-depo.jpg", "caption": "Зал «Депо»"},
        {"src": "img/hall-tonnel.webp", "caption": "Зал «Тоннель»"},
        {"src": "img/hall-platforma.jpg", "caption": "Зал «Платформа»"},
        {"src": "img/hall-vestibul.jpg", "caption": "Бар «Вестибюль»"},
    ]
    return render(request, "venue/gallery.html", {"photos": photos})


def contacts(request):
    return render(request, "venue/contacts.html")


def booking(request):
    # SEO-ВОПРОС: нужна ли эта страница в поисковой выдаче? Если нет — как её закрыть?
    # (meta robots noindex? Disallow в robots.txt? В чём разница?)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка принята! Перезвоним в течение 15 минут.")
            return redirect("venue:booking")
    else:
        form = BookingForm(initial={
            "hall": request.GET.get("hall"),
            "comment": request.GET.get("comment", ""),
            "guests": request.GET.get("guests"),
        })
    return render(request, "venue/booking.html", {"form": form})
