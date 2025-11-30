import re

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[q] Sair

=> """
saldo = 0.0
usuarios = []
contas = []
limite = 500
extrato = []            # agora é uma lista de movimentações
numero_saques = 0
LIMITE_SAQUES = 3



def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print("Saque realizado com sucesso!")

    return saldo, extrato, numero_saques


def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def mostrar_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Saldo:", f"R$ {saldo:.2f}")
    print("Movimentações:")
    if not extrato:
        print("Nenhuma movimentação.")
    else:
        for operacao in extrato:
            print(operacao)
    print("=============================")


def limpar_cpf(cpf: str) -> str:
    """Remove caracteres não numéricos do CPF."""
    return re.sub(r'\D', '', cpf)


def criar_usuario(nome: str, data_nasc: str, endereco: str, cpf: str):
    """Cria um usuário e adiciona à lista, evitando CPFs duplicados."""
    cpf_limpo = limpar_cpf(cpf)

    for usuario in usuarios:
        if usuario["cpf"] == cpf_limpo:
            print("Erro: CPF já cadastrado!")
            return None

    usuario = {
        "nome": nome,
        "data_nasc": data_nasc,
        "endereco": endereco,
        "cpf": cpf_limpo
    }

    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    return usuario


def criar_conta_corrente(usuario):
    """Cria uma conta corrente para o usuário."""
    numero_conta = len(contas) + 1  # sequencial
    conta = {
        "agencia": "0001",
        "numero": numero_conta,
        "usuario": usuario,
        "tipo": "corrente"
    }
    contas.append(conta)
    print(f"Conta corrente criada com sucesso para {usuario}!")
    return conta


def criar_conta_poupanca(usuario):
    """Cria uma conta poupança para o usuário."""
    numero_conta = len(contas) + 1  # sequencial
    conta = {
        "agencia": "0001",
        "numero": numero_conta,
        "usuario": usuario,
        "tipo": "poupança"
    }
    contas.append(conta)
    print(f"Conta poupança criada com sucesso para {usuario}!")
    return conta


def listar_contas_usuario(usuario: str, contas: list):
    print(f"\n===== CONTAS DE {usuario} =====")
    # Filtra as contas do usuário
    contas_usuario = [conta for conta in contas if conta["usuario"] == usuario]

    if not contas_usuario:
        print("Nenhuma conta encontrada para este usuário.")
    else:
        for conta in contas_usuario:
            linha = f"Agência: {conta['agencia']} | Conta: {conta['numero']} | Tipo: {conta['tipo']}"
            print(linha)
    print("================================")


# Helpers adicionais
def encontrar_usuario_por_cpf(cpf: str):
    cpf_limpo = limpar_cpf(cpf)
    for usuario in usuarios:
        if usuario["cpf"] == cpf_limpo:
            return usuario
    return None


# Loop principal que chama as funções corretamente
if __name__ == "__main__":
    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: ").strip())
            except ValueError:
                print("Valor inválido.")
                continue
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: ").strip())
            except ValueError:
                print("Valor inválido.")
                continue
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                LIMITE_SAQUES=LIMITE_SAQUES
            )

        elif opcao == "e":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            nome = input("Nome: ").strip()
            data_nasc = input("Data de nascimento (dd/mm/aaaa): ").strip()
            endereco = input("Endereço: ").strip()
            cpf = input("CPF: ").strip()
            criar_usuario(nome, data_nasc, endereco, cpf)

        elif opcao == "nc":
            cpf = input("CPF do titular: ").strip()
            usuario = encontrar_usuario_por_cpf(cpf)
            if not usuario:
                print("Usuário não encontrado. Cadastre o usuário primeiro.")
                continue
            tipo = input("Tipo de conta (corrente/poupança) [c/p]: ").strip().lower()
            if tipo == "c":
                criar_conta_corrente(usuario["nome"])
            elif tipo == "p":
                criar_conta_poupanca(usuario["nome"])
            else:
                print("Tipo de conta inválido.")

        elif opcao == "q":
            print("Encerrando. Obrigado.")
            break

        else:
            print("Opção inválida.")
