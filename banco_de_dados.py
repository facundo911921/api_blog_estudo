# import sqlite3

# # conectando ao database ou, se não existir, criando e conectando
# with sqlite3.connect(r'database/data.db') as conexao:
#     # criando cursor
#     sql = conexao.cursor()
#     # criando database
#     sql.execute('create table bandas(nome text, estilo text, membros intereger);')

#     # inserindo dados
#     sql.execute('insert into bandas(nome, estilo, membros) values("Linkin Park", "Rock", 5)')

#     # inserindo dados dinâmicos
#     nome_banda, estilo_musical, quantidade_integrantes = 'Evanescense', 'Rock', 3

#     sql.execute('insert into bandas values(?,?,?)',[nome_banda, estilo_musical, quantidade_integrantes])

#     # buscando dados
#     dados = sql.execute('select * from bandas')
#     for dado in dados:
#         print(dado)

#     # salvando alterações
#     conexao.commit()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# criar uma API
app = Flask(__name__)

# criar uma instância do SqlAlchemy
app.config['SECRET_KEY'] = '234SDF#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # instanciando um db localmente

db = SQLAlchemy(app)
db: SQLAlchemy

# definir estrutura da tabela Postagem
# com as colunas id_postagem, titulo e autor
class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor'))

# definir estrutura da tabela Autor
class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem')


def inicializar_banco():
    with app.app_context():
        # executar comando para criar banco de dados
        db.drop_all()
        db.create_all()

        # criar usuário administrador
        autor = Autor(nome='Facundo', email='facundo@mail.com', senha='123456', admin=True)
        db.session.add(autor)
        db.session.commit()

if __name__ == '__main__':
    inicializar_banco()