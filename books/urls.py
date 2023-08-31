from django.urls import path

from books.views import BookListView, BookDetailView, AddReviewView, ReviewEditView, DeleteReviewView

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('detail/<int:pk>/  ', BookDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/add-review/', AddReviewView.as_view(), name='add_review'),
    path('review/<int:book_id>/<int:review_id>/edit/', ReviewEditView.as_view(), name='edit_review'),
    path('review/<int:book_id>/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete_review'),
]
