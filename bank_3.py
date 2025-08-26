
from abc import ABC, abstractmethod
import textwrap

class CLIENTE:# tem endereço e lista de contas([CLIENTE]-<possue>-(1, n)-[CONTA])
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, transacao):
        transacao.registrar()

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PESSOA_FISICA(CLIENTE):#tipo de cliente
    def __init__(self, nome, data_nascimento, cpf, endereco, senha):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.senha = senha

class CONTA:#gerencia as contas
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = HISTORICO()

    @property
    def saldo(self):#recebe nenhum argumento e retorna um float
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, numero_conta, cliente):#cria uma nova conta , retorna o objeto CONTA
        return cls(numero_conta, cliente)# cls sempre aponta para a classe que chamou o método. ou seja esse método pode ser chamado por subclasses também.

    def sacar(self, valor_saque):#implementa o saque e retorna um bool, verifica se o saque foi realizado com sucesso
        saldo_insuficiente = self._saldo < valor_saque
        if saldo_insuficiente:
            print("Saldo insuficiente.")
            return False
        elif valor_saque > 0:
            self._saldo -= valor_saque
            print("Saque realizado com sucesso.")
            return True
        else:
            print("Valor de saque inválido.")
            return False

    def depositar(self, valor_deposito):#implementa o deposito e retorna um bool, verifica se o deposito foi realizado com sucesso
        if valor_deposito > 0:
            self._saldo += valor_deposito
            print("Depósito realizado com sucesso.")
            return True
        else:
            print("Valor de depósito inválido.")
            return False

class CONTA_CORRENTE(CONTA):#tipo de conta, implementa os limites de saque
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor_saque):# sobrescreve o metodo sacar da classe CONTA (polimorfismo)
        numero_saques = len(self.historico.transacoes_saque())
        if numero_saques >= self.limite_saques:
            print("Limite de saques atingido.")
            return False
        elif valor_saque > self.limite:
            print("Valor de saque excede o limite.")
            return False
        else:
            return super().sacar(valor_saque)

class HISTORICO:# registra todo o histórico de transações por conta
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def transacoes_saque(self):
        return [t for t in self.transacoes if isinstance(t, SAQUE)]
    
    def transacoes_deposito(self):
        return [t for t in self.transacoes if isinstance(t, DEPOSITO)]

class TRANSACAO(ABC):#classe abstrata, metodo registrar
    @abstractmethod
    def registrar(self):
        pass

class SAQUE(TRANSACAO):#implementam a transação e possuem o metodo registrar
    def __init__(self, conta, valor):
        self.conta = conta
        self.valor = valor

    def registrar(self):
        if self.conta.sacar(self.valor):
            self.conta.historico.adicionar_transacao(self)
            return True
        return False

class DEPOSITO(TRANSACAO):#implementam a transação e possuem o metodo registrar
    def __init__(self, conta, valor):
        self.conta = conta
        self.valor = valor

    def registrar(self):
        if self.conta.depositar(self.valor):
            self.conta.historico.adicionar_transacao(self)
            return True
        return False

def menu1():
    menu1 = """\n
          1.\tCRIAR USUÁRIO
          2.\tCRIAR CONTA
          3.\tLISTAR CONTAS
          4.\tACESSAR CONTA
          => """
    return input(textwrap.dedent(menu1))

def menu2():

    menu2 = """\n
          1.\tEXTRATO
          2.\tSAQUE
          3.\tDEPÓSITO
          4.\tSAIR
          => """
    return input(textwrap.dedent(menu2))


def validar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criando_usuario(usuarios):
    cpf = input("Digite o CPF do usuário: ").strip()
    # verificar se o usuário já existe
    if any(usuario.cpf == cpf for usuario in usuarios):
        print("Usuário já cadastrado.")
        return

    nome = input("Digite o nome completo do usuário: ").strip()
    data_nascimento = input("Digite a data de nascimento do usuário (DD/MM/AAAA): ")
    endereco = input("Digite o endereço do usuário (logradouro, nro - bairro - cidade/sigla estado): ")
    senha = input("Digite a senha do usuário: ")

    novo_usuario = PESSOA_FISICA(nome, data_nascimento, cpf, endereco, senha)
    usuarios.append(novo_usuario)
    print("Usuário cadastrado com sucesso!")

def criando_conta(usuarios, contas):
    cpf = input("Digite o CPF do usuário: ").strip()
    verificar_senha = input("Digite sua senha: ")

    usuario = next((c for c in usuarios if c.cpf == cpf and hasattr(c, 'senha')and c.senha == verificar_senha), None)
    if usuario:
        numero_conta = len(contas) + 1
        conta = CONTA_CORRENTE(numero_conta, usuario)
        usuario.adicionar_conta(conta) # adciona conta ao cliente
        print(f"Conta criada com sucesso! Agência: {conta.agencia}, Conta: {conta.numero}")
        return conta
    else:
        print("Usuário não encontrado ou senha incorreta.")
        return None

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    for conta in contas:
        print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Usuário: {conta.cliente.nome}")

def extratos(conta):
    
    print("\n=========== EXTRATO ===========")
    print(f"Agência: {conta.agencia}")
    print(f"Conta: {conta.numero}")
    print(f"Titular: {conta.cliente.nome}")
    print("\nTransações:")
    
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            tipo = transacao.__class__.__name__
            print(f"{tipo}: R$ {transacao.valor:.2f}")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("==================\n")

def fazer_saque(conta):

    valor_saque = float(input("Digite o valor do saque: R$ "))
    saque = SAQUE(conta, valor_saque)
    conta.cliente.realizar_transacao(saque)

def fazer_deposito(conta):

    valor_deposito = float(input("Digite o valor do depósito: R$ "))
    deposito = DEPOSITO(conta, valor_deposito)
    conta.cliente.realizar_transacao(deposito)

def main():

    usuarios = []
    contas = []

    while True:
        opcao = menu1()
        if opcao == "1":
            criando_usuario(usuarios)
        elif opcao == "2":
            conta = criando_conta(usuarios, contas)
            if conta:
                contas.append(conta)
        elif opcao == "3":
            listar_contas(contas)
        elif opcao == "4":
            numero_conta = int(input("Digite o número da conta: "))
            verificar_senha = input("Digite sua senha: ")

            conta = next((c for c in contas if c.numero == numero_conta), None)
            if conta and hasattr(conta.cliente, 'senha') and conta.cliente.senha == verificar_senha:
                print("Acesso concedido.")
                while True:
                    opcao2 = menu2()
                    if opcao2 == "1":
                        extratos(conta)
                    elif opcao2 == "2":
                        fazer_saque(conta)
                    elif opcao2 == "3":
                        fazer_deposito(conta)
                    elif opcao2 == "4":
                        print("Obrigado por usar o Banco 'BOOTCAMP SUZANO'! Até logo!")
                        print("Saindo da conta...")
                        break
                    else:
                        print("Opção inválida.")
            else:
                print("Número da conta ou senha inválidos.")
main()
