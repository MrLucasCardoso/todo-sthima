from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.core.serializers import serialize


class AjaxMixin(JSONResponseMixin, AjaxResponseMixin):
    success_status = 201

    def get_ajax(self, request, *args, **kwargs):
        return self.render_json_response({})

    def post_ajax(self, request, *args, **kwargs):
        # Verificando se é uma requisição com a pk do model
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            self.object = self.get_object()

        # Validando o form
        form = self.get_form()
        if form.is_valid():
            todo = form.save()
            json_string = serialize('json', [todo, ])[:-1][1:]  # removendo [] da string gerada
            return self.render_json_response(json_string, status=self.success_status)
        else:
            json_dict = {'errors': [(k, v[0].__str__()) for k, v in form.errors.items()]}  # gerando json de retorno \
            # com erros
            return self.render_json_response(json_dict, status=400)
