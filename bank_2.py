from datetime import datetime
import textwrap

def MENU1():
    menu1 = """\n
          1.\tACESSAR CONTA
          2.\tCRIAR CONTA
          3.\tCRIAR USUÁRIO
          4.\tLISTAR CONTAS
          => """
    return input(textwrap.dedent(menu1))

def MENU2():
    menu2 = """\n
          1.\tEXTRATO
          2.\tSAQUE
          3.\tDEPÓSITO
          4.\tSAIR
          => """
    return input(textwrap.dedent(menu2))

def EXTRATO(saldo, /, *, extrato):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("\n=========== EXTRATO ===========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nData/Hora: {agora}")
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=====================================")

def SAQUE(*, saldo, extrato, agora, saques_dia):

    hoje = datetime.now().date()
    saques_hoje = [dia for dia in saques_dia if dia == hoje]

    if len(saques_hoje) >= 3:
        print("\nVocê já atingiu o limite de 3 saques diários.")
        return saldo, extrato, saques_dia

    valor_saque = float(input("Digite o valor do saque: R$ "))
    if valor_saque > 500:
        print("\nLimite de saque é R$ 500,00.")
    elif valor_saque > saldo:
        print("\nSaldo insuficiente.")
    else:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        saldo -= valor_saque
        extrato += f"Saque: R$ {valor_saque:.2f} às {agora}\n"
        saques_dia.append(hoje)
        print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
    return saldo, extrato, saques_dia

def DEPOSITO(saldo, extrato, /):

    valor_deposito = float(input("Digite o valor do depósito: R$ "))
    if valor_deposito < 0:
        print("\nValor de depósito inválido.")
    else:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        saldo += valor_deposito
        extrato += f"Depósito:\tR$ {valor_deposito:.2f} às {agora}\n"
        print(f"\nDepósito de R$ {valor_deposito:.2f} realizado com sucesso.")
    return saldo, extrato

def CRIANDO_USUARIO(usuarios):
    cpf = input("Digite o CPF do usuário: ").strip()
    usuario = VALIDAR_USUARIO(cpf, usuarios)

    if usuario:
        print("Usuário já cadastrado.")
        return

    nome = input("Digite o nome completo do usuário: ").strip()
    data_nascimento = input("Digite a data de nascimento do usuário (DD/MM/AAAA): ")
    endereco = input("Digite o endereço do usuário (logradouro, nro - bairro - cidade/sigla estado): ")
    senha = input("Digite a senha do usuário: ")

    usuarios.append({
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "senha": senha
    })
    print("Usuário cadastrado com sucesso!")

def VALIDAR_USUARIO(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def CRIANDO_CONTA(AGENCIA, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuário: ").strip()
    usuario = VALIDAR_USUARIO(cpf, usuarios)

    if usuario:
        conta = {
            "agencia": AGENCIA,
            "numero_conta": numero_conta,
            "usuario": usuario
        }
        print(f"Conta criada com sucesso! Agência: {AGENCIA}, Conta: {numero_conta}")
        return conta
    else:
        print("Usuário não encontrado.")
        return None

def LISTANDO_CONTAS(contas):
    for conta in contas:
        linha = f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Usuário: {conta['usuario']['nome']}"
        print(textwrap.dedent(linha))

def MAIN():
    AGENCIA = "0001"
    saldo = 0.0
    extrato = ""
    saques_dia = []
    usuarios = []
    contas = []

    print("\nBem-vindo ao Banco 'BOOTCAMP SUZANO'!!!")

    while True:
        opcao1 = MENU1()

        if opcao1 == "1":
            verificar_numero = int(input("Digite o número da conta: "))
            verificar_senha = input("Digite sua senha: ")
            conta = next((c for c in contas if c['numero_conta'] == verificar_numero), None)
            if not usuarios or not contas:
                print("Nenhuma conta ou usuário encontrado. Por favor, crie uma conta primeiro.")
                continue
            elif conta and conta['usuario']['senha'] == verificar_senha:
                print("Acesso concedido.")
                while True:
                    opcao2 = MENU2()
                    if opcao2 == "1":
                        EXTRATO(saldo, extrato=extrato)
                    elif opcao2 == "2":
                        saldo, extrato, saques_dia = SAQUE(
                        saldo=saldo,
                        extrato=extrato,
                        saques_dia=saques_dia
                        )
                    elif opcao2 == "3":
                        saldo, extrato = DEPOSITO(saldo, extrato)
                    elif opcao2 == "4":
                        print("SAINDO...")
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
            else:
                print("Número da conta ou senha inválidos.")
                continue
        elif opcao1 == "2":
            numero_conta = len(contas) + 1
            conta = CRIANDO_CONTA(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao1 == "3":
            CRIANDO_USUARIO(usuarios)
        elif opcao1 == "4":
            LISTANDO_CONTAS(contas)

MAIN()
print("Obrigado por usar o Banco 'BOOTCAMP SUZANO'! Até logo!")
