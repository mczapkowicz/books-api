from unittest import TestCase, main as unittest_main, mock
from create_app import create_app
from fixtures.book_fixtures import sample_form_data
from mongoengine import disconnect
from models.books import Books
from config import TestingConfig


class BooksApiTest(TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_wrong_endpoint(self):
        result = self.client.get('/booksy')
        self.assertEqual(result.status, '404 NOT FOUND')

    @mock.patch('jwt.decode')
    def test_update_book(self, mock_update):
        books = BooksApiTest.generate_books()
        mock_decode = "true"
        book_id = books[0]["_id"]
        result = self.client.put('/books/' + book_id, data=sample_form_data)
        self.assertEqual(result.status, '200 OK')

    @mock.patch('jwt.decode')
    def test_update_book_404(self, mock_update):
        mock_decode = "true"
        book_id = "612cd6ab534dfb8d738c5938"
        result = self.client.put('/books/' + book_id, data=sample_form_data)
        self.assertEqual(result.status, '404 NOT FOUND')

    @mock.patch('jwt.decode')
    def test_update_book_400(self, mock_update):
        books = BooksApiTest.generate_books()
        mock_decode = "true"
        book_id = "612cd6ab534dfb8d738c5938"
        result = self.client.put('/books/' + book_id)
        self.assertEqual(result.status, '400 BAD REQUEST')

    def test_get_books(self):
        books = BooksApiTest.generate_books()
        result = self.client.get('/books')
        self.assertEqual(result.status, '200 OK')
        page_content = result.get_json()
        self.assertListEqual(books, page_content)

    @mock.patch('jwt.decode')
    def test_delete_book(self, mock_decode):
        books = BooksApiTest.generate_books()
        mock_decode = "true"
        book_id = books[0]["_id"]
        result = self.client.delete('/books/' + book_id)
        self.assertEqual(result.status, '200 OK')

    @mock.patch('jwt.decode')
    def test_delete_book_404(self, mock_decode):
        BooksApiTest.generate_books()
        mock_decode = "true"
        book_id = "612cd6ab534dfb8d738c5938"
        result = self.client.delete('/books/' + book_id)
        self.assertEqual(result.status, '404 NOT FOUND')

    @staticmethod
    def generate_books():
        book1 = Books(name="Casino Royal", author="Ian Fleming")
        book1.save()
        books = []
        for book in Books.objects():
            books.append(book.to_json())
        return books


if __name__ == '__main__':
    unittest_main()