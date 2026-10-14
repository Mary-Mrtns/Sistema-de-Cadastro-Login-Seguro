# Lista global: cada usuário será um dicionário, por exemplo:
# {"usuario": "mary", "email": "mary@email.com", "senha": "..."}
# Atenção: os dados ficam só na memória e somem quando o programa fecha.
usuarios = []

def mostrar_menu():
    print("=" * 36)
    print("            PORTASEGURA")
    print("=" * 36)
    print("1 - Criar conta")
    print("2 - Entrar")
    print("0 - Sair do programa")
    print("-" * 36)

def campo_vazio(texto):
    # strip() remove espaços; se sobrar nada, o campo está vazio
    return texto.strip() == ""

def validar_senha(senha):
    # Regra 1: mínimo de 8 caracteres
    if len(senha) < 8:
        return (False, "A senha precisa ter pelo menos 8 caracteres.")

    # Regra 2: pelo menos uma letra e pelo menos um número
    tem_letra = False
    tem_numero = False
    for caractere in senha:
        if caractere.isalpha():
            tem_letra = True
        if caractere.isdigit():
            tem_numero = True

    if not tem_letra:
        return (False, "A senha precisa ter pelo menos uma letra.")
    if not tem_numero:
        return(False, "A senha precisa ter pelo menos um número.")

    return (True, "Senha válida")

def criar_conta():
    print("\n[Cadastro] Ainda será feito\n")

def entrar():
    print("\n[Login] Ainda será feito\n")

def main():
    opcao = ""
    while opcao != "0":
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip

        if opcao == "1":
            criar_conta()
        elif opcao == "2":
            entrar()
        elif opcao == "0":
            print("\nAté logo!")
        else:
            print("\nOpção inválida. Digite 1, 2 ou 0.\n")

main()