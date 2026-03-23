from db import db

class Scenario(db.Model):
    __tablename__ = "scenarios"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    options = db.Column(db.JSON, nullable=False)
    results = db.Column(db.JSON, nullable=False)

    final_decision = db.Column(db.String(255), nullable=True)
    reflection = db.Column(db.Text, nullable=True)