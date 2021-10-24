from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from core.rate_limiter import limiter
from models.books import Books
from decorators.token_required import token_required

books_blueprint = Blueprint('books_blueprint', __name__)

limiter.limit('10/minute')(books_blueprint)


@books_blueprint.route('/books', methods=['GET'])
def get_books():
    books = []
    for book in Books.objects():
        books.append(book.to_json())
    return jsonify(books)


@books_blueprint.route('/books', methods=['POST'])
@token_required
def add_book():
    name = request.form.get('name', None)
    author = request.form.get('author', None)
    category = request.form.get('category', None)

    if name is None:
        return jsonify({"message": "Name field is missing"}), 400
    if author is None:
        return jsonify({"message": "Author field is missing"}), 400
    if category is None:
        return jsonify({"message": "Category field is missing"}), 400

    book = Books(name=name, author=author)
    book.save()
    return jsonify({"message": 'Book added'})


@books_blueprint.route('/books/<book_id>', methods=['PUT'])
@token_required
def update_book(book_id):
    book = Books.objects(_id=ObjectId(book_id))
    updated_items = book.update(name=request.form['name'], author=request.form['author'])
    if updated_items == 1:
        return jsonify({"message": "Book updated"})
    else:
        return jsonify({"message": "Book not exist"}), 404


@books_blueprint.route('/books/<book_id>', methods=['DELETE'])
@token_required
def delete_book(book_id):
    book = Books.objects(_id=ObjectId(book_id))
    deleted_number = book.delete()
    if deleted_number > 0:
        return jsonify({"message": "Book deleted"})
    else:
        return jsonify({"message": "Book not exist"}), 404
