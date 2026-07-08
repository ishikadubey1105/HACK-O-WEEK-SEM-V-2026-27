#  Library Management System — REST API

A clean and simple REST API built with **Flask** and **SQLite** for managing a library's books, members, and borrowing operations.

---

##  Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
python run.py
```

### 3. Open in browser
Visit **http://127.0.0.1:5000/** — you'll see a JSON map of all available endpoints.

---

## 📁 Project Structure

```
library-api/
├── app/
│   ├── __init__.py          # App factory (creates the Flask app)
│   ├── config.py            # Database and app configuration
│   ├── extensions.py        # Shared SQLAlchemy instance
│   ├── models/
│   │   ├── book.py          # Book table
│   │   ├── member.py        # Member table
│   │   └── borrow.py        # BorrowRecord table
│   └── routes/
│       ├── books.py         # /api/books  endpoints
│       ├── members.py       # /api/members endpoints
│       └── borrow.py        # /api/borrow  endpoints
├── run.py                   # Entry point → python run.py
├── requirements.txt         # Python packages
└── library.db               # SQLite database (auto-created on first run)
```

---

##  API Endpoints

###  Books

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/books/` | List all books |
| POST | `/api/books/` | Add a new book |
| GET | `/api/books/<id>` | Get a book by ID |
| PUT | `/api/books/<id>` | Update a book |
| DELETE | `/api/books/<id>` | Delete a book |

#### Add a Book — `POST /api/books/`
```json
{
    "title": "The Alchemist",
    "author": "Paulo Coelho",
    "isbn": "978-0062315007",
    "genre": "Fiction",
    "total_copies": 3
}
```

#### Sample Response
```json
{
    "success": true,
    "message": "Book added!",
    "book": {
        "id": 1,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "isbn": "978-0062315007",
        "genre": "Fiction",
        "total_copies": 3,
        "available": 3
    }
}
```

---

### 👤 Members

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/members/` | List all members |
| POST | `/api/members/` | Register a member |
| GET | `/api/members/<id>` | Get a member by ID |
| PUT | `/api/members/<id>` | Update a member |
| DELETE | `/api/members/<id>` | Remove a member |

#### Register a Member — `POST /api/members/`
```json
{
    "name": "Ishika Dubey",
    "email": "ishika@example.com",
    "phone": "9876543210",
    "address": "Delhi, India"
}
```

---

###  Borrow & Return

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/borrow/` | Borrow a book |
| POST | `/api/borrow/return` | Return a book |
| GET | `/api/borrow/active` | All currently borrowed books |
| GET | `/api/borrow/history` | Full borrow history |
| GET | `/api/borrow/overdue` | Overdue books |

#### Borrow a Book — `POST /api/borrow/`
```json
{
    "book_id": 1,
    "member_id": 1
}
```

#### Return a Book — `POST /api/borrow/return`
```json
{
    "record_id": 1
}
```

#### Sample Borrow Response
```json
{
    "success": true,
    "message": "'The Alchemist' borrowed by Ishika Dubey. Due by 2026-07-22.",
    "record": {
        "id": 1,
        "book_id": 1,
        "book_title": "The Alchemist",
        "member_id": 1,
        "member_name": "Ishika Dubey",
        "borrow_date": "2026-07-08",
        "due_date": "2026-07-22",
        "return_date": null,
        "is_returned": false,
        "is_overdue": false
    }
}
```

---

## 🛡️ Business Rules

- ✅ A book can only be borrowed if `available > 0`
- ✅ A member cannot borrow the same book twice (until returned)
- ✅ Loan period is **14 days** from borrow date
- ✅ `is_overdue` flag is automatically calculated
- ✅ Returning a book restores its availability count

---

## 🧪 Testing with curl

```bash
# Add a book
curl -X POST http://127.0.0.1:5000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Python Crash Course","author":"Eric Matthes","isbn":"978-1593279288"}'

# Register a member
curl -X POST http://127.0.0.1:5000/api/members/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'

# Borrow a book
curl -X POST http://127.0.0.1:5000/api/borrow/ \
  -H "Content-Type: application/json" \
  -d '{"book_id":1,"member_id":1}'

# Return a book
curl -X POST http://127.0.0.1:5000/api/borrow/return \
  -H "Content-Type: application/json" \
  -d '{"record_id":1}'
```

---

## 🗄️ Database

SQLite database (`library.db`) is auto-created in the project root when you first run `python run.py`. No setup needed!

---

## 👨‍💻 Built With

- [Flask](https://flask.palletsprojects.com/) — Web framework
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM
- [SQLite](https://www.sqlite.org/) — Database