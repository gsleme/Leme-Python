import oracledb
import json
from utilitarios import getConnection, validar_string, validar_inteiro, validar_id

def create_modulo(id_modulo, id_trilha, titulo, descricao, tipo, conteudo, xp_recompensa, ordem, adaptacao_necessaria):
    """Insere um novo modulo no banco e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO LM_MODULOS (id_modulo, id_trilha, titulo, descricao, tipo, conteudo, xp_recompensa, ordem, adaptacao_necessaria)
                    VALUES (:id_modulo, :id_trilha, :titulo, :descricao, :tipo, :conteudo, :xp_recompensa, :ordem, :adaptacao_necessaria)
                """
                cursor.execute(sql, {'id_modulo': id_modulo, 'id_trilha': id_trilha, 'titulo': titulo, 'descricao': descricao, 'tipo': tipo, 'conteudo': conteudo, 'xp_recompensa': xp_recompensa, 'ordem': ordem, 'adaptacao_necessaria': adaptacao_necessaria})
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir Modulo: {e}')
        return False

def read_modulo():
    """Lê e retorna uma lista de todos os modulos do banco."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id_modulo, id_trilha, titulo, descricao, tipo, conteudo, xp_recompensa, ordem, adaptacao_necessaria FROM LM_MODULOS ORDER BY ordem"
                cursor.execute(sql)
                modulos = []
                for row in cursor.fetchall():
                    modulos.append({'id_modulo': row[0], 'id_trilha': row[1], 'titulo': row[2], 'descricao': row[3], 'tipo': row[4], 'conteudo': row[5], 'xp_recompensa': row[6], 'ordem': row[7], 'adaptacao_necessaria': row[8]})
                return modulos
    except oracledb.Error as e:
        print(f'\n Erro ao ler Modulos: {e}')
        return None

def update_modulo(id_modulo, novo_id_trilha, novo_titulo, nova_descricao, novo_tipo, novo_conteudo, nova_xp_recompensa, nova_ordem, nova_adaptacao_necessaria):
    """Atualiza um modulo e retorna True se a atualização for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE LM_MODULOS
                    SET id_trilha = :novo_id_trilha, titulo = :novo_titulo, descricao = :nova_descricao, tipo = :novo_tipo, conteudo = :novo_conteudo, xp_recompensa = :nova_xp_recompensa, ordem = :nova_ordem, adaptacao_necessaria = :nova_adaptacao_necessaria
                    WHERE id_modulo = :id_modulo
                """
                cursor.execute(sql, {'novo_id_trilha': novo_id_trilha, 'novo_titulo': novo_titulo, 'nova_descricao': nova_descricao, 'novo_tipo': novo_tipo, 'novo_conteudo': novo_conteudo, 'nova_xp_recompensa': nova_xp_recompensa, 'nova_ordem': nova_ordem, 'nova_adaptacao_necessaria': nova_adaptacao_necessaria, 'id_modulo': id_modulo})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar Modulo: {e}')
        return False

def delete_modulo(id_modulo):
    """Exclui um modulo e retorna True se a exclusão for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM LM_MODULOS WHERE id_modulo = :id_modulo"
                cursor.execute(sql, {'id_modulo': id_modulo})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir Modulo: {e}')
        return False

def exportar_modulos_json():
    """Exporta os modulos para um arquivo JSON e retorna True em caso de sucesso."""
    print('\n Exportando dados dos modulos para JSON...')
    modulos = read_modulo()
    if modulos is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not modulos:
        print(" Nenhum modulo cadastrado para exportar.")
        return True

    try:
        with open('modulos.json', 'w', encoding='utf-8') as f:
            json.dump(modulos, f, ensure_ascii=False, indent=4)
        print(' Dados exportados com sucesso para modulos.json.')
        return True
    except IOError as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_modulo():
    while True:
        print('\n**Menu - Modulo**')
        print('1. Inserir um novo Modulo')
        print('2. Listar todos os Modulos')
        print('3. Atualizar os dados de um Modulo')
        print('4. Excluir um Modulo')
        print('5. Exportar Modulos para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo um novo modulo ***')
            id_modulo = validar_id()
            id_trilha = validar_string('Digite o id_trilha do modulo: ')
            titulo = validar_string('Digite o titulo do modulo: ')
            descricao = validar_string('Digite a descricao do modulo: ')
            tipo = validar_string('Digite o tipo do modulo: ')
            conteudo = validar_string('Digite o conteudo do modulo: ')
            xp_recompensa = validar_inteiro('Digite a xp_recompensa do modulo: ')
            ordem = validar_inteiro('Digite a ordem do modulo: ')
            adaptacao_necessaria = validar_string('Digite a adaptacao_necessaria do modulo: ')
            
            if create_modulo(id_modulo, id_trilha, titulo, descricao, tipo, conteudo, xp_recompensa, ordem, adaptacao_necessaria):
                print(f'\n Modulo {titulo} (ID: {id_modulo}) foi adicionado com sucesso!')
            else:
                print('\n Falha ao adicionar o modulo.')

        elif opcao == 2:
            print('\n*** Listando todos os Modulos ***')
            modulos = read_modulo()
            if modulos is not None:
                if modulos:
                    print("\n--- Lista de Modulos ---")
                    for m in modulos:
                        print(f"ID: {m['id_modulo']}, ID Trilha: {m['id_trilha']}, Titulo: {m['titulo']}, Descricao: {m['descricao']}, Tipo: {m['tipo']}, Conteudo: {m['conteudo']}, XP: {m['xp_recompensa']}, Ordem: {m['ordem']}, Adaptacao Necessaria: {m['adaptacao_necessaria']}")
                        print('----------------------------------')
                else:
                    print(" Nenhum modulo encontrado.")
            else:
                print(" Erro ao listar os modulos.")

        elif opcao == 3:
            print('\n*** Atualizando um Modulo ***')
            id_modulo = validar_string('Digite o Id do Modulo que deseja atualizar: ')
            novo_id_trilha = validar_string('Digite o novo id_trilha do Modulo: ')
            novo_titulo = validar_string('Digite o novo Titulo do Modulo: ')
            nova_descricao = validar_string('Digite a nova descricao do Modulo: ')
            novo_tipo = validar_string('Digite o novo tipo do Modulo: ')
            novo_conteudo = validar_string('Digite o novo conteudo do Modulo: ')
            nova_xp_recompensa = validar_inteiro('Digite a nova xp_recompensa do Modulo: ')
            nova_ordem = validar_inteiro('Digite a nova ordem do Modulo: ')
            nova_adaptacao_necessaria = validar_string('Digite a nova adaptacao_necessaria do Modulo: ')
            
            if update_modulo(id_modulo, novo_id_trilha, novo_titulo, nova_descricao, novo_tipo, novo_conteudo, nova_xp_recompensa, nova_ordem, nova_adaptacao_necessaria):
                print(f'\n Os dados do Modulo {id_modulo} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhum Modulo com ID {id_modulo} foi encontrado ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo um Modulo ***')
            id_modulo = validar_string('Digite o Id do Modulo que deseja excluir: ')
            if delete_modulo(id_modulo):
                print(f'\n O Modulo {id_modulo} foi excluído com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhum Modulo com ID {id_modulo} foi encontrado ou ocorreu um erro.')
        
        elif opcao == 5:
            exportar_modulos_json()

        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_modulo()