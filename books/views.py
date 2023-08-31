from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import ListView, DetailView

from books.forms import BookReviewForm
from books.models import Book, BookReview


# class BookListView(ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.order_by('-id')
#     context_object_name = 'books'
#     paginate_by = 2


class BookListView(View):
    def get(self, request):
        books = Book.objects.order_by('-id')
        search_books = request.GET.get('q', '')
        if search_books:
            books = books.filter(title__icontains=search_books)
        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)  # Show 2 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ctx = {
            'books': page_obj,
            'value': search_books
        }
        return render(request, 'books/list.html', ctx)


# class BookDetailView(DetailView):
#     template_name = 'books/detail.html'
#     model = Book
#     pk_url_kwarg = 'pk'
#     context_object_name = 'book'

class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        form = BookReviewForm()
        ctx = {
            'book': book,
            'form': form,
        }

        return render(request, 'books/detail.html', ctx)


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        form = BookReviewForm(
            data=request.POST
        )
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.book = book
            review.save()
            messages.success(request, f"Your comment was successfully accepted")
            return redirect(reverse(
                'books:detail', kwargs={'pk': book.id}
            ))
        return render(request, 'books/detail.html', {'form': form, 'book': book})


class ReviewEditView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = get_object_or_404(Book, id=book_id)
        review = book.reviews.get(id=review_id)
        form = BookReviewForm(instance=review)
        ctx = {
            'book': book,
            'review': review,
            'form': form,
        }
        return render(request, 'books/edit_review.html', ctx)

    def post(self, request, book_id, review_id):
        book = get_object_or_404(Book, id=book_id)
        review = book.reviews.get(id=review_id)
        form = BookReviewForm(instance=review, data=request.POST)
        ctx = {
            'book': book,
            'review': review,
            'form': form,
        }
        if form.is_valid():
            form.save()
            messages.success(request, f"Your review was successfully edited")
            return redirect(reverse('books:detail', kwargs={'pk': book_id}))
        else:
            return render(request, 'books/edit_review.html', ctx)


class DeleteReviewView(View):
    def get(self, request, book_id, review_id):
        book = get_object_or_404(Book, id=book_id)
        review = book.reviews.get(id=review_id)
        ctx = {
            'book': book,
            'review': review,
        }
        return render(request, 'books/delete_review.html', ctx)

    def post(self, request, book_id, review_id):
        review = get_object_or_404(BookReview, id=review_id)
        review.delete()
        messages.info(request, f"Your review was deleted")

        return redirect(reverse('books:detail', kwargs={'pk': book_id}))
