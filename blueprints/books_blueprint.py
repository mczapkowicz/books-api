from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from MongoManager import MongoManager
from utils.replace_id import replace_id

books_blueprint = Blueprint('books_blueprint', __name__)


@books_blueprint.route('/books', methods=['GET'])
def get_books():
    _items = MongoManager.getInstance().books.books.find()
    items = []
    for document in _items:
        items.append(replace_id(document))
    return jsonify(items)


@books_blueprint.route('/books', methods=['POST'])
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

    MongoManager.getInstance().books.books.insert_one({
        'name': name,
        'author': author,
        'category': category
    })
    return jsonify({"message": 'Book added'})


@books_blueprint.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    collection = MongoManager.getInstance().books.books
    result = collection.update_one({"_id": ObjectId(book_id)},
                                   {"$set": {
                                       'name': request.form['name'],
                                       'author': request.form['author'],
                                       'category': request.form['category']
                                   }})

    if result.matched_count == 1:
        return jsonify({"message": result.matched_count})
    else:
        return jsonify({"message": "Book not exist"}), 404


@books_blueprint.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = MongoManager.getInstance().books.books.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Book deleted"})
    else:
        return jsonify({"message": "Book not exist"}), 404
