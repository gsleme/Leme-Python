# Leme: Plataforma de Reskilling e API

Este projeto é a Plataforma de Reskilling "Leme". Ele oferece funcionalidades completas de **CRUD (Create, Read, Update, Delete) e exportação para json** para gerenciar seus recursos através de dois componentes principais: uma **API RESTful** e uma **Interface de Linha de Comando (CLI)** interativa.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
/
|-- api.py                  # Ponto de entrada da API Flask, define todos os endpoints.
|-- main.py                 # Interface de Linha de Comando (CLI) com menus para CRUD.
|-- test_api.py             # Suíte de testes de integração para validar os endpoints da API.
|-- requirements.txt        # Lista de dependências do Python.
|-- README.md               # Este arquivo.
|
|-- usuarios.py             # Lógica de CRUD para a tabela de usuários.
|-- trilhas.py              # Lógica de CRUD para a tabela de trilhas.
|-- modulos.py              # Lógica de CRUD para a tabela de módulos.
|-- progressos.py           # Lógica de CRUD para a tabela de progressos.
|-- sugestoes.py            # Lógica de CRUD para a tabela de sugestões.
|-- previsoes.py            # Lógica de CRUD para a tabela de previsões.
|
`-- utilitarios.py          # Funções utilitárias.
```

## Tecnologias

*   **Python 3:** Linguagem de programação principal.
*   **Flask:** Microframework web para a criação da API.
*   **Requests:** Biblioteca para realizar as chamadas HTTP nos testes.
*   **python-dotenv:** Para gerenciamento de variáveis de ambiente em desenvolvimento.

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd Leme-Python
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuração do Ambiente Local

Para executar o projeto localmente, o sistema precisa das credenciais de acesso ao banco de dados Oracle.

1.  **Crie um arquivo `.env`** na raiz do projeto. Este arquivo não é versionado para proteger suas credenciais.

2.  **Adicione as seguintes variáveis** ao arquivo `.env`, substituindo os valores de exemplo pelas suas credenciais reais:
    ```env
    ORACLE_USER=seu_usuario
    ORACLE_PASSWORD=sua_senha
    ORACLE_DSN=seu_dsn_oracle
    ```

O sistema está configurado para ler essas variáveis automaticamente durante a execução.

## Como Usar

O projeto pode ser executado de duas formas:

### 1. Executando a API RESTful

Para iniciar o servidor da API, que oferece endpoints para operações de CRUD em todos os recursos, execute:

```bash
python api.py
```

O servidor estará em execução no endereço `http://127.0.0.1:8080`.

### 2. Executando a Interface de Linha de Comando (CLI)

Para usar a aplicação via terminal, que oferece um menu para realizar operações de CRUD (Criar, Ler, Atualizar, Deletar) em todos os recursos, execute:

```bash
python main.py
```

### Validando a API com Testes

Para garantir que todos os endpoints da API estão funcionando corretamente, execute a suíte de testes:

```bash
python test_api.py
```

Você deverá ver uma saída indicando que todos os testes passaram (`OK`).

## 👨‍💻 Autores

| Nome                                  | RM       |
| ------------------------------------- | -------- |
| Felipe Ferrete Lemes                  | RM562999 |
| Gustavo Bosak Santos                  | RM566315 |
| Nikolas Henrique de Souza Lemes Brisola | RM564371 |