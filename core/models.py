from django.db import models
from datetime import datetime


class Todo(models.Model):
    """
    Classe para representar uma tarefa
    """
    name = models.CharField(max_length=100)  # Nome da tarefa, em tamanho reduzido
    content = models.TextField(null=True, blank=True)  # Conteudo da tarefa, é TextField para dar uma descrição maior
    done = models.BooleanField(default=False)  # Flag para tarefa concluida e não concluida
    created = models.DateTimeField(auto_now_add=True)  # Data de criação da tarefa
    changed = models.DateTimeField(auto_now_add=True)  # Data de alteração da tarefa
    ranking = models.IntegerField(unique=True)  # Posição da tarefa, para poder alterar a ordem das mesmas manualmente

    class Meta:
        verbose_name = 'TODO'
        verbose_name_plural = 'TODOs'
        ordering = ('-ranking', )

    def __str__(self):
        """Retornando o nome da tarefa"""
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Sobrescrevendo o metodo save para atualizar o campo changed e
        setar no campo ranking o valor inicial
        """
        self.changed = datetime.now()

        # Em caso de tarefa nova o valor de ranking será a quantidade + 1
        if not self.pk:
            self.ranking = self.__class__.objects.count() + 1  # Faço uso do __class__ pois o Manager não pode ser \
            #  acessado de dentro do objeto

        return super(Todo, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        """Sobrescrevendo metodo delete para atualizar o campo ranking"""
        old_ranking = self.ranking

        obj = super(Todo, self).delete(using, keep_parents)

        todos = self.__class__.objects.filter(ranking__gt=old_ranking).order_by('ranking')  # Filtrando por tarefas com ranking superior
        for todo in todos:  # Caso existam devo diminuir em 1 cada uma delas
            todo.ranking -= 1
            todo.save()

        return obj

