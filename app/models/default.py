from app.extensions import db

class Default_Model(db.Model):
    '''
    Default model
    '''
    __tablename__ = 'Default_Model'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    message = db.Column(db.Text)

    def __repr__(self):
        return f'Name: {self.name}, Date: {self.date}, Message: {self.message}'