from datetime import datetime

def EXTRATO(saldo, extrato):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("=== EXTRATO ===")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Data/Hora: {agora}")
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("================")

def SAQUE(saldo, extrato, agora, saques_dia):

    hoje = datetime.now().date()
    saques_hoje = [dia for dia in saques_dia if dia == hoje]

    if len(saques_hoje) >= 3:
        print("Você já atingiu o limite de 3 saques diários.")
        return saldo, extrato, saques_dia

    valor_saque = float(input("Digite o valor do saque: R$ "))
    if valor_saque > 500:
        print("Limite de saque é R$ 500,00.")
    elif valor_saque > saldo:
        print("Saldo insuficiente.")
    else:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        saldo -= valor_saque
        extrato += f"Saque: R$ {valor_saque:.2f} às {agora}\n"
        saques_dia.append(hoje)
        print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
    return saldo, extrato, saques_dia

def DEPOSITO(saldo, extrato, agora):

    valor_deposito = float(input("Digite o valor do depósito: R$ "))
    if valor_deposito < 0:
        print("Valor de depósito inválido.")
    else:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        saldo += valor_deposito
        extrato += f"Depósito: R$ {valor_deposito:.2f} às {agora}\n"
        print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso.")
    return saldo, extrato

saldo = 0.0
extrato = ""
saques_dia = []

print("Bem-vindo ao Banco 'BOOTCAMP SUZANO'!!!")

while True:
    print("""
          1. EXTRATO
          2. SAQUE
          3. DEPÓSITO
          4. SAIR
          """)
    opcao = int(input("Digite a opção desejada: "))

    if opcao == 1:
        print("Você escolheu a opção 1: EXTRATO")
        print(EXTRATO(saldo, extrato))
    elif opcao == 2:
        print("Você escolheu a opção 2: SAQUE")
        saldo, extrato, saques_dia = SAQUE(saldo, extrato, saques_dia)
    elif opcao == 3:
        print("Você escolheu a opção 3: DEPÓSITO")
        saldo, extrato = DEPOSITO(saldo, extrato)
    elif opcao == 4:
        print("Você escolheu a opção 4: SAIR")
        break
    else:
        print("Opção inválida. Tente novamente.")

print("Obrigado por usar o Banco 'BOOTCAMP SUZANO'! Até logo!")
