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


class TodoCreate(JSONResponseMixin, AjaxResponseMixin, CreateView):
    """View para cadastro de tarefas"""
    model = Todo
    fields = ('name', 'content')

    def get_ajax(self, request, *args, **kwargs):
        return self.render_json_response({})

    def post_ajax(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            todo = form.save()
            json_string = serialize('json', [todo, ])[:-1][1:]  # removendo [] da string gerada
            return self.render_json_response(json_string, status=201)
        else:
            json_dict = {'errors': [(k, v[0].__str__()) for k, v in form.errors.items()]}  # gerando json de retorno \
            # com erros
            return self.render_json_response(json_dict, status=400)


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
