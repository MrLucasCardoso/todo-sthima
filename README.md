# TODO-STHIMA
Avaliação técnica para STHIMA

# Instalação

### Linux 
Apos clonar o repositório, deve criar uma virtualenv usando python 3.5+ e instalar os requirements do projeto:

```bash
$ pip install -r requirements.txt
```

Posteriormente, deve-se rodar a migrate

```bash
$ ./manage.py migrate
```

Para rodar os testes:

```bash
$ ./manage.py test
```

Para rodar a aplicação, simplesmente um runserver:

```bash
$ ./manage.py runserver
```

### Docker
Apos clonar o repositório:
```bash
$ docker-compose up -d
```

A aplicação irá rodar no http://localhost:8000/

# Utilização

O sistema e suas operações são feitas em uma unica pagina, no centro da pagina existe
um input com o placeholder "Adicione uma tarefa", para adicionar basta começar a digitar
e ao finalizar clicar no botão de mais(+) no canto direito do input.
- Para remover uma tarefa é só clicar no botão vermelho com uma lixeira;
- Para marcar como feita é só clicar no botão verdo com o "Ok";
- Para editar bascar clicar em cima do texto e digitar ;
- Para alterar a ordem das tarefas, passar o mouse no canto direito da tarefa que vai aparecer o nome "Arrastar"