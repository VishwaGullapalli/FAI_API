class User:
    def __init__(self, public_id, username, password, admin):
        self.public_id = public_id
        self.username = username
        self.password = password
        self.admin = admin

class Book:
    def __init__(self, title, author, isbn, price, quantity, issue_date=None, return_date=None, current_user=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.quantity = quantity
        self.max_quantity = quantity
        self.issue_date = issue_date
        self.return_date = return_date
        self.current_user = current_user