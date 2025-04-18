# Atividade BD2 – Conexão com Banco de Dados

Este projeto foi desenvolvido como parte da disciplina de Banco de Dados II, com foco na implementação de uma API RESTful utilizando Flask, SQLAlchemy e PostgreSQL. O principal objetivo é explorar as diferenças entre utilizar ou não um ORM na manipulação de banco de dados, destacando também as vulnerabilidades associadas à ausência de um ORM, como a exposição a ataques de SQL Injection.

## 🔧 Tecnologias Utilizadas

- Python
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- SQLAlchemy
- psycopg (driver PostgreSQL)
- PostgreSQL
- JavaScript (frontend)
- React.js
- HTML/CSS
- Postman (teste de rotas)

## 📁 Estrutura do Projeto

```
Atividade_BD2_conexao_com_banco_de_dados/
├── back/
│   ├── app.py 
│   │   
│   ├── api/
│   │   ├── customer.py
│   │   ├── employee.py
│   │   ├── order.py
│   │   ├── order_detail.py
│   │   ├── reports.py
│   │   └── shippers.py
│   │  
│   ├── config/
│   │   └── db_config.py
│   │  
│   ├── dao/
│   │   ├── drive/
│   │   │   ├── customer_dao.py
│   │   │   ├── employee_dao.py
│   │   │   ├── order_dao.py
│   │   │   ├── order_detail_dao.py
│   │   │   └── shippers_dao.py
│   │   └── orm/
│   │       ├── customer_dao.py
│   │       ├── employee_dao.py
│   │       ├── order_dao.py
│   │       ├── order_detail.py
│   │       └── shippers_dao.py
│   │  
│   ├── models/
│   │   └── models.py
│   │  
│   └── requirements.txt
│   
├── northwind-front/
│   └── src/
│       ├── components
│       │    ├── Loading.jsx
│       │    └── OrderItemRow.jsx
│       │
│       ├── pages
│       │    ├── EmployeeRankingPage.jsx
│       │    ├── NewOrderPage.jsx
│       │    └── OrdersReportPage.jsx
│       │ 
│       └── services
|            └── api.js
│   
└── README.md
```

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/pdrVenancio/Atividade_BD2_conexao_com_banco_de_dados.git
   cd Atividade_BD2_conexao_com_banco_de_dados/back
   ```

2. **Instale as dependências Back-end:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Instale dependencias do Front-end:**

   ```bash
   npm i
   ```

4. **Inicie Back-end:**

   ```bash
   python app.py
   ```

5. **Inicie Front-end:**

   ```bash
   npm run dev
   ```

A API estará disponível em `http://localhost:5000/`.

## 🧪 Funcionalidades

- Listagem de orders.
- Inserção de novos orders.
- Ranking de funcionarios baseando no valor total que eles venderam.

## 🛠️ Estrutura do Backend

- **app.py**: Ponto de entrada da aplicação Flask.
- **config/db_config.py**: Configurações de conexão com o banco de dados.
- **dao/**: Data Access Objects, contendo a lógica de acesso aos dados.
  - **drive/**: Implementações diretas com SQL permitindo SQL injection.
  - **orm/**: Implementações utilizando SQLAlchemy ORM.
- **models/**: Definição das classes que representam as tabelas do banco de dados.

## 📦 Dependências

As dependências do Back-end projeto estão listadas no arquivo `requirements.txt`. Certifique-se de instalá-las antes de executar a aplicação.

## 📄 Desenvolvido por

Pedro Venâncio dos Santos - 2023010066 [gitHub](https://github.com/pdrVenancio)

Breno Vieira Nogueira Carneiro - 2023003929 [gitHub](https://github.com/Brenovnc)

