import oracledb
import json
from utilitarios import getConnection, validar_string, validar_inteiro, validar_id, validar_data
from datetime import datetime # Importar datetime para a conversão

def create_trilha(id_trilha, titulo, descricao, area_foco, xp_trilha, data_criacao):
    """Insere uma nova trilha no banco e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO LM_TRILHAS (id_trilha, titulo, descricao, area_foco, xp_trilha, data_criacao)
                    VALUES (:id_trilha, :titulo, :descricao, :area_foco, :xp_trilha, :data_criacao)
                """
                cursor.execute(sql, {'id_trilha': id_trilha, 'titulo': titulo, 'descricao': descricao, 'area_foco': area_foco, 'xp_trilha': xp_trilha, 'data_criacao': data_criacao})
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir Trilha: {e}')
        return False

def read_trilha():
    """Lê todas as trilhas do banco e retorna uma lista de dicionários."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_trilha, titulo, descricao, area_foco, xp_trilha, data_criacao FROM LM_TRILHAS")
                # Transforma o resultado em uma lista de dicionários para fácil manipulação
                colunas = [col[0].lower() for col in cursor.description]
                trilhas = [dict(zip(colunas, row)) for row in cursor.fetchall()]
                return trilhas
    except oracledb.Error as e:
        print(f'\n Erro ao buscar Trilhas: {e}')
        return None

def update_trilha(id_trilha, novo_titulo, nova_descricao, nova_area_foco, nova_xp_trilha, nova_data_criacao):
    """Atualiza uma trilha e retorna True se a atualização for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE LM_TRILHAS SET
                    titulo = :novo_titulo,
                    descricao = :nova_descricao,
                    area_foco = :nova_area_foco,
                    xp_trilha = :nova_xp_trilha,
                    data_criacao = :nova_data_criacao
                    WHERE id_trilha = :id_trilha
                """
                cursor.execute(sql, {'novo_titulo': novo_titulo, 'nova_descricao': nova_descricao, 'nova_area_foco': nova_area_foco, 'nova_xp_trilha': nova_xp_trilha, 'nova_data_criacao': nova_data_criacao, 'id_trilha': id_trilha})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar Trilha: {e}')
        return False

def delete_trilha(id_trilha):
    """Exclui uma trilha e retorna True se a exclusão for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM LM_TRILHAS WHERE id_trilha = :id_trilha"
                cursor.execute(sql, {'id_trilha': id_trilha})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir Trilha: {e}')
        return False

def exportar_trilhas_json():
    """Exporta as trilhas para um arquivo JSON e retorna True em caso de sucesso."""
    print('\n Exportando dados das trilhas para JSON...')
    trilhas = read_trilha()
    if trilhas is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not trilhas:
        print(" Nenhuma trilha cadastrada para exportar.")
        return True
    
    # --- CORREÇÃO AQUI ---
    # Converte objetos datetime para string antes de serializar
    for trilha in trilhas:
        for key, value in trilha.items():
            if isinstance(value, datetime):
                trilha[key] = value.isoformat()
    
    try:
        with open('trilhas.json', 'w', encoding='utf-8') as f:
            json.dump(trilhas, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para trilhas.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_trilha():
    while True:
        print('\n**Menu - Trilha**')
        print('1. Inserir uma nova Trilha')
        print('2. Listar todas as Trilhas')
        print('3. Atualizar os dados de uma Trilha')
        print('4. Excluir uma Trilha')
        print('5. Exportar Trilhas para Json')
        print('6. Voltar ao menu principal')
        opcao = input("Digite uma opção entre 1 e 6: ")

        if opcao == '1':
            print("\n--- Inserir Nova Trilha ---")
            id_trilha = validar_id("ID da Trilha: ")
            titulo = validar_string("Título: ")
            descricao = validar_string("Descrição: ")
            area_foco = validar_string("Área de Foco: ")
            xp_trilha = validar_inteiro("XP da Trilha: ")
            data_criacao = validar_data("Data de Criação (YYYY-MM-DD): ")
            if create_trilha(id_trilha, titulo, descricao, area_foco, xp_trilha, data_criacao):
                print(" Trilha inserida com sucesso!")
            else:
                print(" Falha ao inserir a trilha.")

        elif opcao == '2':
            print("\n--- Lista de Trilhas ---")
            trilhas = read_trilha()
            if trilhas:
                for trilha in trilhas:
                    print(trilha)
            else:
                print(" Nenhuma trilha encontrada ou erro na busca.")

        elif opcao == '3':
            print("\n--- Atualizar Trilha ---")
            id_trilha = validar_id("ID da Trilha a ser atualizada: ")
            novo_titulo = validar_string("Novo Título: ")
            nova_descricao = validar_string("Nova Descrição: ")
            nova_area_foco = validar_string("Nova Área de Foco: ")
            nova_xp_trilha = validar_inteiro("Novo XP da Trilha: ")
            nova_data_criacao = validar_data("Nova Data de Criação (YYYY-MM-DD): ")
            if update_trilha(id_trilha, novo_titulo, nova_descricao, nova_area_foco, nova_xp_trilha, nova_data_criacao):
                print(" Trilha atualizada com sucesso!")
            else:
                print(" Trilha não encontrada ou falha na atualização.")

        elif opcao == '4':
            print("\n--- Excluir Trilha ---")
            id_trilha = validar_id("ID da Trilha a ser excluída: ")
            if delete_trilha(id_trilha):
                print(" Trilha excluída com sucesso!")
            else:
                print(" Trilha não encontrada ou falha ao excluir.")

        elif opcao == '5':
            exportar_trilhas_json()

        elif opcao == '6':
            print(" Retornando ao menu principal...")
            break
        
        else:
            print(" Opção inválida. Por favor, tente novamente.")
