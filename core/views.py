from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView, View
from core.models import Todo


class HomeView(TemplateView):
    """Home da aplicação"""
    template_name = 'index.html'


class TodoCreate(CreateView):
    """View para cadastro de tarefas"""
    pass


class TodoUpdate(UpdateView):
    """View para atualização de tarefa"""
    pass


class TodoDelete(DeleteView):
    """View para remover uma tarefa"""
    pass


class TodoList(ListView):
    """View para listar todas as tarefas"""
    pass


class TodoDone(View):
    """View para listar a tarefa como feita"""
    pass


class TodoUndone(View):
    """View para listar a tarefa como desfeita"""
    pass


class TodoOrder(View):
    """View para alterar ordenação das tarefas"""
    pass
