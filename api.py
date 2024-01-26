from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from models import User, Book

app = Flask(__name__)

app.config.from_pyfile('env.py')

mongo = PyMongo(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            current_user = mongo.db.users.find_one({'public_id': data['public_id']})
        except Exception as e:
            print(f"Exception decoding token: {e}")
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



# API Endpoints

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = {
        'public_id': str(uuid.uuid4()),
        'username': data['username'],
        'password': hashed_password,
        'admin': False
    }

    mongo.db.users.insert_one(new_user)

    return jsonify({'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = mongo.db.users.find_one({'username': data['username']})

    if not user or not check_password_hash(user['password'], data['password']):
        return make_response('Authentication failed!', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    token = jwt.encode({'public_id': user['public_id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                      app.config['SECRET_KEY'])

    return jsonify({'token': token})

@app.route('/books', methods=['GET'])
@token_required
def get_all_books(current_user):
    books = mongo.db.books.find()

    output = []

    for book in books:
        book_data = {
            'title': book['title'],
            'author': book['author'],
            'isbn': book['isbn'],
            'price': book['price'],
            'quantity': book['quantity']
        }
        output.append(book_data)

    return jsonify({'books': output})

@app.route('/books/<isbn>', methods=['GET'])
@token_required
def get_one_book(current_user, isbn):
    book = mongo.db.books.find_one({'isbn': isbn})

    if not book:
        return jsonify({'message': 'No book found!'})

    book_data = {
        'title': book['title'],
        'author': book['author'],
        'isbn': book['isbn'],
        'price': book['price'],
        'quantity': book['quantity']
    }

    return jsonify({'book': book_data})

@app.route('/books', methods=['POST'])
@token_required
def add_books(current_user):
    if not current_user['admin']:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format!'})

    new_books = []

    for book_data in data:
        new_book = {
            'title': book_data.get('title'),
            'author': book_data.get('author'),
            'isbn': book_data.get('isbn'),
            'price': book_data.get('price'),
            'quantity': book_data.get('quantity'),
            'max_quantity': book_data.get('quantity')
        }

        if any(value is None for value in new_book.values()):
            return jsonify({'message': 'Incomplete data for one or more books!'})

        new_books.append(new_book)

    mongo.db.books.insert_many(new_books)

    return jsonify({'message': 'New books added!'})


@app.route('/books/<isbn>', methods=['PUT'])
@token_required
def update_book(current_user, isbn):
    if not current_user['admin']:
        return jsonify({'message': 'Cannot perform that function!'})

    book = mongo.db.books.find_one({'isbn': isbn})

    if not book:
        return jsonify({'message': 'No book found!'})

    data = request.get_json()

    mongo.db.books.update_one(
        {'isbn': isbn},
        {
            '$set': {
                'title': data['title'],
                'author': data['author'],
                'price': data['price'],
                'quantity': data['quantity']
            }
        }
    )

    return jsonify({'message': 'Book details updated!'})

@app.route('/books/<isbn>', methods=['DELETE'])
@token_required
def delete_book(current_user, isbn):
    if not current_user['admin']:
        return jsonify({'message': 'Cannot perform that function!'})

    result = mongo.db.books.delete_one({'isbn': isbn})

    if result.deleted_count == 0:
        return jsonify({'message': 'No book found!'})

    return jsonify({'message': 'Book deleted!'})

# New API endpoints for book issuing and returning

@app.route('/books/issue/<isbn>', methods=['POST'])
@token_required
def issue_book(current_user, isbn):
    if not current_user['admin']:
        return jsonify({'message': 'Cannot perform that function!'})

    book = mongo.db.books.find_one({'isbn': isbn})

    if not book:
        return jsonify({'message': 'No book found!'})

    if book['quantity'] <= 0:
        return jsonify({'message': 'Book out of stock!'})

    data = request.get_json()

    book['quantity'] -= 1
    book['issue_date'] = datetime.datetime.utcnow()
    book['current_user'] = data.get('username')

    mongo.db.books.update_one({'isbn': isbn}, {'$set': book})

    return jsonify({'message': 'Book issued successfully!'})

@app.route('/books/return/<isbn>', methods=['POST'])
@token_required
def return_book(current_user, isbn):
    if not current_user['admin']:
        return jsonify({'message': 'Cannot perform that function!'})

    book = mongo.db.books.find_one({'isbn': isbn})

    if not book:
        return jsonify({'message': 'No book found!'})

    if book['quantity'] >= book['max_quantity']:
        return jsonify({'message': 'Cannot return more copies than available!'})

    book['quantity'] += 1
    book['return_date'] = datetime.datetime.utcnow()
    book['current_user'] = None

    mongo.db.books.update_one({'isbn': isbn}, {'$set': book})

    return jsonify({'message': 'Book returned successfully!'})

@app.route('/books/issued', methods=['GET'])
@token_required
def books_issued(current_user):
    books = mongo.db.books.find()

    output = []

    for book in books:
        if book['quantity'] < book['max_quantity']:
            book_data = {
                'title': book['title'],
                'author': book['author'],
                'isbn': book['isbn'],
                'price': book['price'],
                'quantity': book['quantity']
            }
        output.append(book_data)

    return jsonify({'books issued are': output})

if __name__ == '__main__':
    app.run(debug=True)
