from models.database import db


class Dieta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(80), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    dentro_da_dieta = db.Column(db.String(80), nullable=False)
