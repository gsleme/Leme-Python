import oracledb
from datetime import datetime
import regex
import re
import uuid
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env (se ele existir)
load_dotenv()

'''
Lembrar de pip install regex
pip install oracledb
pip install python-dotenv
'''

# criar (obter) uma conexão com o banco de dados Oracle
def getConnection():
    """
    Obtém uma conexão com o banco de dados Oracle usando credenciais
    das variáveis de ambiente (lidas de um arquivo .env localmente).
    """
    try:
        user = os.getenv("ORACLE_USER")
        password = os.getenv("ORACLE_PASSWORD")
        dsn = os.getenv("ORACLE_DSN")

        # Valida se as variáveis de ambiente essenciais foram carregadas
        if not all([user, password, dsn]):
            print("Erro: As variáveis de ambiente ORACLE_USER, ORACLE_PASSWORD, e ORACLE_DSN devem ser definidas.")
            print("Por favor, crie um arquivo .env na raiz do projeto e adicione as credenciais. Veja o README.md para mais detalhes.")
            return None

        conn = oracledb.connect(user=user, password=password, dsn=dsn)
        print('Conexão com Oracle DB realizada!')
        return conn
    except Exception as e:
        print(f'Erro ao obter a conexão: {e}')
        return None


# --- Valida Números Inteiros ---
def validar_inteiro(entrada: str, default=None) -> int:
    """
    Solicita um valor e garante que é um número inteiro, repetindo até ser válido.
    """
    while True:
        valor_input = input(entrada)
        if not valor_input and default is not None:
            return default
        try:
            valor = int(valor_input)
            return valor
        except ValueError:
            print(f"Entrada inválida. Por favor, digite um número inteiro.")

# --- Valida Números de Ponto Flutuante ---
def validar_float(entrada: str, default=None) -> float:
    """
    Solicita um valor e garante que é um número de ponto flutuante, repetindo até ser válido.
    """
    while True:
        valor_input = input(entrada)
        if not valor_input and default is not None:
            return default
        try:
            valor = float(valor_input)
            return valor
        except ValueError:
            print(f"Entrada inválida. Por favor, digite um número de ponto flutuante.")


# --- Valida Data e Hora (a partir de hoje) ---
def validar_data(mensagem: str) -> datetime:
    """
    Solicita uma data/hora no formato 'DD/MM/AAAA HH:MM' e valida se é futura ou atual.
    Repete até receber uma data/hora válida.
    """
    formato = "%d/%m/%Y %H:%M"
    while True:
        entrada = input(mensagem) # Solicita a entrada dentro do loop
        if not entrada:
            return datetime.now()
        try:
            data = datetime.strptime(entrada, formato)
            
            # Compara a data inserida (sem segundos/microssegundos) com a data/hora atual
            # para evitar problemas de comparação de milissegundos.
            if data < datetime.now().replace(microsecond=0):
                print("Operação cancelada. Inserir apenas uma data/hora válida a partir de agora.")
            else:
                return data 
            
        except ValueError:
            print(f"Operação cancelada. Inserir apenas no formato exato '{formato}'.")


# --- Valida Nome ---
def validar_nome(mensagem: str) -> str:
    """
    Solicita o nome do usuário, valida se contém apenas letras/espaços.
    Repete até ser válido.
    """
    while True:
        entrada = input(mensagem)
        nome_tratado = entrada.strip()

        # Padrão para letras, incluindo acentos e espaços (ajustado para melhor cobertura Unicode)
        padrao = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'

        if nome_tratado and re.fullmatch(padrao, nome_tratado):
            return nome_tratado
        else:
            print("Operação cancelada. Inserir apenas letras válidas.")


# --- Valida E-mail ---
def validar_email(mensagem: str) -> str:
    """
    Solicita e valida um e-mail do usuário. Repete até ser válido.
    Retorna o e-mail limpo e em minúsculas.
    """
    # Padrão mais robusto, requer a biblioteca 'regex' para \p{L}
    # Se usar apenas 're', use: r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    padrao = r'^[\p{L}0-9._%+-]+@[\p{L}0-9.-]+\.[\p{L}]{2,}$'

    while True:
        entrada = input(mensagem)
        email_tratado = entrada.strip().lower()

        # Usa regex.fullmatch, que é mais robusto para UNICODE.
        # Se usar 're', remova o 'flags' ou use re.IGNORECASE.
        if regex.fullmatch(padrao, email_tratado, flags=regex.UNICODE | regex.IGNORECASE):
            return email_tratado
        else:
            print("Operação cancelada. Digite um e-mail válido (ex: nome@dominio.com).")

def validar_string(mensagem: str, minimo: int = 1, maximo: int = 100, default=None) -> str:
    """
    Solicita uma string ao usuário e garante que ela não está vazia e está dentro
    de um comprimento mínimo e máximo. Repete até ser válida.
    """
    while True:
        entrada = input(mensagem)
        if not entrada and default is not None:
            return default
        
        string_tratada = entrada.strip()

        tamanho = len(string_tratada)

        if not string_tratada:
            print("Entrada inválida. O campo não pode ficar vazio.")
            continue

        if tamanho < minimo:
            print(f"Entrada inválida. O valor deve ter pelo menos {minimo} caracteres.")
        elif tamanho > maximo:
            print(f"Entrada inválida. O valor deve ter no máximo {maximo} caracteres.")

        else:
            return string_tratada

def validar_id():
    """
    Gera um ID único no formato UUID4.
    """
    return str(uuid.uuid4())


def validar_sim_nao(mensagem: str) -> str:
    """
    Solicita uma resposta 's' ou 'n' e a retorna.
    """
    while True:
        resposta = input(mensagem).lower()
        if resposta in ('s', 'n'):
            return resposta
        else:
            print("Opção inválida. Por favor, digite 's' ou 'n'.")

def converter_hora(o):
    """
    Converte objetos não serializáveis em JSON, como datetime.
    """
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f'O objeto do tipo: {o.__class__.__name__} nao pode ser transportado para Json')
