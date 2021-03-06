from django.test import TestCase, Client

from core.enums import OrderType
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
        self.assertEqual(4, Todo.objects.count(), 'Deve ser 4 com a tarefa alterada')

        data = response.content
        self.assertIs(bytes, type(data), 'Retorna o json em bytes')

        returned_json = json.loads(data.decode('utf8').replace("'", '"'))

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
        Testando remoção de uma tarefa
        """
        args = (self.todo.pk,)  # Id da tarefa a ser alterada
        response = self.client.delete(reverse('todo-delete', args=args), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de criação de uma tarefa')
        self.assertEqual(3, Todo.objects.count(), 'Deve ser 3 com a tarefa removida')

        # Deve levantar esta exceção pois a tarefa desve estar removida
        with self.assertRaisesMessage(Todo.DoesNotExist, "Todo matching query does not exist"):
            Todo.objects.get(id=args[0])

    def test_todo_done_view(self):
        """
        Testando definir tarefa como feita(done=True)
        """
        args = (self.todo.pk,)  # Id da tarefa a ser alterada

        # Salvando todo para conferencia
        self.todo = Todo.objects.get(pk=args[0])
        self.todo.done = False
        self.todo.save()

        response = self.client.post(reverse('todo-done', args=args), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')

        todo = Todo.objects.get(pk=args[0])

        self.assertTrue(todo.done, 'Tarefa deve estar marcada como feita(done)')
        self.assertNotEqual(self.todo.done, todo.done, 'Devem ser diferentes')

    def test_todo_undone_view(self):
        """
        Testando definir tarefa como desfeita(done=False)
        """
        args = (self.todo.pk,)  # Id da tarefa a ser alterada

        # Salvando todo para conferencia
        self.todo = Todo.objects.get(pk=args[0])
        self.todo.done = True
        self.todo.save()

        response = self.client.post(reverse('todo-undone', args=args), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')

        todo = Todo.objects.get(pk=args[0])

        self.assertFalse(todo.done, 'Tarefa deve estar marcada como feita(done)')
        self.assertNotEqual(self.todo.done, todo.done, 'Devem ser diferentes')

    def test_todo_unit_order_view(self):
        """
        Testando altareção de ordem das tarefas por unidade
        campo ranking iniciando com 1
        """
        # Testando de uma posição menor para maior
        data = {'order_type': OrderType.UNIT.value, 'pk': self.todo.pk, 'ranking': 3}
        response = self.client.post(reverse('todo-order'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')

        todo = Todo.objects.get(pk=self.todo.pk)

        self.assertEqual(3, todo.ranking, 'Ranking de ser atualizado para 3')
        self.assertNotEqual(self.todo.ranking, todo.ranking, 'Ranking deve ser diferente do anterior')
        self.assertEqual(Todo.objects.all().order_by('ranking')[2].pk, todo.pk, 'Deve ser a mesma tarefa na terceira posição')

        # Testando de uma posição maior para menor
        data = {'order_type': OrderType.UNIT.value, 'pk': todo.pk, 'ranking': 1}
        response = self.client.post(reverse('todo-order'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')

        _todo = Todo.objects.get(pk=self.todo.pk)

        self.assertEqual(1, _todo.ranking, 'Ranking de ser atualizado para 1')
        self.assertNotEqual(todo.ranking, _todo.ranking, 'Ranking deve ser diferente do anterior')
        self.assertEqual(Todo.objects.all().order_by('ranking')[0].pk, _todo.pk, 'Deve ser a mesma tarefa na primeira posição')

    # def test_todo_name_order_view(self):
    #     """
    #     Testando altareção de ordem das tarefas por campo nome
    #     """
    #     response = self.client.post(reverse('todo-order'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')
    #
    # def test_todo_created_order_view(self):
    #     """
    #     Testando altareção de ordem das tarefas por data de criação
    #     """
    #     response = self.client.post(reverse('todo-order'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')
    #
    # def test_todo_changed_order_view(self):
    #     """
    #     Testando altareção de ordem das tarefas por data de alteração
    #     """
    #     response = self.client.post(reverse('todo-order'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')
    #
    # def test_todo_done_order_view(self):
    #     """
    #     Testando altareção de ordem das tarefas por tarefas feitas
    #     """
    #     response = self.client.post(reverse('todo-order'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     self.assertEqual(200, response.status_code, 'Deve retornar 200 como sucesso de acesso à view')