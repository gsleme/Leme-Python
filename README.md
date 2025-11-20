# Leme - Plataforma de Reskilling

## 📝 Descrição

Este projeto implementa um sistema de back-end em Python, no formato de uma aplicação de console (CLI), para gerenciar as operações de uma plataforma de reskilling voltada para empresas. O sistema é modular e foi desenhado para ser a camada de dados de uma aplicação maior, permitindo o controle total sobre as entidades principais do negócio.

O nome "Leme" simboliza a direção e o controle que a plataforma oferece às empresas para guiar o desenvolvimento de seus colaboradores.

## ✨ Funcionalidades Principais

O sistema oferece um gerenciamento completo (CRUD - Criar, Ler, Atualizar, Deletar) para os seguintes módulos:

- **Gerenciamento de Usuários:**
  - Cadastrar, listar, atualizar e remover colaboradores da plataforma.

- **Gerenciamento de Trilhas de Aprendizado:**
  - Criar, visualizar, modificar e excluir trilhas de aprendizado, que são conjuntos de módulos.

- **Gerenciamento de Módulos:**
  - Adicionar, consultar, editar e excluir módulos de conteúdo, como cursos e workshops.

- **Gerenciamento de Progresso:**
  - Registrar e acompanhar o progresso dos usuários nas trilhas e módulos.

- **Menus Interativos:**
  - Uma interface de linha de comando (CLI) que guia o administrador de forma intuitiva através de todas as operações disponíveis.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Bibliotecas:** Funções nativas do Python, sem dependências externas.

## 🚀 Como Executar o Projeto

**Pré-requisitos:**

- Ter o Python 3 instalado em seu ambiente.

**Execução:**

1. Clone ou faça o download deste repositório.
2. Navegue até a pasta raiz do projeto.
3. Para iniciar o sistema, execute o arquivo `main.py` no seu terminal:

```bash
python main.py
```

4. Navegue pelos menus para acessar as funcionalidades desejadas.

## 📂 Estrutura do Projeto

```
leme/
├── main.py            # Ponto de entrada da aplicação e menu principal
├── usuarios.py        # Módulo para gerenciamento de usuários
├── trilhas.py         # Módulo para gerenciamento de trilhas de aprendizado
├── modulos.py         # Módulo para gerenciamento de módulos de conteúdo
├── progressos.py      # Módulo para gerenciamento do progresso dos usuários
├── utilitarios.py     # Funções auxiliares (validações, IDs, etc.)
├── pyproject.toml     # Arquivo de configuração do projeto
└── README.md          # Este arquivo
```

## 👨‍💻 Autores
Nome	                                  RM
Felipe Ferrete Lemes	                  RM562999
Gustavo Bosak Santos	                  RM566315
Nikolas Henrique de Souza Lemes Brisola	RM564371