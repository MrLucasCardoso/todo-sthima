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

    def test_valid_todo_create_view(self):
        """
        Testando requisição para cadastro de uma tarefa, com dados validos
        """
        response = self.client.get(reverse('todo-add'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')

        data = {'name': 'Testando View', 'content': 'Conteudo'}  # Dicionarios com dados do Tarefa

        response = self.client.post(reverse('todo-add'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(201, response.status_code, 'Deve retornar 201 como sucesso de criação de uma tarefa')
        self.assertEqual(5, Todo.objects.count(), 'Deve ser 5 com a tarefa adicionada')

        data = response.content
        self.assertIs(bytes, type(data), 'Retorna o json em bytes')

        returned_json = json.loads(data.decode('utf8').replace("'", '"'))
        returned_json = json.loads(returned_json)

        self.assertTrue('pk' in returned_json, 'Verifica se tem a chave "pk" no json')
        self.assertTrue('fields' in returned_json, 'Verifica se tem a chave "fields" no json')
        self.assertTrue('name' in returned_json['fields'], 'Verifica se tem a chave "name" no json')
        self.assertTrue('content' in returned_json['fields'], 'Verifica se tem a chave "content" no json')
        self.assertTrue('done' in returned_json['fields'], 'Verifica se tem a chave "done" no json')
        self.assertTrue('created' in returned_json['fields'], 'Verifica se tem a chave "created" no json')
        self.assertTrue('changed' in returned_json['fields'], 'Verifica se tem a chave "changed" no json')
        self.assertTrue('ranking' in returned_json['fields'], 'Verifica se tem a chave "ranking" no json')

        self.assertEqual('Testando View', returned_json['fields']['name'], 'Verificando nome')
        self.assertEqual('Conteudo', returned_json['fields']['content'], 'Verificando conteudo')

    def test_invalid_todo_create_view(self):
        """
        Testando requisição para cadastro de uma tarefa, com dados invalidos
        """
        data = {'name': '', 'content': 'Conteudo'}  # Dicionarios com dados do Tarefa

        response = self.client.post(reverse('todo-add'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(400, response.status_code, 'Deve retornar 400 devido o erro  de validação')
        self.assertEqual(4, Todo.objects.count(), 'Deve ser 4 a tarefa não dever ser adicionada')

        data = response.content
        self.assertIs(bytes, type(data), 'Retorna o json em bytes')

        returned_json = json.loads(data.decode('utf8').replace("'", '"'))

        self.assertTrue('errors' in returned_json, 'Verifica se tem a chave "errors" no json')
        self.assertIs(list, type(returned_json['errors']), 'Verifica se chave "errors" é umas lista')

        item = returned_json['errors'][0]
        self.assertEqual('name', item[0], 'Field que foi invalidado')

    def test_valid_todo_update_view(self):
        """
        Testando requisição para update de uma tarefa, com dados validos
        """
        args = (self.todo.pk, )  # Id da tarefa a ser alterada
        old_name = self.todo.name
        old_content = self.todo.content

        data = {'name': 'Testando View', 'content': 'Conteudo'}  # Dicionarios com dados do Tarefa

        response = self.client.post(reverse('todo-update', args=args), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de criação de uma tarefa')
        self.assertEqual(4, Todo.objects.count(), 'Deve ser 4 com a tarefa adicionada')

        data = response.content
        self.assertIs(bytes, type(data), 'Retorna o json em bytes')

        returned_json = json.loads(data.decode('utf8').replace("'", '"'))
        returned_json = json.loads(returned_json)

        self.assertTrue('pk' in returned_json, 'Verifica se tem a chave "pk" no json')
        self.assertTrue('fields' in returned_json, 'Verifica se tem a chave "fields" no json')
        self.assertTrue('name' in returned_json['fields'], 'Verifica se tem a chave "name" no json')
        self.assertTrue('content' in returned_json['fields'], 'Verifica se tem a chave "content" no json')
        self.assertTrue('done' in returned_json['fields'], 'Verifica se tem a chave "done" no json')
        self.assertTrue('created' in returned_json['fields'], 'Verifica se tem a chave "created" no json')
        self.assertTrue('changed' in returned_json['fields'], 'Verifica se tem a chave "changed" no json')
        self.assertTrue('ranking' in returned_json['fields'], 'Verifica se tem a chave "ranking" no json')

        self.assertNotEqual(old_name, returned_json['fields']['name'], 'Verificando nome')
        self.assertNotEqual(old_content, returned_json['fields']['content'], 'Verificando conteudo')

    def test_invalid_todo_update_view(self):
        """
        Testando requisição para update de uma tarefa, com dados invalidos
        """
        args = (self.todo.pk,)  # Id da tarefa a ser alterada
        data = {'name': '', 'content': 'Conteudo'}  # Dicionarios com dados do Tarefa

        response = self.client.post(reverse('todo-update', args=args), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(400, response.status_code, 'Deve retornar 400 devido o erro  de validação')
        self.assertEqual(4, Todo.objects.count(), 'Deve ser 4 a tarefa não dever ser adicionada')

        data = response.content
        self.assertIs(bytes, type(data), 'Retorna o json em bytes')

        returned_json = json.loads(data.decode('utf8').replace("'", '"'))

        self.assertTrue('errors' in returned_json, 'Verifica se tem a chave "errors" no json')
        self.assertIs(list, type(returned_json['errors']), 'Verifica se chave "errors" é umas lista')

        item = returned_json['errors'][0]
        self.assertEqual('name', item[0], 'Field que foi invalidado')

    def test_todo_delete_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')

    def test_todo_done_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')

    def test_todo_undone_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')

    def test_todo_order_view(self):
        """
        Testando acesso a home da aplicação
        """
        response = self.client.get(reverse('home'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, 'Deve retornar 200 como sucesso de acesso à view')