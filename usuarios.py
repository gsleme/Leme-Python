import oracledb
import json
from utilitarios import getConnection, validar_nome, validar_inteiro, validar_email, validar_string, validar_id, validar_sim_nao, validar_data, converter_hora

def create_usuario(id_usuario, nome, userName, email, senha, area, acessibilidade, xp_total, data_cadastro):
    """Insere um novo usuario no banco e retorna True em caso de sucesso."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO LM_USUARIOS (id_usuario, nome, userName, email, senha, area, acessibilidade, xp_total, data_cadastro)
                    VALUES (:id_usuario, :nome, :userName, :email, :senha, :area, :acessibilidade, :xp_total, :data_cadastro)
                """
                cursor.execute(sql, {'id_usuario': id_usuario, 'nome': nome, 'userName': userName, 'email': email, 'senha': senha, 'area': area, 'acessibilidade': acessibilidade, 'xp_total': xp_total, 'data_cadastro': data_cadastro})
                conn.commit()
                return True
    except oracledb.Error as e:
        print(f'\n Erro ao inserir Usuario: {e}')
        return False

def read_usuario():
    """Lê e retorna uma lista de todos os usuarios do banco."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id_usuario, nome, userName, email, senha, area, acessibilidade, xp_total, data_cadastro FROM LM_USUARIOS ORDER BY nome"
                cursor.execute(sql)
                usuarios = []
                for row in cursor.fetchall():
                    usuarios.append({'id_usuario': row[0], 'nome': row[1], 'userName': row[2], 'email': row[3], 'senha': row[4], 'area': row[5], 'acessibilidade': row[6], 'xp_total': row[7], 'data_cadastro': row[8]})
                return usuarios
    except oracledb.Error as e:
        print(f'\n Erro ao ler Usuarios: {e}')
        return None

def update_usuario(id_usuario, novo_nome, novo_userName, novo_email, nova_senha, nova_area, nova_acessibilidade, novo_xp_total, nova_data_cadastro):
    """Atualiza um usuario e retorna True se a atualização for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE LM_USUARIOS
                    SET nome = :novo_nome, userName = :novo_userName, email = :novo_email, senha = :nova_senha, area = :nova_area, acessibilidade = :nova_acessibilidade, xp_total = :novo_xp_total, data_cadastro = :nova_data_cadastro
                    WHERE id_usuario = :id_usuario
                """
                cursor.execute(sql, {'novo_nome': novo_nome, 'novo_userName': novo_userName, 'novo_email': novo_email, 'nova_senha': nova_senha, 'nova_area': nova_area, 'nova_acessibilidade': nova_acessibilidade, 'novo_xp_total': novo_xp_total, 'nova_data_cadastro': nova_data_cadastro, 'id_usuario': id_usuario})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao atualizar Usuario: {e}')
        return False

def delete_usuario(id_usuario):
    """Exclui um usuario e retorna True se a exclusão for bem-sucedida."""
    try:
        with getConnection() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM LM_USUARIOS WHERE id_usuario = :id_usuario"
                cursor.execute(sql, {'id_usuario': id_usuario})
                conn.commit()
                return cursor.rowcount > 0
    except oracledb.Error as e:
        print(f'\n Erro ao excluir Usuario: {e}')
        return False

def exportar_usuarios_json():
    """Exporta os usuarios para um arquivo JSON e retorna True em caso de sucesso."""
    print('\n Exportando dados dos usuarios para JSON...')
    usuarios = read_usuario()
    if usuarios is None:
        print(' Não foi possível obter os dados para exportar.')
        return False
    if not usuarios:
        print(" Nenhum usuario cadastrado para exportar.")
        return True

    try:
        with open('usuarios.json', 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=4, default=converter_hora)
        print(' Dados exportados com sucesso para usuarios.json.')
        return True
    except (IOError, TypeError) as e:
        print(f' Erro ao escrever o arquivo JSON: {e}')
        return False

def main_usuario():
    while True:
        print('\n**Menu - Usuario**')
        print('1. Inserir um novo Usuario')
        print('2. Listar todos os Usuarios')
        print('3. Atualizar os dados de um Usuario')
        print('4. Excluir um Usuario')
        print('5. Exportar Usuarios para Json')
        print('6. Voltar ao menu principal')

        opcao = validar_inteiro('Digite uma opção entre 1 e 6: ')
        if opcao == 1:
            print('\n*** Inserindo um novo usuario ***')
            id_usuario = validar_id()
            nome = validar_nome('Digite o nome do usuario: ')
            userName = validar_string('Digite o userName do usuario: ')
            email = validar_email('Digite o email do usuario: ')
            senha = validar_string('Digite a senha do usuario: ')
            area = validar_string('Digite a area do usuario: ')
            acessibilidade = validar_string('Digite a acessibilidade do usuario: ')
            xp_total = validar_inteiro('Digite o xp_total do usuario: ')
            data_cadastro = validar_data('Digite a data de cadastro do usuario (DD/MM/AAAA HH:MM): ')
            
            if create_usuario(id_usuario, nome, userName, email, senha, area, acessibilidade, xp_total, data_cadastro):
                print(f'\n Usuario {nome} (ID: {id_usuario}) foi adicionado com sucesso!')
            else:
                print('\n Falha ao adicionar o usuario.')

        elif opcao == 2:
            print('\n*** Listando todos os Usuarios ***')
            usuarios = read_usuario()
            if usuarios is not None:
                if usuarios:
                    print("\n--- Lista de Usuarios ---")
                    for p in usuarios:
                        print(f"ID: {p['id_usuario']}, Nome: {p['nome']}, userName: {p['userName']}, Email: {p['email']}, Senha: {'*' * len(p['senha'])}, area: {p['area']}, acessibilidade: {p['acessibilidade']}, xp_total: {p['xp_total']}, data_cadastro: {p['data_cadastro']}")
                        print('----------------------------------')
                else:
                    print(" Nenhum usuario encontrado.")
            else:
                print(" Erro ao listar os usuarios.")

        elif opcao == 3:
            print('\n*** Atualizando um Usuario ***')
            id_usuario = validar_string('Digite o Id do Usuario que deseja atualizar: ')
            novo_nome = validar_nome('Digite o novo Nome do Usuario: ')
            novo_userName = validar_string('Digite o novo userName do Usuario: ')
            novo_email = validar_email('Digite o novo email do Usuario: ')
            nova_senha = validar_string('Digite a nova senha do Usuario:')
            nova_area = validar_string('Digite a nova area do Usuario: ')
            nova_acessibilidade = validar_string('Digite a nova acessibilidade do Usuario: ')
            novo_xp_total = validar_inteiro('Digite o novo xp_total do Usuario: ')
            nova_data_cadastro = validar_data('Digite a nova data de cadastro do Usuario (DD/MM/AAAA HH:MM): ')
            
            if update_usuario(id_usuario, novo_nome, novo_userName, novo_email, nova_senha, nova_area, nova_acessibilidade, novo_xp_total, nova_data_cadastro):
                print(f'\n Os dados do Usuario {id_usuario} foram atualizados com sucesso!')
            else:
                print(f'\n Falha ao atualizar. Nenhum Usuario com ID {id_usuario} foi encontrado ou ocorreu um erro.')

        elif opcao == 4:
            print('\n*** Excluindo um Usuario ***')
            id_usuario = validar_string('Digite o Id do Usuario que deseja excluir: ')
            if delete_usuario(id_usuario):
                print(f'\n O Usuario {id_usuario} foi excluído com sucesso!')
            else:
                print(f'\n Falha ao excluir. Nenhum Usuario com ID {id_usuario} foi encontrado ou ocorreu um erro.')
        
        elif opcao == 5:
            exportar_usuarios_json()
    
        elif opcao == 6:
            print('\nRetornando ao menu principal...')
            break
        else:
            print("\n Opção inválida. Tente novamente com um número inteiro entre 1 e 6.")

if __name__ == "__main__":
    main_usuario()