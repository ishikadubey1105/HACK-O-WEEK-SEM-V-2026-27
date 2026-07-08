from app.extensions import db


class Member(db.Model):
    """Represents a registered library member."""

    __tablename__ = "members"

    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(100), nullable=False)
    email   = db.Column(db.String(120), unique=True, nullable=False)
    phone   = db.Column(db.String(15))
    address = db.Column(db.String(200))

    # One member can have many borrow records
    borrow_records = db.relationship("BorrowRecord", back_populates="member", lazy=True)

    def to_dict(self):
        return {
            "id":      self.id,
            "name":    self.name,
            "email":   self.email,
            "phone":   self.phone,
            "address": self.address,
        }
