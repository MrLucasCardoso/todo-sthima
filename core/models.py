from django.db import models
from datetime import datetime


class Todo(models.Model):
    """
    Classe para representar uma tarefa
    """
    name = models.CharField(max_length=100)  # Nome da tarefa, em tamanho reduzido
    content = models.TextField(null=True)  # Conteudo da tarefa, é TextField para dar uma descrição maior da tarefa
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
        return super(Todo, self).save(force_insert, force_update, using, update_fields)
