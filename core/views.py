from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView
from django.views.generic.edit import BaseUpdateView
from core.models import Todo
from django.core.serializers import serialize

from utils.mixins import AjaxMixin


class HomeView(TemplateView):
    """Home da aplicação"""
    template_name = 'index.html'


class TodoList(AjaxMixin, ListView):
    """View para listar todas as tarefas"""
    model = Todo

    def get_ajax(self, request, *args, **kwargs):
        return self.render_json_response({'todos': serialize('json', self.get_queryset())})


class TodoCreate(AjaxMixin, CreateView):
    """View para cadastro de tarefas"""
    model = Todo
    fields = ('name', 'content')


class TodoUpdate(AjaxMixin, UpdateView):
    """View para atualização de tarefa"""
    model = Todo
    success_status = 200
    fields = ('name', 'content')


class TodoDelete(AjaxMixin, DeleteView):
    """View para remover uma tarefa"""
    model = Todo


class TodoDone(AjaxMixin, BaseUpdateView):
    """View para listar a tarefa como feita"""
    model = Todo

    def post_ajax(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.done = True
        self.object.save()
        return self.render_json_response({})


class TodoUndone(BaseUpdateView):
    """View para listar a tarefa como desfeita"""
    pass


class TodoOrder(BaseUpdateView):
    """View para alterar ordenação das tarefas"""
    pass
