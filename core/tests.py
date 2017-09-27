from django.test import TestCase, Client

from core.models import Todo
from model_mommy import mommy
from django.core.urlresolvers import reverse
import json


class TestTodo(TestCase):
    """
    Classe de teste para operações com model Todo
    """

    def setUp(self):
        self.todo = mommy.make(Todo, _fill_optional=True)  # Tarefa criada para testes
        self.todos = mommy.make(Todo, _fill_optional=True, _quantity=3)  # Lista com 3 tarefas para testes
        self.client = Client()  # Cliente para testar as requisições nas views

    def test_home_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')

    def test_todo_list_view(self):
        """
        Testando requisição de listagem de tarefas
        """
        response = self.client.get(reverse('todo-list'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')
        data = response.content
        self.assertIs(bytes, type(data), 'Retorna o json em bytes')

        returned_json = data.decode('utf8').replace("'", '"')
        returned_json = json.loads(returned_json)
        returned_json['todos'] = json.loads(returned_json['todos'])

        self.assertEqual(4, len(returned_json['todos']), 'quantidades de tarefas criadas')

        item = returned_json['todos'][0]

        self.assertTrue('pk' in item, 'Verifica se tem a chave "pk" no json')
        self.assertTrue('fields' in item, 'Verifica se tem a chave "fields" no json')
        self.assertTrue('name' in item['fields'], 'Verifica se tem a chave "name" no json')
        self.assertTrue('content' in item['fields'], 'Verifica se tem a chave "content" no json')
        self.assertTrue('done' in item['fields'], 'Verifica se tem a chave "done" no json')
        self.assertTrue('created' in item['fields'], 'Verifica se tem a chave "created" no json')
        self.assertTrue('changed' in item['fields'], 'Verifica se tem a chave "changed" no json')
        self.assertTrue('ranking' in item['fields'], 'Verifica se tem a chave "ranking" no json')

    def test_todo_create_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')

    def test_todo_update_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')

    def test_todo_delete_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')

    def test_todo_done_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')

    def test_todo_undone_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')

    def test_todo_order_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')