from django.test import TestCase
from django.shortcuts import reverse
from books.models import Book, BookReview
from users.models import User


class HomePageTestCase(TestCase):
    def test_reviews_all(self):
        book = Book.objects.create(title='title1', description='description1', isbn='11111')
        user = User.objects.create(username='farhod', email='farhod@gmail.com')
        user.set_password('Pass@123')
        user.save()
        review1 = BookReview.objects.create(author=user, book=book, comment='juda zor', stars_given=5)
        review2 = BookReview.objects.create(author=user, book=book, comment='yaxshi emas ekan', stars_given=2)
        review3 = BookReview.objects.create(author=user, book=book, comment='musur ekan tavsiya bermayman',
                                            stars_given=2)
        response = self.client.get(reverse('home') + "?page_size=2")
        self.assertNotContains(response, review1.comment)
        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        response = self.client.get("home" + "?page_size=2")
        self.assertContains(response, review1.comment)
