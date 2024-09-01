from flask import Flask, request, jsonify
from models.database import db
from models.dieta import Dieta

app = Flask(__name__)
app.config["SECRET_KEY"] = 'your_secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'

db.init_app(app)


@app.route("/adicionar", methods=["POST"])
def adicionar_refeicao():
    data = request.json
    nome = data.get("nome")
    descricao = data.get("descricao")
    data_hora = data.get("data_hora")
    dentro_da_dieta = data.get("dentro_da_dieta")

    if all([nome, descricao, data_hora, dentro_da_dieta is not None]):
        dieta = Dieta(nome=nome, descricao=descricao,
                      data_hora=data_hora, dentro_da_dieta=dentro_da_dieta)
        db.session.add(dieta)
        db.session.commit()
        return jsonify({"message": "refeição adicionada com sucesso"})
    else:
        return jsonify({"message": "informaçoes fornecidas invalidas"}), 404


@app.route("/ver_refeicao/<int:id>", methods=["GET"])
def ver_refeicao(id):
    dieta = Dieta.query.get(id)
    resultado = []

    if dieta:
        resultado.append({
            "nome": dieta.nome,
            "descricao": dieta.descricao,
            "data_hora": dieta.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "dentro_da_dieta": dieta.dentro_da_dieta})
        return jsonify(resultado)

    else:
        return jsonify({"message": "dieta não encontrada"}), 404


@app.route("/todas_refeicoes", methods=["GET"])
def todas_refeicoes():
    dietas = Dieta.query.all()
    resultado = []

    if not dietas:
        return jsonify({"message": "nenhuma dieta cadastrada"})

    for dieta in dietas:
        resultado.append({
            "id": dieta.id,
            "nome": dieta.nome,
            "descricao": dieta.descricao,
            "data_hora": dieta.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "dentro_da_dieta": dieta.dentro_da_dieta
        })
    return jsonify(resultado)


@app.route("/editar_refeicao/<int:id>", methods=["PUT"])
def atualizar_refeicao(id):
    data = request.json
    dieta = Dieta.query.get(id)

    if dieta:
        dieta.nome = data.get("nome")
        dieta.descricao = data.get("descricao")
        dieta.data_hora = data.get("data_hora")
        dieta.dentro_da_dieta = data.get("dentro_da_dieta")
        db.session.commit()
        return jsonify({"message": "refeição atualizada com sucesso"})
    return jsonify({"message": "refeição não encontrada"}), 404


@app.route("/deletar_refeicao/<int:id>", methods=["DELETE"])
def deletar_refeicao(id):
    dieta = Dieta.query.get(id)

    if dieta:
        db.session.delete(dieta)
        db.session.commit()
        return jsonify ({"message": f"refeição {id}, deletada com sucesso."})
    return jsonify ({"message": "refeição não encontrada"},404)


if __name__ == "__main__":
    app.run(debug=True)
