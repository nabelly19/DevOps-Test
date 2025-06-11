import unittest
import os
import sys

# Adiciona o diretório pai ao PYTHONPATH para que app.py possa ser importado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import app, db, Item

class BasicTests(unittest.TestCase):

    # Configuração inicial para cada teste
    def setUp(self):
        # Usar um banco de dados em memória para testes (SQLite)
        # para não depender do Azure SQL durante os testes unitários.
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    # Limpeza após cada teste
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Teste para criar um novo item
    def test_1_create_item(self):
        response = self.app.post('/items', json={'name': 'Test Item 1', 'description': 'Description for Test Item 1'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Item 1', response.get_data(as_text=True))

    # Teste para listar itens (após criação)
    def test_2_get_items(self):
        # Criar um item primeiro para garantir que a lista não esteja vazia
        self.app.post('/items', json={'name': 'Test Item 2', 'description': 'Description for Test Item 2'})
        response = self.app.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Item 2', response.get_data(as_text=True))

    # Teste para obter um item específico
    def test_3_get_single_item(self):
        # Criar um item para obter
        self.app.post('/items', json={'name': 'Test Item 3', 'description': 'Description for Test Item 3'})
        # Assumindo que o ID será 1 se for o primeiro item criado no teste
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Item 3', response.get_data(as_text=True))

    # Teste para obter um item que não existe
    def test_4_get_non_existent_item(self):
        response = self.app.get('/items/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Item não encontrado', response.get_data(as_text=True))

    # Teste para atualizar um item
    def test_5_update_item(self):
        self.app.post('/items', json={'name': 'Item to Update', 'description': 'Old description'})
        response = self.app.put('/items/1', json={'name': 'Updated Item', 'description': 'New description'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Item', response.get_data(as_text=True))
        self.assertIn('New description', response.get_data(as_text=True))

    # Teste para deletar um item
    def test_6_delete_item(self):
        self.app.post('/items', json={'name': 'Item to Delete', 'description': 'Description to delete'})
        response = self.app.delete('/items/1')
        self.assertEqual(response.status_code, 204) # No Content
        # Tentar obter o item deletado deve retornar 404
        response_get = self.app.get('/items/1')
        self.assertEqual(response_get.status_code, 404)


if __name__ == '__main__':
    unittest.main()