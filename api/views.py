from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import BookReview
from .serializers import BookReviewSerializer


class BookReviewDetailApiView(APIView):
    def get(self, request, pk):
        review = get_object_or_404(BookReview.objects.all(), id=pk)
        serializer = BookReviewSerializer(instance=review)
        return Response(data=serializer.data, status=200)

    def put(self, request, pk):
        review = get_object_or_404(BookReview.objects.all(), id=pk)
        serializer = BookReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request, pk):
        review = get_object_or_404(BookReview.objects.all(), id=pk)
        serializer = BookReviewSerializer(instance=review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        review = get_object_or_404(BookReview.objects.all(), id=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookReviewsListApiView(APIView):

    def get(self, request):
        reviews = BookReview.objects.all()
        pagination = PageNumberPagination()
        page_obj = pagination.paginate_queryset(reviews, request)
        serializer = BookReviewSerializer(reviews, many=True)
        return pagination.get_paginated_response(data=serializer.data)

    def post(self, request):
        data = request.data
        serializer = BookReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
