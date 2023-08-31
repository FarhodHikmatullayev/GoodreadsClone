from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import User


class BookReviewApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='farhod', email='farhod@gmail.com')
        self.user.set_password('Pass@123')
        self.user.save()
        self.client.login(username='farhod', password='Pass@123')

    def test_detail_book_review(self):
        book = Book.objects.create(title='title', description='description', isbn='123456')
        review = BookReview.objects.create(comment='comment', stars_given=4, author=self.user, book=book)
        response = self.client.get(
            reverse('api:review_detail', kwargs={'pk': review.id})
        )
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['comment'], 'comment')
        self.assertEqual(response.data['stars_given'], 4)
        self.assertEqual(response.data['author']['id'], 1)
        self.assertEqual(response.data['author']['username'], 'farhod')
        self.assertEqual(response.data['author']['email'], 'farhod@gmail.com')
        self.assertEqual(response.data['book']['id'], 1)
        self.assertEqual(response.data['book']['title'], 'title')
        self.assertEqual(response.data['book']['description'], 'description')
        self.assertEqual(response.data['book']['isbn'], '123456')

    def test_reviews_list(self):
        book = Book.objects.create(title='title', description='description', isbn='123456')
        BookReview.objects.create(author=self.user, book=book, comment='comment1', stars_given=5)
        BookReview.objects.create(author=self.user, book=book, comment='comment2', stars_given=4)

        response = self.client.get(
            reverse('api:review_list')
        )
        self.assertEqual(len(response.data['results']), 2)



