from django.test import TestCase
from django.urls import reverse

from users.models import User
from .models import Book, BookReview, Author, BookAuthor


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(
            reverse('books:list')
        )
        self.assertContains(response, "No books found.")

    # def test_books_list(self):
    #     book1 = Book.objects.create(title='title1', description='description1', isbn='11111')
    #     book2 = Book.objects.create(title='title2', description='description2', isbn='22222')
    #     book3 = Book.objects.create(title='title3', description='description3', isbn='33333')
    #     book4 = Book.objects.create(title='title4', description='description4', isbn='44444')
    #
    #     response = self.client.get(
    #         reverse('books:list')
    #     )
    #     self.assertEqual(Book.objects.count(), 4)
    #     for book in [book1, book2]:
    #         self.assertContains(response, book.title)
    #
    #     response = self.client.get(
    #         reverse('books:list') + '?page=2&page_size=2'
    #     )
    #     self.assertEqual(Book.objects.count(), 4)
    #     books = Book.objects.all()
    #     for book in [book3, book4]:
    #         self.assertContains(response, book.title)

    def test_search_books(self):
        book1 = Book.objects.create(title='farhod', description='description1', isbn='11111')
        book2 = Book.objects.create(title='sherzod', description='description2', isbn='22222')

        response = self.client.get(
            reverse('books:list') + '?q=farhod'
        )
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)

        response = self.client.get(
            reverse('books:list') + '?q=sherzod'
        )
        self.assertNotContains(response, book1.title)
        self.assertContains(response, book2.title)

    def test_detail_books(self):
        book = Book.objects.create(title='title1', description='description1', isbn='11111')
        author1 = Author.objects.create(first_name='farhod', last_name='Hikmatullayev', email='farhod@gmail.com',
                                        bio='aaa')
        author2 = Author.objects.create(first_name='javlonbek', last_name='Jahongirov', email='javlonbek@gmail.com',
                                        bio='bbb')
        author3 = Author.objects.create(first_name='behruz', last_name='Negmurodov', email='behruz@gmail.com',
                                        bio='jjj')
        BookAuthor.objects.create(book=book, author=author1)
        BookAuthor.objects.create(book=book, author=author2)
        BookAuthor.objects.create(book=book, author=author3)
        response = self.client.get(
            reverse('books:detail', kwargs={'pk': book.id})
        )
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, book.isbn)
        self.assertContains(response, author1.full_name())
        self.assertContains(response, author2.full_name())
        self.assertContains(response, author3.full_name())


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='title1', description='description1', isbn='11111')
        user = User.objects.create(username='farhod', email='farhod@gmail.com')
        user.set_password('Pass@123')
        user.save()
        self.client.login(username='farhod', password='Pass@123')

        response = self.client.post(
            reverse('books:add_review', kwargs={'pk': book.id}),
            data={
                'comment': 'juda soz',
                'stars_given': 4
            }
        )
        reviews = BookReview.objects.all()
        self.assertEqual(response.url, reverse('books:detail', kwargs={'pk': book.id}))
        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews[0].stars_given, 4)
        self.assertEqual(reviews[0].comment, 'juda soz')
        self.assertEqual(reviews[0].author, user)
        self.assertEqual(reviews[0].book, book)

        response = self.client.post(
            reverse('books:add_review', kwargs={'pk': book.id}),
            data={
                'comment': 'juda soz',
                'stars_given': 6
            }
        )
        self.assertFormError(response, 'form', 'stars_given', 'Ensure this value is less than or equal to 5.')

    def test_delete_review(self):
        book = Book.objects.create(title='title1', description='description1', isbn='11111')
        user = User.objects.create(username='farhod', email='farhod@gmail.com')
        user.set_password('Pass@123')
        user.save()
        review = BookReview.objects.create(comment='comment', stars_given=4, author=user, book=book)
        self.client.login(username='farhod', password="Pass@123")

        response = self.client.get(
            reverse('books:delete_review', kwargs={'book_id': book.id, 'review_id': review.id}),
        )
        self.assertContains(response, book.title)
        self.assertContains(response, review.comment)

        response = self.client.post(
            reverse('books:delete_review', kwargs={'book_id': book.id, 'review_id': review.id}),
        )
        self.assertEqual(BookReview.objects.count(), 0)
        self.assertEqual(response.url, reverse('books:detail', kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, 302)

    def test_edit_review(self):
        book = Book.objects.create(title='title1', description='description1', isbn='11111')
        user = User.objects.create(username='farhod', email='farhod@gmail.com')
        user.set_password('Pass@123')
        user.save()
        review = BookReview.objects.create(comment='comment', stars_given=4, author=user, book=book)
        self.client.login(username='farhod', password="Pass@123")

        response = self.client.get(
            reverse('books:edit_review', kwargs={'book_id': book.id, 'review_id': review.id}),
        )
        self.assertContains(response, review.comment)
        self.assertContains(response, review.stars_given)

        response = self.client.post(
            reverse('books:edit_review', kwargs={'book_id': book.id, 'review_id': review.id}),
            data={
                'comment': "comment",
                'stars_given': 5
            }
        )
        review.refresh_from_db()
        self.assertEqual(review.comment, 'comment')
        self.assertEqual(review.stars_given, 5)
        self.assertEqual(response.url, reverse('books:detail', kwargs={'pk': book.id}))

        response = self.client.post(
            reverse('books:edit_review', kwargs={'book_id': book.id, 'review_id': review.id}),
            data={
                'comment': "comment",
            }
        )
        self.assertFormError(response, 'form', 'stars_given', 'This field is required.')

        response = self.client.post(
            reverse('books:edit_review', kwargs={'book_id': book.id, 'review_id': review.id}),
            data={
                'stars_given': 4,
            }
        )
        self.assertFormError(response, 'form', 'comment', 'This field is required.')
