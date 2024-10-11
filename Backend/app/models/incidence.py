# from app import db
# from sqlalchemy.sql import func
# import uuid

# class Incidence(db.Model):
#     id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     user_id = db.Column(db.String(80), db.ForeignKey('user.id'), nullable=False)
#     creation_date = db.Column(db.Date, default=func.current_date()) 
#     description = db.Column(db.String(128))