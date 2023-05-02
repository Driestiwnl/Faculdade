from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'


db = SQLAlchemy(app)


class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)


@app.route('/registros', methods=['GET'])
def get_registros():
    registros = Registro.query.all()
    return jsonify([registro.__dict__ for registro in registros])


@app.route('/registros', methods=['POST'])
def post_registros():
    nome = request.args.get('nome')
    email = request.args.get('email')

    registro = Registro(nome=nome, email=email)
    db.session.add(registro)
    db.session.commit()

    return jsonify(registro.__dict__)


@app.route('/registros/<id>', methods=['DELETE'])
def delete_registro(id):
    registro = Registro.query.get(id)
    db.session.delete(registro)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)

