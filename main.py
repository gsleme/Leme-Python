from usuarios import main_usuario
from trilhas import main_trilha
from modulos import main_modulo
from progressos import main_progresso
from sugestoes import main_sugestao
from previsoes import main_previsao
from utilitarios import validar_inteiro

def exibir_menu():
    """Exibe as opções do menu principal."""
    print("\n" + "="*40)
    print("==== Sistema de Gerenciamento de Aprendizagem ====")
    print("="*40)
    print("1.  Gerenciar Usuarios.")
    print("2.  Gerenciar Trilhas.")
    print("3.  Gerenciar Modulos.")
    print("4.  Gerenciar Progressos.")
    print("5.  Gerenciar Sugestoes.")
    print("6.  Gerenciar Previsoes.")
    print("0. Sair: Encerra o Sistema.")
    print("="*40)

def main():
    while True:
        exibir_menu()
        
        opcao = validar_inteiro("Escolha uma opção de 0 a 6: ")

        if opcao == 1:
            main_usuario()
        elif opcao == 2:
            main_trilha()
        elif opcao == 3:
            main_modulo()
        elif opcao == 4:
            main_progresso()
        elif opcao == 5:
            main_sugestao()
        elif opcao == 6:
            main_previsao()
        elif opcao == 0:
            print("\nEncerrando o sistema... até logo!")
            break
        else:
            print("\nOpção inválida. Tente novamente com um número inteiro entre 0 e 6.")


if __name__ == "__main__":
    main()