#CONSULTANDO UMA API
# import requests
# from pprint import pprint

# nova_tarefa= {'completed': False,
#   'title': 'aprender APIs',
#   'userId': 10}

# concluida_tarefa= {'completed': True,
#   'title': 'aprender APIs',
#   'userId': 10}

# resultados_get = requests.get('https://jsonplaceholder.typicode.com/todos')

# resultados_get_id = requests.get('https://jsonplaceholder.typicode.com/todos/1')

# post_request = requests.post('https://jsonplaceholder.typicode.com/todos/', nova_tarefa)

# post_request = requests.put('https://jsonplaceholder.typicode.com/todos/10', concluida_tarefa)

# post_request = requests.delete('https://jsonplaceholder.typicode.com/todos/10')


# CRIANDO UMA API
# from flask import Flask, jsonify, request

# app = Flask(__name__)
# postagens = [
#     {
#         'título': 'postagem 1',
#         'autor': 'autor 1'
#     },
#     {
#         'título': 'postagem 2',
#         'autor': 'autor 2'
#     },
#     {
#         'título': 'postagem 3',
#         'autor': 'autor 3'
#     }
# ]

# catalogo = [
#     {
#         'título': 'titanic',
#         'autor': 'james camerom'
#     },
#     {
#         'título': 'pear harbor',
#         'autor': 'cara que explode coisas'
#     },
#     {
#         'título': 'osnejknvkje',
#         'autor': 'autor 3'
#     }
# ]

# # Rota padrão - GET http://localhost:5000
# @app.route('/')
# def obter_postagens():
#     return jsonify(postagens)

# @app.route('/catalogo')
# def obter_catalogo():
#     return jsonify(catalogo)

# @app.route('/postagens/<int:indice>', methods=['GET'])
# def obter_postagem_por_indice(indice):
#     return jsonify(postagens[indice])

# @app.route('/postagens', methods=['POST'])
# def criar_postagem():
#     post = request.get_json()
#     postagens.append(post)

#     return jsonify(postagens, 200)

# @app.route('/postagens/<int:indice>', methods=['PUT'])
# def atualizar_postagem(indice):
#     put = request.get_json()
#     postagens[indice].update(put)

#     return(jsonify(postagens), 200)

# @app.route('/postagens/<int:indice>', methods=['DELETE'])
# def excluir_postagem(indice):
#     try:
#         if postagens[indice] is not None:
#             postagem_deletada = postagens[indice]
#             del postagens[indice]

#             return jsonify(f'{postagem_deletada} excluída\n{postagens}')
#     except:
#         return jsonify(f'Não foi possível exluir a postagem com o índice {indice}')

# app.run(port=5000, host='localhost', debug=True)

'''
​DESAFIO API músicas 
### 1. Defnir o objetivo da API:
Iremos montar uma api de músicas, onde deverá ser possível, consultar todas canções disponíveis, consultar uma canção individual, editar canções existentes e também excluir músicas existentes.
### 2. Qual será o URL base da API?
Iremos utilizar o url base 'localhost'
### 3. Quais são os endpoints?
Disponibilize endpoints para consultar, editar, criar e excluir
### 4. Quais recursos serão disponibilizados pela API?
Informações sobre canções
### 5. Quais verbos http serão disponibilizados?
* GET
* POST
* PUT
* DELETE
### 6. Quais são os URLs completos para cada um?
* GET http://localhost:5000/cancoes
* GET http://localhost:5000/cancoes/1
* POST http://localhost:5000/cancoes
* PUT http://localhost:5000/cancoes/1
* DELETE http://localhost:5000/cancoes/1
### 7. Qual deve ser a estrutura de cada canção
 - lista de dicionários, que contem cancao e estilo
 '''

from flask import Flask, jsonify, request, make_response
from banco_de_dados import Autor, Postagem, app, db
import datetime
import json
import jwt
from functools import wraps

# get para todas as musicas disponiveis
# @app.route('/')
# def exibir_musicas():
#     return jsonify(songs, 200)

# # get para uma musica individual usando o indice
# @app.route('/songs/<int:indice>', methods=['GET'])
# def buscar_musica_por_indice(indice):
#     return jsonify(songs[indice], 200)

# # put para editar uma música existente
# @app.route('/songs/<int:indice>', methods=['PUT'])
# def atualizar_musica_por_indice(indice):
#     put = request.get_json()
#     songs[indice].update(put)

#     return jsonify(songs)

# # delete para exluir musica existente
# @app.route('/songs/<int:indice>', methods=['DELETE'])
# def excluir_musica(indice):
    # try:
    #     if songs[indice] is not None:
    #         dado_deletado = songs[indice]
    #         del songs[indice]

    #         return jsonify(f'''{dado_deletado} excluído com sucesso!
    #                        Dados restantes:
    #                        {songs}
    #                        ''', 200)
    # except:
    #     return jsonify(f'Não foi possível excluir o dado de índice {indice}', 401)
    

def token_obrigatorio(f):
    @wraps(f)
    def decoreted(*args, **kwargs):
        token = None
        # Verifica se o token foi enviado
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem': 'Token não incluído!'}, 401)
        # se há token, validar no db
        try:
            resultado = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'mensagem': 'Token inválido'}, 401)
        return f(autor, *args, **kwargs)
    return decoreted
     

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or auth.username or not auth.password:
        make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    

@app.route('/autores')
@token_obrigatorio
def exibir_autores(autor):
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        lista_de_autores.append(autor_atual)

    return jsonify({'autores': lista_de_autores})

@app.route('/autores/<int:id>', methods=['GET'])
@token_obrigatorio
def buscar_autor_por_indice(autor, id):
    autor = Autor.query.filter_by(id_autor=id).first()
    if not autor:
        return jsonify('Autor não encontrado')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email
    return jsonify({'autores': autor_atual})

@app.route('/autores', methods=['POST'])
@token_obrigatorio
def novo_autor(autor):
    novo_autor = request.get_json()
    autor = Autor(nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email'])
    db.session.add(autor)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário criado com sucesso'}, 200)

@app.route('/autores/<int:indice>', methods=['PUT'])
@token_obrigatorio
def atualizar_autor_por_indice(autor, indice):
    usuario_a_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=indice).first()
    if not autor:
        return jsonify({'mensagem': 'Não foi possível encontrar o id passado'})
    try:
            autor.nome = usuario_a_alterar['nome']
    except:
        pass
    try:
            autor.email = usuario_a_alterar['email']
    except:
        pass
    try:
            autor.senha = usuario_a_alterar['senha']
    except:
        pass
    db.session.commit()
    return jsonify({'mensagem': f'autor de id {indice} alterado com sucesso'}, 200)

# delete para exluir musica existente
@app.route('/autores/<int:indice>', methods=['DELETE'])
@token_obrigatorio
def excluir_autor(autor, indice):
    autor = Autor.query.filter_by(id_autor=indice).first()
    if not autor:
        return jsonify({'mensagem': 'autor não encontrado'})
    db.session.delete(autor)
    db.session.commit()

    return jsonify({'mensagem': f'Autor de id {indice} exluído com sucesso'}, 200)


app.run(port=5000, host='localhost', debug=True)