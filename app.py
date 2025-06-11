import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from

# Inicialização da aplicação Flask
app = Flask(__name__)

# Configuração do Swagger/Flasgger para documentação da API
app.config['SWAGGER'] = {
    'title': 'API CRUD DevOps',
    'uiversion': 3,
    "specs_route": "/swagger/" # Rota para acessar a documentação
}
swagger = Swagger(app)

# Configuração do Banco de Dados MySQL Server via SQLAlchemy
# A string de conexão será obtida de uma variável de ambiente (MYSQL_CONNECTION_STRING)
# Exemplo de Connection String para MySQL (formato SQLAlchemy):
# "mysql+pymysql://<user>:<password>@<host>:<port>/<database>"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MYSQL_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definição do modelo de dados para um Item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<Item {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        
# Criar as tabelas no banco de dados se não existirem
# Isso é útil para demonstrações, mas em produção, use ferramentas de migração (ex: Alembic)
with app.app_context():
    db.create_all()
    
# --- Rotas da API e Documentação Swagger ---

@app.route('/items', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'id': 'Item',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Nome do item',
                        'required': True
                    },
                    'description': {
                        'type': 'string',
                        'description': 'Descrição do item'
                    }
                }
            },
            'required': True
        }
    ],
    'responses': {
        201: {
            'description': 'Item criado com sucesso',
            'schema': {'$ref': '#/definitions/Item'}
        },
        400: {'description': 'Requisição inválida'}
    },
    'tags': ['Items']
})
def create_item():
    """
    Cria um novo item
    Retorna o item criado.
    ---
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Nome do item é obrigatório"}), 400
    if Item.query.filter_by(name=data['name']).first():
        return jsonify({"error": "Item com este nome já existe"}), 400

    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.serialize()), 201

@app.route('/items', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Lista de todos os itens',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/Item'}
            }
        }
    },
    'tags': ['Items']
})
def get_items():
    """
    Lista todos os itens
    Retorna uma lista de todos os itens.
    ---
    """
    items = Item.query.all()
    return jsonify([item.serialize() for item in items])

@app.route('/items/<int:item_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'item_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do item'
        }
    ],
    'responses': {
        200: {
            'description': 'Detalhes de um item específico',
            'schema': {'$ref': '#/definitions/Item'}
        },
        404: {'description': 'Item não encontrado'}
    },
    'tags': ['Items']
})
def get_item(item_id):
    """
    Obtém um item pelo ID
    Retorna os detalhes de um item específico.
    ---
    """
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item não encontrado"}), 404
    return jsonify(item.serialize())

@app.route('/items/<int:item_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'item_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do item a ser atualizado'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Novo nome do item'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'Nova descrição do item'
                    }
                }
            },
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Item atualizado com sucesso',
            'schema': {'$ref': '#/definitions/Item'}
        },
        404: {'description': 'Item não encontrado'},
        400: {'description': 'Requisição inválida'}
    },
    'tags': ['Items']
})
def update_item(item_id):
    """
    Atualiza um item existente
    Atualiza um item pelo ID.
    ---
    """
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item não encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado fornecido para atualização"}), 400

    if 'name' in data:
        # Verificar se o novo nome já existe em outro item
        existing_item = Item.query.filter(Item.name == data['name'], Item.id != item_id).first()
        if existing_item:
            return jsonify({"error": "Item com este nome já existe"}), 400
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']

    db.session.commit()
    return jsonify(item.serialize())

@app.route('/items/<int:item_id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'item_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do item a ser deletado'
        }
    ],
    'responses': {
        204: {'description': 'Item deletado com sucesso'},
        404: {'description': 'Item não encontrado'}
    },
    'tags': ['Items']
})
def delete_item(item_id):
    """
    Deleta um item
    Deleta um item pelo ID.
    ---
    """
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item não encontrado"}), 404

    db.session.delete(item)
    db.session.commit()
    return '', 204 # Retorna status 204 No Content para deleção bem-sucedida

if __name__ == '__main__':
    # Obtém a porta da variável de ambiente, padrão 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)