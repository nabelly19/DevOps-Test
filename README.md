# Projeto DevOps - API CRUD com Python, Azure Database for MySQL e Swagger


## Visão Geral do Projeto


Este projeto tem como objetivo demonstrar a implementação de práticas DevOps, focando em versionamento, integração contínua (CI) e entrega contínua (CD), utilizando o Azure DevOps e recursos do Azure. A aplicação de exemplo é uma API RESTful simples para operações CRUD (Create, Read, Update, Delete) de "Items".


## Tecnologias Utilizadas


* Linguagem de Programação: Python
* Framework Web: Flask
* Banco de Dados: Azure Database for MySQL
* ORM: SQLAlchemy
* Driver MySQL: PyMySQL
* Documentação da API: Flasgger (Swagger/OpenAPI)
* Versionamento de Código: Git
* Plataforma DevOps: Azure DevOps
* Serviço de Deploy: Azure App Service


## Estrutura do Repositório


O repositório está organizado da seguinte forma:


DevOps/
├── app.py                  # Código fonte da API Flask
├── requirements.txt        # Dependências Python do projeto
├── test_app.py             # Testes unitários da API
├── azure-pipelines.yml     # Definição do pipeline CI/CD do Azure DevOps
└── README.md               # Este arquivo de documentação


## Configuração Local (Opcional, para desenvolvimento)


Para executar a API localmente:

1. **Pré-requisitos**:


> Python 3
> Cliente MySQL (opcional, para gerenciar o banco de dados)
  

2. **Clone o repositório**:

~~~text
git clone <URL_DO_SEU_REPOSITORIO>
cd DevOps
~~~


3. *Crie e ative um ambiente virtual (recomendado)*:
   
~~~text
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
~~~

4. *Instale as dependências*:

~~~text
pip install -r requirements.txt
~~~

5. *Configure a variável de ambiente para a conexão com o banco de dados*:
   
* IMPORTANTE: Para rodar localmente, você precisaria de um servidor MySQL local ou acesso a um Azure Database for MySQL.
* Defina a variável MYSQL_CONNECTION_STRING com sua string de conexão no formato SQLAlchemy. Exemplo:

~~~text
# No Windows (PowerShell):
$env:MYSQL_CONNECTION_STRING="mysql+pymysql://<usuario>:<senha>@<host_mysql>:<porta>/<nome_do_banco>"
# No macOS/Linux:
export MYSQL_CONNECTION_STRING="mysql+pymysql://<usuario>:<senha>@<host_mysql>:<porta>/<nome_do_banco>"
~~~

* Exemplo completo: 
~~~text
mysql+pymysql://adminuser:MyStrongP@ssw0rd!@myserver.mysql.database.azure.com:3306/mydatabase
~~~

6. *Execute a aplicação*:

~~~text
gunicorn --bind 0.0.0.0:$PORT app:app
# Ou para depuração local (não recomendado para produção):
# python app.py
~~~

A API estará disponível em http://localhost:5000. A documentação Swagger estará em http://localhost:5000/swagger/.

# Rotas da API

* POST /items: Cria um novo item.

* Corpo da requisição: { "name": "string", "description": "string" }

* GET /items: Lista todos os itens.

* GET /items/{item_id}: Obtém um item específico pelo ID.

* PUT /items/{item_id}: Atualiza um item existente.

* Corpo da requisição: { "name": "string", "description": "string" } (campos opcionais)

* DELETE /items/{item_id}: Deleta um item.

# Estratégia de Branches (Gitflow)
    O projeto segue a estratégia de branches Gitflow, com as seguintes branches principais:

* main: Representa o código de produção, sempre estável e pronto para deploy.

* develop: Branch de integração para novas funcionalidades. Todos os merges de branches de feature são feitos aqui.

* release: Criada a partir de develop para preparar uma nova versão. Nenhuma nova funcionalidade é adicionada, apenas bugs críticos são corrigidos.

### Fluxo de Trabalho de Branches
1. Novas funcionalidades são desenvolvidas em branches de feature (feature/<nome-da-feature>) criadas a partir de develop.

2. Correções de bugs são feitas em branches de hotfix (hotfix/<nome-do-bug>) criadas a partir de main.

3. Todas as alterações são submetidas via Pull Requests (PRs) com aprovação obrigatória.

## Pipeline CI/CD (azure-pipelines.yml)
O arquivo azure-pipelines.yml define o pipeline de Integração Contínua e Entrega Contínua, consistindo nos seguintes estágios:

* Build:

Instala as dependências Python.

Gera os artefatos de build (código empacotado).

* Test:

Executa os testes unitários definidos em test_app.py.

* Deploy:

Realiza o deploy automático da aplicação para os ambientes correspondentes no Azure App Service, com base na branch:

main: Deploy para o ambiente de Produção.

develop: Deploy para o ambiente de Desenvolvimento.

release: Deploy para o ambiente de Homologação/Teste de Release.

# Políticas de Branch na main
A branch main possui as seguintes políticas para garantir a estabilidade do código:

* Não permitir commits diretos: Todas as alterações devem vir através de Pull Requests.

* Aprovação obrigatória de pelo menos um revisor: Um PR deve ser aprovado por no mínimo um colega antes de poder ser mesclado na main.

# Demonstração e Desafios Individuais

Durante a avaliação, serão solicitadas demonstrações práticas de habilidades com Git e Azure DevOps, incluindo:

* Realizar um commit que intencionalmente "quebre" a build do pipeline.

* Realizar um commit que "corrija" a build após uma quebra.

* Criar e gerenciar Pull Requests para migração de código entre as branches develop → release → main.

# Links Úteis
* > Documentação do Azure DevOps

* > Documentação do Azure App Service

* > Documentação do Azure Database for MySQL

* > Gitflow Workflow