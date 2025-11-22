import oracledb
import json
from utilitarios import getConnection, validar_string, validar_id, validar_data, validar_inteiro, converter_hora

def create_sugestao(id_sugestao, id_usuario, id_trilha, data_sugestao):
    """Insere uma nova sugestão no banco e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO LM_SUGESTOES (id_sugestao, id_usuario, id_trilha, data_sugestao)
                    VALUES (:id_sugestao, :id_usuario, :id_trilha, :data_sugestao)
                """
                cursor.execute(sql, {'id_sugestao': id_sugestao, 'id_usuario': id_usuario, 'id_trilha': id_trilha, 'data_sugestao': data_sugestao})
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir Sugestão: {e}')
        return False

def read_sugestao():
    """Lê e retorna uma lista de todas as sugestões do banco."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id_sugestao, id_usuario, id_trilha, data_sugestao FROM LM_SUGESTOES ORDER BY data_sugestao"
                cursor.execute(sql)
                sugestoes = []
                for row in cursor.fetchall():
                    sugestoes.append({'id_sugestao': row[0], 'id_usuario': row[1], 'id_trilha': row[2], 'data_sugestao': row[3]})
                return sugestoes
    except oracledb.Error as e:
        print(f'\n Erro ao ler Sugestões: {e}')
        return None

def update_sugestao(id_sugestao, novo_id_usuario, novo_id_trilha, nova_data_sugestao):
    """Atualiza uma sugestão e retorna True se a atualização for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE LM_SUGESTOES
                    SET id_usuario = :novo_id_usuario, id_trilha = :novo_id_trilha, data_sugestao = :nova_data_sugestao
                    WHERE id_sugestao = :id_sugestao
                """
                cursor.execute(sql, {'novo_id_usuario': novo_id_usuario, 'novo_id_trilha': novo_id_trilha, 'nova_data_sugestao': nova_data_sugestao, 'id_sugestao': id_sugestao})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar Sugestão: {e}')
        return False

def delete_sugestao(id_sugestao):
    """Exclui uma sugestão e retorna True se a exclusão for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM LM_SUGESTOES WHERE id_sugestao = :id_sugestao"
                cursor.execute(sql, {'id_sugestao': id_sugestao})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir Sugestão: {e}')
        return False

def exportar_sugestoes_json():
    """Exporta as sugestões para um arquivo JSON e retorna True em caso de sucesso."""
    print('\n Exportando dados das sugestões para JSON...')
    sugestoes = read_sugestao()
    if sugestoes is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not sugestoes:
        print(" Nenhuma sugestão cadastrada para exportar.")
        return True

    try:
        with open('sugestoes.json', 'w', encoding='utf-8') as f:
            json.dump(sugestoes, f, ensure_ascii=False, indent=4, default=converter_hora)
        print(' Dados exportados com sucesso para sugestoes.json.')
        return True
    except (IOError, TypeError) as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_sugestao():
    while True:
        print('\n**Menu - Sugestões**')
        print('1. Inserir uma nova Sugestão')
        print('2. Listar todas as Sugestões')
        print('3. Atualizar os dados de uma Sugestão')
        print('4. Excluir uma Sugestão')
        print('5. Exportar Sugestões para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo uma nova sugestão ***')
            id_sugestao = validar_id()
            id_usuario = validar_string('Digite o id_usuario da sugestão: ')
            id_trilha = validar_string('Digite o id_trilha da sugestão: ')
            data_sugestao = validar_data('Digite a data da sugestão (DD/MM/AAAA HH:MM): ')

            if create_sugestao(id_sugestao, id_usuario, id_trilha, data_sugestao):
                print(f'\n Sugestão (ID: {id_sugestao}) foi adicionada com sucesso!')
            else:
                print('\n Falha ao adicionar a sugestão.')

        elif opcao == 2:
            print('\n*** Listando todas as Sugestões ***')
            sugestoes = read_sugestao()
            if sugestoes is not None:
                if sugestoes:
                    print("\n--- Lista de Sugestões ---")
                    for s in sugestoes:
                        print(f"ID: {s['id_sugestao']}, ID Usuario: {s['id_usuario']}, ID Trilha: {s['id_trilha']}, Data da Sugestão: {s['data_sugestao']}")
                        print('----------------------------------')
                else:
                    print(" Nenhuma sugestão encontrada.")
            else:
                print(" Erro ao listar as sugestões.")

        elif opcao == 3:
            print('\n*** Atualizando uma Sugestão ***')
            id_sugestao = validar_string('Digite o Id da Sugestão que deseja atualizar: ')
            novo_id_usuario = validar_string('Digite o novo id_usuario da Sugestão: ')
            novo_id_trilha = validar_string('Digite o novo id_trilha da Sugestão: ')
            nova_data_sugestao = validar_data('Digite a nova data da sugestão (DD/MM/AAAA HH:MM): ')

            if update_sugestao(id_sugestao, novo_id_usuario, novo_id_trilha, nova_data_sugestao):
                print(f'\n Os dados da Sugestão {id_sugestao} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhuma Sugestão com ID {id_sugestao} foi encontrada ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo uma Sugestão ***')
            id_sugestao = validar_string('Digite o Id da Sugestão que deseja excluir: ')
            if delete_sugestao(id_sugestao):
                print(f'\n A Sugestão {id_sugestao} foi excluída com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhuma Sugestão com ID {id_sugestao} foi encontrada ou ocorreu um erro.')

        elif opcao == 5:
            exportar_sugestoes_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_sugestao()
