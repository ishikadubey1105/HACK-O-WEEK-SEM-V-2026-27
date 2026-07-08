from app.extensions import db


class Book(db.Model):
    """Represents a book available in the library."""

    __tablename__ = "books"

    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(200), nullable=False)
    author        = db.Column(db.String(100), nullable=False)
    isbn          = db.Column(db.String(20), unique=True, nullable=False)
    genre         = db.Column(db.String(50), default="General")
    total_copies  = db.Column(db.Integer, default=1)          # how many copies exist
    available     = db.Column(db.Integer, default=1)          # copies currently on shelf

    # One book can have many borrow records
    borrow_records = db.relationship("BorrowRecord", back_populates="book", lazy=True)

    def to_dict(self):
        return {
            "id":           self.id,
            "title":        self.title,
            "author":       self.author,
            "isbn":         self.isbn,
            "genre":        self.genre,
            "total_copies": self.total_copies,
            "available":    self.available,
        }
