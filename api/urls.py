from django.urls import path

from api.views import BookReviewDetailApiView, BookReviewsListApiView

app_name = 'api'

urlpatterns = [
    path('reviews/<int:pk>/', BookReviewDetailApiView.as_view(), name='review_detail'),
    path('reviews/', BookReviewsListApiView.as_view(), name='review_list'),
]
