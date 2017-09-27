from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView, View
from core.models import Todo
from django.core.serializers import serialize


class HomeView(TemplateView):
    """Home da aplicação"""
    template_name = 'index.html'


class TodoList(JSONResponseMixin, AjaxResponseMixin, ListView):
    """View para listar todas as tarefas"""
    model = Todo

    def get_ajax(self, request, *args, **kwargs):
        return self.render_json_response({'todos': serialize('json', self.get_queryset())})


class TodoCreate(CreateView):
    """View para cadastro de tarefas"""
    pass


class TodoUpdate(UpdateView):
    """View para atualização de tarefa"""
    pass


class TodoDelete(DeleteView):
    """View para remover uma tarefa"""
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
