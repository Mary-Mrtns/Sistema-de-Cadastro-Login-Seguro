# PortaSegura 🛡️

**PortaSegura** é um sistema de autenticação e gerenciamento de usuários em linha de comando (CLI) desenvolvido em Python, com foco em boas práticas de segurança da informação e armazenamento seguro de credenciais.

---

## Funcionalidades

- **Cadastro de Usuários**: Validação de campos obrigatórios, verificação de duplicidade de usuário e e-mail.
- **Validação de Senhas Fortes**:
  - Mínimo de 8 caracteres.
  - Exigência de pelo menos uma letra e um número.
  - Confirmação de senha no cadastro.
- **Armazenamento Seguro (Hashing & Salting)**:
  - Utilização do algoritmo **PBKDF2-HMAC-SHA256** com **600.000 iterações** (em conformidade com as recomendações da OWASP).
  - Gerador de *salt* criptograficamente seguro por usuário (`secrets.token_hex`).
  - Nenhuma senha é armazenada em texto puro.
- **Proteção Contra Ataques**:
  - **Bloqueio por Força Bruta**: Bloqueia a conta temporariamente após 3 tentativas malsucedidas de login.
  - **Mitigação de Timing Attack**: Executa o processo de hashing simulado mesmo para usuários inexistentes, garantindo tempo de resposta constante e impedindo enumeração de contas via análise de latência.
- **Privacidade de Entrada**: Entradas de senha ocultas no terminal utilizando a biblioteca nativa `getpass`.
- **Área Restrita**: Proteção baseada em estado de sessão logada.

---

## Tecnologias Utilizadas

- **Python 3.x**
- Módulos nativos da biblioteca padrão:
  - `hashlib` (derivação de chave de segurança PBKDF2)
  - `secrets` (geração de salts criptográficos)
  - `getpass` (mascaramento de entrada de senha)

---

## ⚙️ Como Executar

### Pré-requisitos
- Python 3.7 ou superior instalado.

### Passos
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/portasegura.git
   cd portasegura
   ```

2. Execute o arquivo principal:
   ```bash
   python main.py
   ```

---

## 📁 Estrutura do Código

| Função | Descrição |
| :--- | :--- |
| `cadastrar_usuario` | Gera o salt único e armazena o hash derivado da senha. |
| `proteger_senha` | Aplica PBKDF2-HMAC-SHA256 com 600k iterações. |
| `realizar_login` | Valida credenciais e gerencia a lógica de mitigação contra ataques temporais. |
| `login_bloqueado` | Verifica o limite de 3 falhas de login. |
| `area_restrita` | Exibe dados protegidos apenas se houver sessão ativa. |

---

## 📄 Licença

Este projeto é de uso livre para fins acadêmicos e de aprendizado.