import hashlib
import getpass
import secrets

usuarios = []
MAX_TENTATIVAS = 3
tentativas_falhas = {}

usuario_logado = None

def mostrar_menu():
    print("=" * 36)
    print("            PORTASEGURA")
    print("=" * 36)
    if usuario_logado is None:
        print("Status: você não está logado")
    else:
        print("Status: logado como " + usuario_logado)
    print("1 - Criar conta")
    print("2 - Entrar")
    print("3 - Área restrita")
    print("4 - Sair da conta")
    print("0 - Sair do programa")
    print("-" * 36)

def iniciar_sessao(nome):
    global usuario_logado                          # sem isso, criaria uma variável LOCAL
    usuario_logado = nome

def sair_da_conta():
    global usuario_logado
    if usuario_logado is None:
        print("\nVocê não está logado.\n")
    else:
        print("\nAté logo, " + usuario_logado + "! Você saiu da conta.\n")
        usuario_logado = None

def area_restrita():
        # A PROTEÇÃO FICA AQUI, dentro da função (não só no menu)
        if usuario_logado is None:
            print("\n[ACESSO NEGADO] Faça login para acessar a área restrita.\n")
            return

        pessoa = buscar_usuario(usuario_logado)
        print("\n" + "=" * 36)
        print("            ÁREA RESTRITA")
        print("=" * 36)
        print("Bem-vindo(a), " + pessoa["usuario"] + "!")
        print("E-mail da conta: " + pessoa["email"])
        print("=" * 36 + "\n")

def buscar_usuario(nome):
    for pessoa in usuarios:
        if pessoa["usuario"].lower() == nome.lower():
            return pessoa
    return None 

def login_bloqueado(nome):
    chave = nome.lower()
    if chave in tentativas_falhas:
        return tentativas_falhas[chave] >= MAX_TENTATIVAS 
    return False

def tentativas_restantes(nome):
    chave = nome.lower()
    if chave in tentativas_falhas:
        return MAX_TENTATIVAS - tentativas_falhas[chave]
    return MAX_TENTATIVAS

def registrar_falha(nome):
    chave = nome.lower()
    if chave in tentativas_falhas:
        tentativas_falhas[chave] = tentativas_falhas[chave] + 1
    else:
        tentativas_falhas[chave] = 1

def limpar_falhas(nome):
    chave = nome.lower()
    if chave in tentativas_falhas:
        tentativas_falhas[chave] = 0

def falha_de_login(nome):
    registrar_falha(nome)
    if login_bloqueado(nome):
        return (False, "Muitas tentativas. Login bloqueado até reiniciar o programa")
    restantes = tentativas_restantes(nome)
    return (False, "Usuário ou senha incorretos. Tentativas restantes: " + str(restantes))

def realizar_login(usuario, senha):
    if login_bloqueado(usuario):
        return (False, "Muitas tentativas. Login bloqueado até reiniciar o programa.")

    pessoa = buscar_usuario(usuario)

    if pessoa is None:
        # Usuário não existe: faz a mesma conta mesmo assim, para a
        # resposta demorar o mesmo tempo e não entregar que ele não existe
        proteger_senha(senha, "sal_falso")
        return falha_de_login(usuario)

    hash_digitado = proteger_senha(senha, pessoa["sal"])

    if hash_digitado == pessoa["senha"]:
        limpar_falhas(usuario)
        return (True, "Login realizado com sucesso.")

    return falha_de_login(usuario)

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
        print("\n[ERRO] " + mensagem + "\n")

def entrar():
    if usuario_logado is not None:
        print("\nVocê já está logado como " + usuario_logado + ". Use a opção 4 para sair.\n")
        return

    print("\n--- Login (Enter vazio no usuário para voltar) ---")
    while True:
        usuario = input("Usuário: ").strip()
        if campo_vazio(usuario):
            print("\nVoltando ao menu.\n")
            return

        senha = getpass.getpass("Senha (não aparece na tela): ")
        ok, mensagem = realizar_login(usuario, senha)

        if ok:
           pessoa = buscar_usuario(usuario)
           iniciar_sessao(pessoa["usuario"])         # NOVO: abre a sessão
           print("\n[OK] " + mensagem + " Bem-vindo(a), " + usuario_logado + "!\n")
           return


        print("\n[ERRO] " + mensagem + "\n")
        if login_bloqueado(usuario):
            return

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
    usuarios.append(novo_usuario)

def main():
    opcao = ""
    while opcao != "0":
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_conta()
        elif opcao == "2":
            entrar()
        elif opcao == "3":
            area_restrita()
        elif opcao == "4":
            sair_da_conta()
        elif opcao == "0":
            print("\nAté logo!")
        else:
            print("\nOpção inválida. Digite 1, 2, 3, 4 ou 0.\n")

main()