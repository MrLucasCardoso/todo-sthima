from django.test import TestCase
from core.models import Todo
from model_mommy import mommy


class TestTodo(TestCase):
    """
    Classe de teste para operações com model Todo
    """

    def setUp(self):
        self.todo = mommy.make(Todo, _fill_optional=True)
        self.todos = mommy.make(Todo, _fill_optional=True, _quantity=3)

    def test_foo(self):
        self.assertTrue(True)

