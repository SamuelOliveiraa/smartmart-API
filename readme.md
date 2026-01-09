# SmartMart API

Esta API foi desenvolvida como um teste prático para o processo seletivo de estágio em desenvolvimento full-stack da **APOLLO SOLUTIONS**. O objetivo é fornecer um conjunto de endpoints para gerenciar produtos, categorias e vendas de um sistema de varejo fictício, o SmartMart.

## 📝 Sobre o Projeto

A smartmart API é um serviço RESTful construído em Python que oferece funcionalidades de CRUD para as principais entidades de um sistema de vendas. Além das operações básicas, a API também inclui rotas para importação e exportação de dados em massa via arquivos CSV, facilitando a integração e a gestão de dados.

A aplicação utiliza uma arquitetura limpa e modular, separando a lógica de negócios, o acesso ao banco de dados e a definição dos endpoints, o que a torna escalável e de fácil manutenção.

## 💻 Tecnologias Utilizadas

O projeto foi construído com as seguintes tecnologias:

- **Python 3.12:** Linguagem de programação principal.
- **FastAPI:** Framework web de alta performance para a construção de APIs.
- **SQLAlchemy:** ORM (Object-Relational Mapper) para interação com o banco de dados SQL.
- **Uvicorn:** Servidor ASGI (Asynchronous Server Gateway Interface) para rodar a aplicação FastAPI.
- **Pydantic:** Para validação e serialização de dados.
- **SQLite:** Banco de dados relacional leve, utilizado para o desenvolvimento e armazenamento local.
- **Pandas:** Utilizado para manipulação de dados, especialmente nas operações de importação/exportação.
- **Vercel:** Configurada para deploy simplificado da API em ambiente serverless.

## 📂 Estrutura do Projeto

O código-fonte está organizado da seguinte forma:

```
├── api/
│   └── index.py         # Ponto de entrada para o deploy na Vercel
├── app/
│   ├── crud.py          # Funções de acesso e manipulação de dados (CRUD)
│   ├── database.py      # Configuração da conexão com o banco de dados
│   ├── main.py          # Ponto de entrada principal da aplicação FastAPI
│   ├── models.py        # Definição dos modelos de tabela do SQLAlchemy
│   ├── routers.py       # Definição dos endpoints (rotas) da API
│   └── schemas.py       # Definição dos schemas Pydantic para validação de dados
├── requirements.txt     # Lista de dependências Python
├── vercel.json          # Configuração de deploy para a Vercel
├── Insomnia_2026-01-08.yaml # Arquivo de configuração para o Insomnia
└── smartmart.db         # Arquivo do banco de dados SQLite
```

## 🚀 Como Executar Localmente

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

- Python 3.10 ou superior
- Pip (gerenciador de pacotes do Python)

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/smartmart-API.git
    cd smartmart-API
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### Execução

Com o ambiente configurado, inicie o servidor de desenvolvimento Uvicorn:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`. A documentação interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.

## 🛠️ Usando a API com Insomnia

Para facilitar os testes dos endpoints, o projeto inclui um arquivo de configuração para o cliente de API **Insomnia**. Este arquivo já contém todas as rotas da API pré-configuradas.

### Como importar o arquivo no Insomnia:

1.  Abra o Insomnia.
2.  Vá para o menu principal (canto superior esquerdo) e clique em **"Import/Export"**.
3.  Na janela que abrir, clique em **"Import Data"** e depois em **"From File"**.
4.  Selecione o arquivo `Insomnia_2026-01-08.yaml` que está na raiz deste projeto.
5.  Após a importação, uma nova coleção chamada "SmartMart Solutions" será criada, contendo todas as requisições prontas para serem usadas.

## Endpoints da API

A API oferece os seguintes endpoints:

### Produtos (`/products`)

- `GET /products`: Retorna uma lista de todos os produtos.
- `POST /products`: Cria um novo produto.
- `GET /products/export_csv`: Exporta todos os produtos para um arquivo CSV.
- `POST /products/import_csv`: Importa produtos a partir de um arquivo CSV.

### Categorias (`/categories`)

- `GET /categories`: Retorna uma lista de todas as categorias.
- `POST /categories`: Cria uma nova categoria.
- `POST /categories/import_csv`: Importa categorias a partir de um arquivo CSV.

### Vendas (`/sales`)

- `GET /sales`: Retorna uma lista de todas as vendas.
- `POST /sales`: Registra uma nova venda.
- `POST /sales/import_csv`: Importa dados de vendas a partir de um arquivo CSV.

## ☁️ Deploy

O projeto está pré-configurado para deploy na plataforma **Vercel**. O arquivo `vercel.json` define a rota de build e o redirecionamento, apontando todas as requisições para o entrypoint `api/index.py`. Para fazer o deploy, basta conectar seu repositório Git à Vercel.
