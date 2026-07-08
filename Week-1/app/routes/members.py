from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.member import Member

members_bp = Blueprint("members", __name__, url_prefix="/api/members")


# ─────────────────────────────────────────────
#  GET /api/members  →  List all members
# ─────────────────────────────────────────────
@members_bp.route("/", methods=["GET"])
def get_all_members():
    """Return all registered library members."""
    members = Member.query.all()
    return jsonify({
        "success": True,
        "count":   len(members),
        "members": [m.to_dict() for m in members]
    }), 200


# ─────────────────────────────────────────────
#  POST /api/members  →  Register a new member
# ─────────────────────────────────────────────
@members_bp.route("/", methods=["POST"])
def add_member():
    """Register a new member. Required: name, email."""
    data = request.get_json()

    for field in ["name", "email"]:
        if not data or not data.get(field):
            return jsonify({"success": False, "error": f"'{field}' is required"}), 400

    # Prevent duplicate emails
    if Member.query.filter_by(email=data["email"]).first():
        return jsonify({"success": False, "error": "Email is already registered"}), 409

    new_member = Member(
        name    = data["name"],
        email   = data["email"],
        phone   = data.get("phone"),
        address = data.get("address"),
    )
    db.session.add(new_member)
    db.session.commit()

    return jsonify({"success": True, "message": "Member registered!", "member": new_member.to_dict()}), 201


# ─────────────────────────────────────────────
#  GET /api/members/<id>  →  Get one member
# ─────────────────────────────────────────────
@members_bp.route("/<int:member_id>", methods=["GET"])
def get_member(member_id):
    """Get a single member's details."""
    member = Member.query.get_or_404(member_id, description=f"No member found with id={member_id}")
    return jsonify({"success": True, "member": member.to_dict()}), 200


# ─────────────────────────────────────────────
#  PUT /api/members/<id>  →  Update a member
# ─────────────────────────────────────────────
@members_bp.route("/<int:member_id>", methods=["PUT"])
def update_member(member_id):
    """Update member details. Send only the fields you want to change."""
    member = Member.query.get_or_404(member_id, description=f"No member found with id={member_id}")
    data   = request.get_json()

    member.name    = data.get("name",    member.name)
    member.phone   = data.get("phone",   member.phone)
    member.address = data.get("address", member.address)

    db.session.commit()
    return jsonify({"success": True, "message": "Member updated!", "member": member.to_dict()}), 200


# ─────────────────────────────────────────────
#  DELETE /api/members/<id>  →  Remove a member
# ─────────────────────────────────────────────
@members_bp.route("/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    """Remove a member from the system."""
    member = Member.query.get_or_404(member_id, description=f"No member found with id={member_id}")
    db.session.delete(member)
    db.session.commit()
    return jsonify({"success": True, "message": f"Member '{member.name}' removed."}), 200
