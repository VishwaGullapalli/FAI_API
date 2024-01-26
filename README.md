# Flask API Documentation

This documentation provides an overview of a Flask-based API for managing a library system. The API includes endpoints for user registration, authentication, book management, issuing, and returning books.

## Table of Contents

1. [Authentication](#authentication)
    1.1 [Token Required Decorator](#token-required-decorator)
  
2. [API Endpoints](#api-endpoints)
    2.1 [Register User](#register-user)
    2.2 [Login User](#login-user)
    2.3 [Get All Books](#get-all-books)
    2.4 [Get One Book](#get-one-book)
    2.5 [Add Books](#add-books)
    2.6 [Update Book](#update-book)
    2.7 [Delete Book](#delete-book)
    2.8 [Issue Book](#issue-book)
    2.9 [Return Book](#return-book)
    2.10 [Books Issued](#books-issued)

## 1. Authentication <a name="authentication"></a>

### 1.1 Token Required Decorator <a name="token-required-decorator"></a>

The `token_required` decorator is used to protect specific endpoints, ensuring that only authenticated users can access them. It extracts the token from the request headers and decodes it to identify the user based on the provided public ID.

```python
@token_required
def protected_endpoint(current_user):
    # Your protected endpoint logic here
```

## 2. API Endpoints <a name="api-endpoints"></a>

### 2.1 Register User <a name="register-user"></a>

#### Endpoint
```
POST /register
```

#### Request
- Method: `POST`
- Data: JSON
    ```json
    {
        "username": "example_user",
        "password": "password"
    }
    ```

#### Response
- Status: 200 OK
    ```json
    {
        "message": "User registered successfully!"
    }
    ```

### 2.2 Login User <a name="login-user"></a>

#### Endpoint
```
POST /login
```

#### Request
- Method: `POST`
- Data: JSON
    ```json
    {
        "username": "example_user",
        "password": "password"
    }
    ```

#### Response
- Status: 200 OK
    ```json
    {
        "token": "<JWT_TOKEN>"
    }
    ```

### 2.3 Get All Books <a name="get-all-books"></a>

#### Endpoint
```
GET /books
```

#### Request
- Method: `GET`
- Headers:
    - `x-access-token`: JWT token obtained during login

#### Response
- Status: 200 OK
    ```json
    {
        "books": [
            {
                "title": "Book Title",
                "author": "Author Name",
                "isbn": "ISBN",
                "price": 19.99,
                "quantity": 10
            },
            // ...
        ]
    }
    ```

### 2.4 Get One Book <a name="get-one-book"></a>

#### Endpoint
```
GET /books/<isbn>
```

#### Request
- Method: `GET`
- Headers:
    - `x-access-token`: JWT token obtained during login

#### Response
- Status: 200 OK
    ```json
    {
        "book": {
            "title": "Book Title",
            "author": "Author Name",
            "isbn": "ISBN",
            "price": 19.99,
            "quantity": 5
        }
    }
    ```

### 2.5 Add Books <a name="add-books"></a>

#### Endpoint
```
POST /books
```

#### Request
- Method: `POST`
- Headers:
    - `x-access-token`: JWT token obtained during login
- Data: JSON (List of Books)
    ```json
    [
        {
            "title": "Book Title",
            "author": "Author Name",
            "isbn": "ISBN",
            "price": 19.99,
            "quantity": 10
        },
        // ...
    ]
    ```

#### Response
- Status: 200 OK
    ```json
    {
        "message": "New books added!"
    }
    ```

### 2.6 Update Book <a name="update-book"></a>

#### Endpoint
```
PUT /books/<isbn>
```

#### Request
- Method: `PUT`
- Headers:
    - `x-access-token`: JWT token obtained during login
- Data: JSON
    ```json
    {
        "title": "New Book Title",
        "author": "New Author Name",
        "price": 24.99,
        "quantity": 8
    }
    ```

#### Response
- Status: 200 OK
    ```json
    {
        "message": "Book details updated!"
    }
    ```

### 2.7 Delete Book <a name="delete-book"></a>

#### Endpoint
```
DELETE /books/<isbn>
```

#### Request
- Method: `DELETE`
- Headers:
    - `x-access-token`: JWT token obtained during login

#### Response
- Status: 200 OK
    ```json
    {
        "message": "Book deleted!"
    }
    ```

### 2.8 Issue Book <a name="issue-book"></a>

#### Endpoint
```
POST /books/issue/<isbn>
```

#### Request
- Method: `POST`
- Headers:
    - `x-access-token`: JWT token obtained during login
- Data: JSON
    ```json
    {
        "username": "borrower_username"
    }
    ```

#### Response
- Status: 200 OK
    ```json
    {
        "message": "Book issued successfully!"
    }
    ```

### 2.9 Return Book <a name="return-book"></a>

#### Endpoint
```
POST /books/return/<isbn>
```

#### Request
- Method: `POST`
- Headers:
    - `x-access-token`: JWT token obtained during login

#### Response
- Status: 200 OK
    ```json
    {
        "message": "Book returned successfully!"
    }
    ```

### 2.10 Books Issued <a name="books-issued"></a>

#### Endpoint
```
GET /books/issued
```

#### Request
- Method: `GET`
- Headers:
    - `x-access-token`: JWT token obtained during login

#### Response
- Status: 200 OK
    ```json
    {
        "books_issued": [
            {
                "title": "Book Title",
                "author": "Author Name",
                "isbn": "ISBN",
                "price": 19.99,
                "quantity": 3
            },
            // ...
        ]
    }
    ```