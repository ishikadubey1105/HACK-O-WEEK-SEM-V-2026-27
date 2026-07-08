from datetime import date, timedelta
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.book import Book
from app.models.member import Member
from app.models.borrow import BorrowRecord

borrow_bp = Blueprint("borrow", __name__, url_prefix="/api/borrow")

BORROW_DAYS = 14  # default loan period


# ─────────────────────────────────────────────
#  POST /api/borrow  →  Borrow a book
# ─────────────────────────────────────────────
@borrow_bp.route("/", methods=["POST"])
def borrow_book():
    """
    Borrow a book for a member.
    Required JSON body: { "book_id": 1, "member_id": 2 }
    """
    data = request.get_json()

    book_id   = data.get("book_id")
    member_id = data.get("member_id")

    if not book_id or not member_id:
        return jsonify({"success": False, "error": "'book_id' and 'member_id' are required"}), 400

    # Make sure book and member actually exist
    book   = Book.query.get_or_404(book_id,   description=f"No book found with id={book_id}")
    member = Member.query.get_or_404(member_id, description=f"No member found with id={member_id}")

    # Check if any copy is available
    if book.available < 1:
        return jsonify({"success": False, "error": f"'{book.title}' is currently unavailable"}), 400

    # Check if this member already has this book
    already_borrowed = BorrowRecord.query.filter_by(
        book_id=book_id, member_id=member_id, is_returned=False
    ).first()
    if already_borrowed:
        return jsonify({"success": False, "error": "Member already has this book checked out"}), 400

    # Create the borrow record
    record = BorrowRecord(
        book_id     = book_id,
        member_id   = member_id,
        borrow_date = date.today(),
        due_date    = date.today() + timedelta(days=BORROW_DAYS),
    )

    # Reduce available count by 1
    book.available -= 1

    db.session.add(record)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"'{book.title}' borrowed by {member.name}. Due by {record.due_date}.",
        "record":  record.to_dict()
    }), 201


# ─────────────────────────────────────────────
#  POST /api/borrow/return  →  Return a book
# ─────────────────────────────────────────────
@borrow_bp.route("/return", methods=["POST"])
def return_book():
    """
    Return a borrowed book.
    Required JSON body: { "record_id": 3 }
    """
    data      = request.get_json()
    record_id = data.get("record_id")

    if not record_id:
        return jsonify({"success": False, "error": "'record_id' is required"}), 400

    record = BorrowRecord.query.get_or_404(record_id, description=f"No borrow record with id={record_id}")

    if record.is_returned:
        return jsonify({"success": False, "error": "This book was already returned"}), 400

    # Mark as returned and restore availability
    record.is_returned = True
    record.return_date = date.today()
    record.book.available += 1

    db.session.commit()

    was_overdue = date.today() > record.due_date
    msg = "Book returned successfully!"
    if was_overdue:
        msg += " ⚠️  Note: This book was overdue."

    return jsonify({"success": True, "message": msg, "record": record.to_dict()}), 200


# ─────────────────────────────────────────────
#  GET /api/borrow/active  →  All active borrows
# ─────────────────────────────────────────────
@borrow_bp.route("/active", methods=["GET"])
def active_borrows():
    """List all books that are currently checked out (not returned)."""
    records = BorrowRecord.query.filter_by(is_returned=False).all()
    return jsonify({
        "success": True,
        "count":   len(records),
        "active":  [r.to_dict() for r in records]
    }), 200


# ─────────────────────────────────────────────
#  GET /api/borrow/history  →  Full borrow history
# ─────────────────────────────────────────────
@borrow_bp.route("/history", methods=["GET"])
def borrow_history():
    """Get the complete borrow history (all records, returned or not)."""
    records = BorrowRecord.query.order_by(BorrowRecord.borrow_date.desc()).all()
    return jsonify({
        "success": True,
        "count":   len(records),
        "history": [r.to_dict() for r in records]
    }), 200


# ─────────────────────────────────────────────
#  GET /api/borrow/overdue  →  Overdue books
# ─────────────────────────────────────────────
@borrow_bp.route("/overdue", methods=["GET"])
def overdue_books():
    """List all borrow records that are past their due date and not yet returned."""
    today   = date.today()
    records = BorrowRecord.query.filter(
        BorrowRecord.is_returned == False,
        BorrowRecord.due_date < today
    ).all()
    return jsonify({
        "success": True,
        "count":   len(records),
        "overdue": [r.to_dict() for r in records]
    }), 200
