from src.app import db


class InvalidToken(db.Model):

    __tablename__ = "invalid_tokens"
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_invalid(cls, jti):
        """ Determine whether the jti key is on the blocklist return bool"""
        q = cls.query.filter_by(jti=jti).first()
        return bool(q)