import oracledb
import json
from utilitarios import getConnection, validar_string, validar_inteiro, validar_id, validar_data

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
    """Lê e retorna uma lista de todas as trilhas do banco."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id_trilha, titulo, descricao, area_foco, xp_trilha, data_criacao FROM LM_TRILHAS ORDER BY titulo"
                cursor.execute(sql)
                trilhas = []
                for row in cursor.fetchall():
                    trilhas.append({'id_trilha': row[0], 'titulo': row[1], 'descricao': row[2], 'area_foco': row[3], 'xp_trilha': row[4], 'data_criacao': row[5]})
                return trilhas
    except oracledb.Error as e:
        print(f'\n Erro ao ler Trilhas: {e}')
        return None

def update_trilha(id_trilha, novo_titulo, nova_descricao, nova_area_foco, nova_xp_trilha, nova_data_criacao):
    """Atualiza uma trilha e retorna True se a atualização for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE LM_TRILHAS
                    SET titulo = :novo_titulo, descricao = :nova_descricao, area_foco = :nova_area_foco, xp_trilha = :nova_xp_trilha, data_criacao = :nova_data_criacao
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

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo uma nova trilha ***')
            id_trilha = validar_id()
            titulo = validar_string('Digite o titulo da trilha: ')
            descricao = validar_string('Digite a descricao da trilha: ')
            area_foco = validar_string('Digite a area_foco da trilha: ')
            xp_trilha = validar_inteiro('Digite a xp_trilha da trilha: ')
            data_criacao = validar_data('Digite a data de criação da trilha (DD/MM/AAAA HH:MM): ')

            if create_trilha(id_trilha, titulo, descricao, area_foco, xp_trilha, data_criacao):
                print(f'\n Trilha {titulo} (ID: {id_trilha}) foi adicionada com sucesso!')
            else:
                print('\n Falha ao adicionar a trilha.')

        elif opcao == 2:
            print('\n*** Listando todas as Trilhas ***')
            trilhas = read_trilha()
            if trilhas is not None:
                if trilhas:
                    print("\n--- Lista de Trilhas ---")
                    for t in trilhas:
                        print(f"ID: {t['id_trilha']}, Titulo: {t['titulo']}, Descricao: {t['descricao']}, Area de Foco: {t['area_foco']}, XP: {t['xp_trilha']}, Data de Criacao: {t['data_criacao']}")
                        print('----------------------------------')
                else:
                    print(" Nenhuma trilha encontrada.")
            else:
                print(" Erro ao listar as trilhas.")

        elif opcao == 3:
            print('\n*** Atualizando uma Trilha ***')
            id_trilha = validar_string('Digite o Id da Trilha que deseja atualizar: ')
            novo_titulo = validar_string('Digite o novo Titulo da Trilha: ')
            nova_descricao = validar_string('Digite a nova descricao da Trilha: ')
            nova_area_foco = validar_string('Digite a nova area_foco da Trilha: ')
            nova_xp_trilha = validar_inteiro('Digite a nova xp_trilha da Trilha: ')
            nova_data_criacao = validar_data('Digite a nova data de criação da Trilha (DD/MM/AAAA HH:MM): ')

            if update_trilha(id_trilha, novo_titulo, nova_descricao, nova_area_foco, nova_xp_trilha, nova_data_criacao):
                print(f'\n Os dados da Trilha {id_trilha} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhuma Trilha com ID {id_trilha} foi encontrada ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo uma Trilha ***')
            id_trilha = validar_string('Digite o Id da Trilha que deseja excluir: ')
            if delete_trilha(id_trilha):
                print(f'\n A Trilha {id_trilha} foi excluída com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhuma Trilha com ID {id_trilha} foi encontrada ou ocorreu um erro.')

        elif opcao == 5:
            exportar_trilhas_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_trilha()