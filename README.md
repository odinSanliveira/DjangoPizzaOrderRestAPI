# Pizza Order RestAPI
A REST API for pizza delivery service built for fun and practice with django framework.

## Instalação
#
* Instale o [python](https://www.python.org/downloads/).
* use o comando ```git clone https://github.com/odinSanliveira/DjangoPizzaOrderRestAPI``` em seu prompt de comando onde deseja baixar o repositório.
* Entre na pasta raíz e use o comando. ```virtualenv <nome-do-ambiente-virtual>```ou com ```pipenv``` para criar um ambiente virtual.
* Ative seu ambiente virtual com `<nome-do-ambiente-virtual>\Scripts\activate` .

* Instale os requisitos do ambiente com o comando: ```pip install -r requirements.txt```.
* cria sua base de dados ```python manage.py migrate```.
* crie um super user ``python manage.py createsuperuser``.
* Agora é só rodar a aplicação com ```python manage.py runserver```.


## Rotas disponíveis / Enabled Routes
#
Method | Funcionalidade | Rota | Access
|---|---|---|---|
|POST | Cadastrar novo usuário | /auth/signup | Todos|
|POST | Login de usuário | /auth/login | Todos|
|POST | _Refresh_ o token de acesso | auth/jwt/refresh/| Todo Usuário|
|POST | Verifica a validade do token | /auth/jwt/verify/ | Todo Usuário|
|POST | Realiza um pedido | /orders/ | Todo Usuário|
|GET  | retorna todos os pedidos | /orders/ | todos|
|GET  | retorna detalhes de pedido | /orders/{order_id} | super user|
|GET  | retorna detalhes de pedido de um usuário | /orders/user/{user_id}/order/{order_id}/ | todos|
|GET  | retorna pedidos de um usuário | /orders/user/{user_id}/orders/ | Todo Usuário|
|PUT  | Atualiza _status_ de pedido | /orders/update-status/{order_id} | Super User|
|PUT  | Atualiza pedido | /orders/{order_id}/ | Super User|
|PUT  | Atualiza username de usuário | /auth/update-username/{user_id} | Todo Usuário |
|DELETE  | Deleta pedido | /orders/{order_id}/ | Super User|
|GET | Documentação | /docs/ | Todos|


# Detalhes e funcionalidades
* Ao cadastrar pelo `auth/signup` um email será enviado para a ativação do usuário pelo endpoint `/auth/email-verification/`, caso não seja ativado o login não poderá ser efetuado.
* Se os usuário não for verificado ele não poderá ter acesso aos endpoints de verificação de Token.
* Será necessário usar o _Bearer Token_ no header da aplicação, já que algumas requisições precisam de autenticação e outras a permissão de _superuser_.
* Importante! o superuser deve está com o campo *is_verified* ativo, então acesse o endpoint `/admin` faça o login e ative esse campo.
* O django-seed pode ser usado para preencher o banco de dados com o comando `python manage.py seed (api_name) --number=15`.
