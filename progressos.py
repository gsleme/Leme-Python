import oracledb
import json
from utilitarios import getConnection, validar_string, validar_id, validar_data, validar_inteiro

def create_progresso(id_progresso, id_usuario, id_modulo, data_conclusao):
    """Insere um novo progresso no banco e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO LM_PROGRESSOS (id_progresso, id_usuario, id_modulo, data_conclusao)
                    VALUES (:id_progresso, :id_usuario, :id_modulo, :data_conclusao)
                """
                cursor.execute(sql, {'id_progresso': id_progresso, 'id_usuario': id_usuario, 'id_modulo': id_modulo, 'data_conclusao': data_conclusao})
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir Progresso: {e}')
        return False

def read_progresso():
    """Lê e retorna uma lista de todos os progressos do banco."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id_progresso, id_usuario, id_modulo, data_conclusao FROM LM_PROGRESSOS ORDER BY data_conclusao"
                cursor.execute(sql)
                progressos = []
                for row in cursor.fetchall():
                    progressos.append({'id_progresso': row[0], 'id_usuario': row[1], 'id_modulo': row[2], 'data_conclusao': row[3]})
                return progressos
    except oracledb.Error as e:
        print(f'\n Erro ao ler Progressos: {e}')
        return None

def update_progresso(id_progresso, novo_id_usuario, novo_id_modulo, nova_data_conclusao):
    """Atualiza um progresso e retorna True se a atualização for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE LM_PROGRESSOS
                    SET id_usuario = :novo_id_usuario, id_modulo = :novo_id_modulo, data_conclusao = :nova_data_conclusao
                    WHERE id_progresso = :id_progresso
                """
                cursor.execute(sql, {'novo_id_usuario': novo_id_usuario, 'novo_id_modulo': novo_id_modulo, 'nova_data_conclusao': nova_data_conclusao, 'id_progresso': id_progresso})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar Progresso: {e}')
        return False

def delete_progresso(id_progresso):
    """Exclui um progresso e retorna True se a exclusão for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM LM_PROGRESSOS WHERE id_progresso = :id_progresso"
                cursor.execute(sql, {'id_progresso': id_progresso})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir Progresso: {e}')
        return False

def exportar_progressos_json():
    """Exporta os progressos para um arquivo JSON e retorna True em caso de sucesso."""
    print('\n Exportando dados dos progressos para JSON...')
    progressos = read_progresso()
    if progressos is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not progressos:
        print(" Nenhum progresso cadastrado para exportar.")
        return True

    try:
        with open('progressos.json', 'w', encoding='utf-8') as f:
            json.dump(progressos, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para progressos.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_progresso():
    while True:
        print('\n**Menu - Progresso**')
        print('1. Inserir um novo Progresso')
        print('2. Listar todos os Progressos')
        print('3. Atualizar os dados de um Progresso')
        print('4. Excluir um Progresso')
        print('5. Exportar Progressos para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo um novo progresso ***')
            id_progresso = validar_id()
            id_usuario = validar_string('Digite o id_usuario do progresso: ')
            id_modulo = validar_string('Digite o id_modulo do progresso: ')
            data_conclusao = validar_data('Digite a data de conclusão do progresso (DD/MM/AAAA HH:MM): ')

            if create_progresso(id_progresso, id_usuario, id_modulo, data_conclusao):
                print(f'\n Progresso (ID: {id_progresso}) foi adicionado com sucesso!')
            else:
                print('\n Falha ao adicionar o progresso.')

        elif opcao == 2:
            print('\n*** Listando todos os Progressos ***')
            progressos = read_progresso()
            if progressos is not None:
                if progressos:
                    print("\n--- Lista de Progressos ---")
                    for p in progressos:
                        print(f"ID: {p['id_progresso']}, ID Usuario: {p['id_usuario']}, ID Modulo: {p['id_modulo']}, Data de Conclusao: {p['data_conclusao']}")
                        print('----------------------------------')
                else:
                    print(" Nenhum progresso encontrado.")
            else:
                print(" Erro ao listar os progressos.")

        elif opcao == 3:
            print('\n*** Atualizando um Progresso ***')
            id_progresso = validar_string('Digite o Id do Progresso que deseja atualizar: ')
            novo_id_usuario = validar_string('Digite o novo id_usuario do Progresso: ')
            novo_id_modulo = validar_string('Digite o novo id_modulo do Progresso: ')
            nova_data_conclusao = validar_data('Digite a nova data de conclusão do Progresso (DD/MM/AAAA HH:MM): ')

            if update_progresso(id_progresso, novo_id_usuario, novo_id_modulo, nova_data_conclusao):
                print(f'\n Os dados do Progresso {id_progresso} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhum Progresso com ID {id_progresso} foi encontrado ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo um Progresso ***')
            id_progresso = validar_string('Digite o Id do Progresso que deseja excluir: ')
            if delete_progresso(id_progresso):
                print(f'\n O Progresso {id_progresso} foi excluído com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhum Progresso com ID {id_progresso} foi encontrado ou ocorreu um erro.')

        elif opcao == 5:
            exportar_progressos_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_progresso()