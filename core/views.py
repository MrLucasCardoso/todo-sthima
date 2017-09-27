from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView, View
from django.views.generic.edit import BaseUpdateView

from core.enums import OrderType
from core.models import Todo
from django.core.serializers import serialize
import json
from utils.mixins import AjaxMixin


class HomeView(TemplateView):
    """Home da aplicação"""
    template_name = 'index.html'


class TodoList(AjaxMixin, ListView):
    """View para listar todas as tarefas"""
    model = Todo
    ordering = 'ranking'

    def get_ajax(self, request, *args, **kwargs):
        return self.render_json_response({'todos': json.loads(serialize('json', self.get_queryset()))})


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


class TodoUndone(AjaxMixin, BaseUpdateView):
    """View para listar a tarefa como desfeita"""
    model = Todo

    def post_ajax(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.done = False
        self.object.save()
        return self.render_json_response({})


class TodoOrder(AjaxMixin, View):
    """View para alterar ordenação das tarefas"""

    def post_ajax(self, request, *args, **kwargs):
        order_type = int(request.POST.get('order_type', -1))
        kwargs['data'] = request.POST.dict()

        if order_type == -1:
            return self.render_json_response({}, status=400)

        # Despachando para o metodo referente ao tipo de ordenação
        for value, name in OrderType.choices():
            if order_type == value:
                handler = getattr(self, 'order_{0}'.format(name.lower()))
                return handler(request, *args, **kwargs)

        return self.render_json_response({}, status=400)

    def order_unit(self, request, *args, **kwargs):
        data = kwargs['data']
        todo = Todo.objects.get(pk=data['pk'])
        ranking = int(data['ranking'])

        if ranking > todo.ranking:  # se a nova posição for maior que a atual
            todos = Todo.objects.exclude(pk=data['pk']).filter(ranking__lte=ranking).order_by(
                'ranking'
            )  # Inferior ou igual al atual

            for _ in todos:  # Caso existam devo diminuir em 1 cada uma delas
                print(_.ranking)
                _.ranking -= 1
                _.save()

            todo.ranking = ranking
            todo.save()

        elif ranking < todo.ranking:  # se a nova posição for menor que a atual
            old_ranking = todo.ranking
            todos = Todo.objects.exclude(pk=data['pk']).filter(ranking__gte=ranking, ranking__lt=old_ranking).order_by(
                '-ranking'
            )  # Inferior ou igual al atual

            for _ in todos:  # Caso existam devo diminuir em 1 cada uma delas
                _.ranking += 1
                _.save()

            todo.ranking = ranking
            todo.save()

        return self.render_json_response({}, status=200)