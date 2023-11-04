# Anotações

Este arquivo contém todos os comandos a anotações feitas por mim sobre o curso.

## Comandos

```bash
django-admin startproject project .
```

↳ Inicia o projeto intitulado `project` no diretório `.` (atual).

```bash
python manage.py runserver
```

↳ Sobe o servidor localmente do Django em desenvolvimento.

## Arquivos

- `manage.py`: configura a variável de ambiente `DJANGO_SETTINGS_MODULE`, que aponta para `settings.py`. Tem quase a mesma função do comando `django-admin`; porém, este é mais usado quando o projeto vai ser iniciado.
- `settings.py`: armazena as configurações do projeto, diz ao Django como ele deve se comportar.
- `urls.py`: carrega as configurações de URL de cada aplicação.
- `asgi.py` e `wsgi.py`: são usados em produção, para fazer a ligação entre o Django e um servidor web externo.
