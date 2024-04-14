# Projeto Integrador I

Projeto Integrador I - Grupo 005 - UNIVESP

Tema: Desenvolvimento de um software com framework web que utilize noções de banco de dados, praticando controle de versão.

## Índice

<!--ts-->
  * [Requisitos iniciais](#Requisitos-iniciais)
  * [Ambiente de desenvolvimento](#Ambiente-de-desenvolvimento)
<!--te-->

### Requisitos iniciais

- Baixe o VS Code: https://code.visualstudio.com/download
- Baixe o git: https://git-scm.com/downloads
- Baixe o Python: https://www.python.org/downloads/


### Ambiente de desenvolvimento

Faça o clone deste repositório via https ou ssh. Abra o terminal em qualquer pasta que queira manter o projeto e digite: 
- ```https://github.com/projeto-pi-2024/controle-de-estoque.git``` para clone via https
- ```git@github.com:projeto-pi-2024/controle-de-estoque.git``` para clone via ssh

Com o projeto em sua máquina, crie um ambiente virtual na raiz
```
python -m venv venv
. venv/Scrpits/activate
```

Caso o ambiente virtual não seja iniciado no Windows, abra o PowerShell como administrador e execute o comando
```
Set-ExecutionPolicy AllSigned -Force
```

Instale todas as dependências do arquivo ```requirements.txt```
```
pip install -r requirements.txt
```

Faça as migrações necessárias para a base de dados do Django
```
python manage.py makemigrations
python manage.py migrate
```

Crie o superuser do Django
```
python manage.py createsuperuser
```

Rode o servidor do Django
```
python manage.py runserver 
```

Acesse a URL ```http://localhost:8000/admin/``` e faça o login com seu superuser
