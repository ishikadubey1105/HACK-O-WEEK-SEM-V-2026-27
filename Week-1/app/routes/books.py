from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.book import Book

# Blueprint groups all /api/books routes together
books_bp = Blueprint("books", __name__, url_prefix="/api/books")


# ─────────────────────────────────────────────
#  GET /api/books  →  List all books
# ─────────────────────────────────────────────
@books_bp.route("/", methods=["GET"])
def get_all_books():
    """Return every book in the library."""
    books = Book.query.all()
    return jsonify({
        "success": True,
        "count":   len(books),
        "books":   [b.to_dict() for b in books]
    }), 200


# ─────────────────────────────────────────────
#  POST /api/books  →  Add a new book
# ─────────────────────────────────────────────
@books_bp.route("/", methods=["POST"])
def add_book():
    """Add a new book. Required fields: title, author, isbn."""
    data = request.get_json()

    # Validate required fields
    required = ["title", "author", "isbn"]
    for field in required:
        if not data or not data.get(field):
            return jsonify({"success": False, "error": f"'{field}' is required"}), 400

    # Check for duplicate ISBN
    if Book.query.filter_by(isbn=data["isbn"]).first():
        return jsonify({"success": False, "error": "A book with this ISBN already exists"}), 409

    copies = data.get("total_copies", 1)

    new_book = Book(
        title        = data["title"],
        author       = data["author"],
        isbn         = data["isbn"],
        genre        = data.get("genre", "General"),
        total_copies = copies,
        available    = copies,   # all copies available when first added
    )
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"success": True, "message": "Book added!", "book": new_book.to_dict()}), 201


# ─────────────────────────────────────────────
#  GET /api/books/<id>  →  Get one book
# ─────────────────────────────────────────────
@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Get details of a single book by its ID."""
    book = Book.query.get_or_404(book_id, description=f"No book found with id={book_id}")
    return jsonify({"success": True, "book": book.to_dict()}), 200


# ─────────────────────────────────────────────
#  PUT /api/books/<id>  →  Update a book
# ─────────────────────────────────────────────
@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """Update book info. Send only the fields you want to change."""
    book = Book.query.get_or_404(book_id, description=f"No book found with id={book_id}")
    data = request.get_json()

    book.title        = data.get("title",        book.title)
    book.author       = data.get("author",       book.author)
    book.genre        = data.get("genre",         book.genre)
    book.total_copies = data.get("total_copies", book.total_copies)
    book.available    = data.get("available",    book.available)

    db.session.commit()
    return jsonify({"success": True, "message": "Book updated!", "book": book.to_dict()}), 200


# ─────────────────────────────────────────────
#  DELETE /api/books/<id>  →  Remove a book
# ─────────────────────────────────────────────
@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """Delete a book from the library."""
    book = Book.query.get_or_404(book_id, description=f"No book found with id={book_id}")
    db.session.delete(book)
    db.session.commit()
    return jsonify({"success": True, "message": f"Book '{book.title}' deleted."}), 200
