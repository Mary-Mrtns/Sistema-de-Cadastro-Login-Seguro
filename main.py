import hashlib
import getpass
import secrets

usuarios = []

def mostrar_menu():
    print("=" * 36)
    print("            PORTASEGURA")
    print("=" * 36)
    print("1 - Criar conta")
    print("2 - Entrar")
    print("0 - Sair do programa")
    print("-" * 36)

def usuario_existe(usuario):
    for pessoa in usuarios:
        if pessoa["usuario"].lower() == usuario.lower():
            return True      # achou: encerra a função na hora
    return False             # só chega aqui se o for terminou sem achar

def email_existe(email):
    for pessoa in usuarios:
        if pessoa["email"].lower() == email.lower():
            return True
    return False

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

def validar_cadastro(usuario, email, senha, confirmacao):
    # Regra: nenhum campo pode ficar vazio
    if (campo_vazio(usuario) or campo_vazio(email)
            or campo_vazio(senha) or campo_vazio(confirmacao)):
        return (False, "Preencha todos os campos.")

    if usuario_existe(usuario):
        return (False, "Esse nome de usuário já está em uso.")
    if email_existe(email):
        return (False, "Esse e-mail já está cadastrado.")

    # Regra: a senha precisa atender aos critérios
    senha_ok, mensagem = validar_senha(senha)
    if not senha_ok:
        return (False, mensagem)

    # Regra: a confirmação precisa ser igual à senha
    if senha != confirmacao:
        return (False, "A confirmação não é igual à senha.")

    return (True, "Dados válidos.")        

def criar_conta():
    print("\n--- Cadastro ---")
    usuario = input("Nome de usuário: ").strip()
    email = input("E-mail: ").strip()
    senha = getpass.getpass("Senha (não aparece na tela): ")
    confirmacao = getpass.getpass("Confirme a senha: ")

    valido, mensagem = validar_cadastro(usuario, email, senha, confirmacao)

    if valido:
        cadastrar_usuario(usuario, email, senha)
        print("\n[OK] Conta criada com sucesso!\n")
    else:
        print("\n[ERRO]" + mensagem + "\n")

def entrar():
    print("\n[Login] Ainda será feito\n")

def proteger_senha(senha, sal):
    # .encode() converte texto em bytes, que é o que o hashlib exige
    resultado = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        sal.encode("utf-8"),
        600000
    )
    # .hex() transforma o resultado em texto legível (64 caracteres)
    return resultado.hex()

def cadastrar_usuario(usuario, email, senha):
    sal = secrets.token_hex(16)                   # sal aleatório e único
    senha_protegida = proteger_senha(senha, sal)

    novo_usuario = {
        "usuario": usuario,
        "email": email,
        "senha": senha_protegida,                  # NUNCA a senha original
        "sal": sal
    }
    usuario.append(novo_usuario)

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