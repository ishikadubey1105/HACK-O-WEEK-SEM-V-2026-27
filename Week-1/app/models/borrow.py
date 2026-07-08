from datetime import date
from app.extensions import db


class BorrowRecord(db.Model):
    """Tracks which member borrowed which book and when."""

    __tablename__ = "borrow_records"

    id          = db.Column(db.Integer, primary_key=True)
    book_id     = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    member_id   = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    borrow_date = db.Column(db.Date, default=date.today)
    due_date    = db.Column(db.Date, nullable=False)           # 14 days from borrow date
    return_date = db.Column(db.Date, nullable=True)            # NULL = not yet returned
    is_returned = db.Column(db.Boolean, default=False)

    book   = db.relationship("Book",   back_populates="borrow_records")
    member = db.relationship("Member", back_populates="borrow_records")

    def to_dict(self):
        return {
            "id":          self.id,
            "book_id":     self.book_id,
            "book_title":  self.book.title if self.book else None,
            "member_id":   self.member_id,
            "member_name": self.member.name if self.member else None,
            "borrow_date": str(self.borrow_date),
            "due_date":    str(self.due_date),
            "return_date": str(self.return_date) if self.return_date else None,
            "is_returned": self.is_returned,
            "is_overdue":  (not self.is_returned) and (date.today() > self.due_date),
        }
