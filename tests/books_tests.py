from unittest import TestCase, main as unittest_main, mock
from main import app
from bson.objectid import ObjectId
from fixtures.book_fixtures import sample_books, sample_form_data


class BooksApiTest(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_wrong_endpoint(self):
        result = self.client.get('/booksy')
        self.assertEqual(result.status, '404 NOT FOUND')

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_book(self, mock_update):
        mock_update.return_value.matched_count = 1
        book_id = "612cd6ab534dfb8d738c5938"
        result = self.client.put('/books/' + book_id, data=sample_form_data)
        mock_update.assert_called_with({'_id': ObjectId(book_id)}, {'$set': sample_form_data})
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_book_404(self, mock_update):
        mock_update.return_value.matched_count = 0
        book_id = "612cd6ab534dfb8d738c5938"
        result = self.client.put('/books/' + book_id, data=sample_form_data)
        mock_update.assert_called_with({'_id': ObjectId(book_id)}, {'$set': sample_form_data})
        self.assertEqual(result.status, '404 NOT FOUND')

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_book_400(self, mock_update):
        mock_update.return_value.matched_count = 0
        book_id = "612cd6ab534dfb8d738c5938"
        result = self.client.put('/books/' + book_id)
        print(result.get_data(as_text=True))
        self.assertEqual(result.status, '400 BAD REQUEST')

    @mock.patch('pymongo.collection.Collection.find')
    def test_get_books(self, mock_find):
        mock_find.return_value = sample_books

        result = self.client.get('/books')
        self.assertEqual(result.status, '200 OK')
        page_content = result.get_json()
        self.assertListEqual(sample_books, page_content)

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_book(self, mock_delete):
        mock_delete.return_value.deleted_count = 1

        book_id = sample_books[0]["_id"]
        result = self.client.delete('/books/' + book_id)
        mock_delete.assert_called_with({'_id': ObjectId(book_id)})
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_book_404(self, mock_delete):
        mock_delete.return_value.deleted_count = 0
        books = sample_books.copy()
        book_id = books[0]["_id"]
        result = self.client.delete('/books/' + book_id)
        mock_delete.assert_called_with({'_id': ObjectId(book_id)})
        self.assertEqual(result.status, '404 NOT FOUND')


if __name__ == '__main__':
    unittest_main()