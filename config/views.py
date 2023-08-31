from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import BookReview


def goodreads(request):
    return render(request, 'goodreads.html')


def home(request):
    reviews = BookReview.objects.order_by('-created_time')
    page_size = request.GET.get('page_size', 2)
    paginator = Paginator(reviews, page_size)  # Show 2 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    ctx = {
        'reviews': page_obj
    }
    return render(request, 'home.html', ctx)
