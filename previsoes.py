import oracledb
import json
from utilitarios import getConnection, validar_string, validar_id, validar_data, validar_float, converter_hora, validar_inteiro

def create_previsao(id_previsao, id_usuario, taxa_sucesso, categoria, data_previsao):
    """Insere uma nova previsão no banco e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO LM_PREVISOES (id_previsao, id_usuario, taxa_sucesso, categoria, data_previsao)
                    VALUES (:id_previsao, :id_usuario, :taxa_sucesso, :categoria, :data_previsao)
                """
                cursor.execute(sql, {'id_previsao': id_previsao, 'id_usuario': id_usuario, 'taxa_sucesso': taxa_sucesso, 'categoria': categoria, 'data_previsao': data_previsao})
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir Previsão: {e}')
        return False

def read_previsao():
    """Lê e retorna uma lista de todas as previsões do banco."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id_previsao, id_usuario, taxa_sucesso, categoria, data_previsao FROM LM_PREVISOES ORDER BY data_previsao"
                cursor.execute(sql)
                previsoes = []
                for row in cursor.fetchall():
                    previsoes.append({'id_previsao': row[0], 'id_usuario': row[1], 'taxa_sucesso': row[2], 'categoria': row[3], 'data_previsao': row[4]})
                return previsoes
    except oracledb.Error as e:
        print(f'\n Erro ao ler Previsões: {e}')
        return None

def update_previsao(id_previsao, novo_id_usuario, nova_taxa_sucesso, nova_categoria, nova_data_previsao):
    """Atualiza uma previsão e retorna True se a atualização for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE LM_PREVISOES
                    SET id_usuario = :novo_id_usuario, taxa_sucesso = :nova_taxa_sucesso, categoria = :nova_categoria, data_previsao = :nova_data_previsao
                    WHERE id_previsao = :id_previsao
                """
                cursor.execute(sql, {'novo_id_usuario': novo_id_usuario, 'nova_taxa_sucesso': nova_taxa_sucesso, 'nova_categoria': nova_categoria, 'nova_data_previsao': nova_data_previsao, 'id_previsao': id_previsao})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar Previsão: {e}')
        return False

def delete_previsao(id_previsao):
    """Exclui uma previsão e retorna True se a exclusão for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM LM_PREVISOES WHERE id_previsao = :id_previsao"
                cursor.execute(sql, {'id_previsao': id_previsao})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir Previsão: {e}')
        return False

def exportar_previsoes_json():
    """Exporta as previsões para um arquivo JSON e retorna True em caso de sucesso."""
    print('\n Exportando dados das previsões para JSON...')
    previsoes = read_previsao()
    if previsoes is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not previsoes:
        print(" Nenhuma previsão cadastrada para exportar.")
        return True

    try:
        with open('previsoes.json', 'w', encoding='utf-8') as f:
            json.dump(previsoes, f, ensure_ascii=False, indent=4, default=converter_hora)
        print(' Dados exportados com sucesso para previsoes.json.')
        return True
    except (IOError, TypeError) as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_previsao():
    while True:
        print('\n**Menu - Previsões**')
        print('1. Inserir uma nova Previsão')
        print('2. Listar todas as Previsões')
        print('3. Atualizar os dados de uma Previsão')
        print('4. Excluir uma Previsão')
        print('5. Exportar Previsões para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo uma nova previsão ***')
            id_previsao = validar_id()
            id_usuario = validar_string('Digite o id_usuario da previsão: ')
            taxa_sucesso = validar_float('Digite a taxa de sucesso da previsão: ')
            categoria = validar_string('Digite a categoria da previsão: ')
            data_previsao = validar_data('Digite a data da previsão (DD/MM/AAAA HH:MM): ')

            if create_previsao(id_previsao, id_usuario, taxa_sucesso, categoria, data_previsao):
                print(f'\n Previsão (ID: {id_previsao}) foi adicionada com sucesso!')
            else:
                print('\n Falha ao adicionar a previsão.')

        elif opcao == 2:
            print('\n*** Listando todas as Previsões ***')
            previsoes = read_previsao()
            if previsoes is not None:
                if previsoes:
                    print("\n--- Lista de Previsões ---")
                    for p in previsoes:
                        print(f"ID: {p['id_previsao']}, ID Usuario: {p['id_usuario']}, Taxa de Sucesso: {p['taxa_sucesso']}, Categoria: {p['categoria']}, Data da Previsão: {p['data_previsao']}")
                        print('----------------------------------')
                else:
                    print(" Nenhuma previsão encontrada.")
            else:
                print(" Erro ao listar as previsões.")

        elif opcao == 3:
            print('\n*** Atualizando uma Previsão ***')
            id_previsao = validar_string('Digite o Id da Previsão que deseja atualizar: ')
            novo_id_usuario = validar_string('Digite o novo id_usuario da Previsão: ')
            nova_taxa_sucesso = validar_float('Digite a nova taxa de sucesso da Previsão: ')
            nova_categoria = validar_string('Digite a nova categoria da Previsão: ')
            nova_data_previsao = validar_data('Digite a nova data da previsão (DD/MM/AAAA HH:MM): ')

            if update_previsao(id_previsao, novo_id_usuario, nova_taxa_sucesso, nova_categoria, nova_data_previsao):
                print(f'\n Os dados da Previsão {id_previsao} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhuma Previsão com ID {id_previsao} foi encontrada ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo uma Previsão ***')
            id_previsao = validar_string('Digite o Id da Previsão que deseja excluir: ')
            if delete_previsao(id_previsao):
                print(f'\n A Previsão {id_previsao} foi excluída com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhuma Previsão com ID {id_previsao} foi encontrada ou ocorreu um erro.')

        elif opcao == 5:
            exportar_previsoes_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_previsao()
