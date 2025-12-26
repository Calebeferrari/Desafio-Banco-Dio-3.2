from datetime import datetime
from pathlib import Path # Lê arquivos de uma pasta como se fosse uma lista
import csv
import os
import re # Regex(Expressão regulares) - Usado para ler caracteres específicos.
import tempfile # Necessário para criação de arquivos temporários


# Classe Cliente
class Cliente:
    def __init__(self, nome, cpf, nascimento):
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.contas = []
    
    def __str__(self):
        return f'Nome: {self.nome}\nCPF: {self.cpf}\nNascimento: {self.nascimento}\nIdade: {self.idade}\nContas: {self.visualizacao_contas_vinculadas}'
    
    # Calculando idade - criar uo atributo idade a partir de nascimento
    @property
    def idade(self):
        # Converter data em objeto tipo date
        data_objeto = datetime.strptime(self.nascimento, "%d/%m/%Y").date()

        # Calculo de idade
        idade = datetime.today().year - data_objeto.year

        # Verificando se já fez aniversário
        if (datetime.today().month, datetime.today().day) < (data_objeto.month, data_objeto.day):
            idade -= 1
        return idade
    
    # Formatação de cpf
    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, cpf_informado):
        cpf_convertion = str(cpf_informado)[:3] + '.' + str(cpf_informado)[3:6] + '.' + str(cpf_informado)[6:9] + '-' + str(cpf_informado)[9:11]
        self._cpf = cpf_convertion

    
    # Vinculação de conta a cliente
    def vincular_conta(self, conta_unica):
        self.contas.append(conta_unica)

    
    # Visualização de informações de contas vinculadas
    @property
    def visualizacao_contas_vinculadas(self):
        if self.contas != []:
            contas_ = ''
            for conta_vis in self.contas:
                contas_ += str(f'\n{conta_vis}')

            return contas_
        else:
            return f'Não há constas vinculadas.'


# Classe Conta
class Conta:

    def __init__(self):
        self.agencia = int(1)
        self.conta = int(self.gerenciador_conta()) + 1
        self.saldo = 0
        self.extrato = []
        self.limite_transacao_diaria = 3
    
    def __str__(self):
        return f'Agência: {self.agencia:03} - N° Conta: {self.conta:04}'
    
    def deposito(self, valor):

        # Condição p/ limite diário de transações
        if self.limite_transacao() == 0:
            return f'limite'
        
        # Atualização de saldo
        self.saldo += valor
        # Armazenando informações de transação p/ extrato
        self.extrato.append(self.transacao_formatada(valor, 'deposito'))

        return self.saldo
    
    def saque(self, valor):
        # Condição p/ saque.
        if self.saldo <= 0 or self.saldo < valor:
            return False
        
        elif self.limite_transacao() == 0:
            return f'limite'
        
        else:
            # Atualização de saldo
            self.saldo -= valor
            # Armazenando informações de transação p/ extrato
            self.extrato.append(self.transacao_formatada(valor, 'saque'))

            return self.saldo
 
    def extrato_bancario(self):
        '''
        Exibição das informações do extrato em formato de str.
        '''

        # Variável que conterá informação de extrato
        info_extrato = ''
        # Ciclo que organiza informações de extrato
        for pos, valor in enumerate(self.extrato):
            for key, value in valor.items():
                info_extrato +=  f'{key}: {value}\n'
            info_extrato += '\n'
        
        # Retorno de informações de extrato - Caso não haja nenhum
        if info_extrato == '':
            return f'Nenhuma transação efetuada.'
        # Retorno de informações de extrato - Caso haja informações
        else:
            return info_extrato

    #@staticmethod
    def transacao_formatada(self, valor_transacao, tipo_transacao, data_formatada=None, data_carregamento=True):
        '''
        valor_transacao: Recebe o valor da transação.
        tipo_transacao: Recebe o tipo da transação, que pode ser 'deposito' ou 'saque'.
        data_formatada: Recebe a data da transação em caso de carregamento pelo arquivo salvo.
        data_carregamento: True é o valor padrão para execução do usuário. Falso é usado para o carregamento das informações vindas do arquivo de dados salvos.
        '''

        # Criando data da transação bancária
        if data_carregamento == True:
            data_transacao = datetime.today()
            data_formatada = data_transacao.strftime("%d/%m/%Y - %H:%M:%S")


        # Formatar saída de valores monetários.
        valor_formatado = str(f'{valor_transacao:.2f}').replace('.', ',')
        saldo_formatado = str(f'{self.saldo:.2f}').replace('.', ',')

        # Dicionário que armazena as informações da transação bancária
        info_transacao = {}
        # Condições para definir o tipo da transação em um valor str
        if tipo_transacao == 'deposito':
            info_transacao['Depósito'] = f'R${valor_formatado}'

        elif tipo_transacao == 'saque':
            info_transacao['Saque'] = f'R${valor_formatado}'

        # Atribuindo valores str para itens de dicionário de transações
        info_transacao['Data'] = data_formatada
        info_transacao['Saldo'] = f'R${saldo_formatado}'

        return info_transacao
  
    def limite_transacao(self):
        # Declaração de data
        data_hoje = datetime.now().date().strftime("%d/%m/%Y")
        # Declaração de quantidade de transações liberadas
        transacoes_diarias = self.limite_transacao_diaria

        for pos, i in enumerate(self.extrato):
            if self.extrato[pos]['Data'].startswith(data_hoje):
                transacoes_diarias -= 1
        
        return transacoes_diarias

    def gerenciador_conta(self):

        lista_geral_contas = []
        lista_conta_max = []

        with open('save_data.csv', 'r', encoding='utf-8', newline="") as arquivo:
            
            leitor = csv.reader(arquivo, delimiter=';')

            # Armazena valores de agência e contas em lista_geral
            for cad in leitor:
                for cont in cad[3:]:
                    lista_geral_contas.append(cont)
            
            # Extrae apenas valores de contas para lista_conta
            for conta_cad in range(1, len(lista_geral_contas), 2):
                lista_conta_max.append(lista_geral_contas[conta_cad])

            # Se lista estiver vázia ele retornará valor mínimo para criação de novas contas
            if lista_conta_max:
                valor_max = int(max(lista_conta_max))
            else:
                valor_max = 0
            
        return valor_max

# Classe Lista geral de cadastros
class Lista_Geral:
    def __init__(self):
        self.lista_clientes = []

    
    def adicionar_cadastros(self, cadastro_cliente):
        self.lista_clientes.append(cadastro_cliente)
    
    
    def excluir_cadastro(self, posicao_cadastro):
        del self.lista_clientes[posicao_cadastro]
    

    def organizar_lista(self, lista_cadastros):
        lista_ordenada = sorted(lista_cadastros, key=lambda cliente:cliente.nome)
        self.lista_clientes = lista_ordenada

    
    def visualizar_cadastros(self):
        # Informa o cabeçalho da lista
        print_visualizacao = f'{'Pos.':03} {'Cliente':^31} {'CPF':^11}\n'+'-'*50+'\n'

        for pos, cadastro in enumerate(self.lista_clientes, 1):
            # Mostra resultados da lista formatados
            print_visualizacao += f'{pos:03} {cadastro.nome[:31]:31} {cadastro.cpf}\n'
        
        return print_visualizacao
    
    
    def validacao_cpf(self, cpf_informado):
        # Validador de cpf
        validador_cpf = True

        # Ciclo p/ verificar se cpf já existe
        for pos, cpf in enumerate(self.lista_clientes):
            if cpf_informado == cpf.cpf:
                validador_cpf = False

        return validador_cpf

    # Funções relativas ao salvamento e carregamento de informações arquivadas.

    def salvar_arquivo_cadastro(self, info_nome, info_cpf, info_nascimento):
        # Criar e salvar em arquivo csv
        with open('save_data.csv', 'a+', encoding='utf-8', newline='') as save_arquivo:
            
            escritor = csv.writer(save_arquivo, delimiter=';')

            escritor.writerow([info_nome, info_cpf, info_nascimento])

    
    def carregar_arquivo_cadastros(self):

        with open('save_data.csv', 'r', encoding='utf-8', newline='') as save_arquivo:

            leitor = list(csv.reader(save_arquivo, delimiter=';'))

            # Carregar informações no sistema
            for info_cadastro in leitor:
                # Desempacotando informações salvas
                nome, cpf, nascimento = info_cadastro[0:3]
                # Adicionando informações cadastrais em classe Cliente
                cadastro = Cliente(nome, cpf, nascimento)

                # Carregar informações de contas salvas na classe Cliente, caso as tenha.
                if not info_cadastro[3:]:
                    pass
                else:
                    # Ciclo que percorrerá a lista de possíveis contas cadastradas
                    for posicao_conta in range(3, len(info_cadastro), 2):
                        # Variável local que conterá as informações da classe Conta
                        info_conta = Conta()
                        # Carregar contas cadastradas
                        info_conta.agencia = int(info_cadastro[posicao_conta])
                        info_conta.conta = int(info_cadastro[posicao_conta+1])

                        # Vinculando conta a lista de contas da classe Cliente
                        cadastro.vincular_conta(info_conta)

                        # LEITURA DE ARQUIVOS DE CONTAS SALVAS
                        # Transforma a pasta de arquivos em uma lista que pode ser lida em um ciclo
                        pasta_arquivos = Path('contas_salvas')

                        # Ciclo de leitura dos arquivos presentes na pasta(contas_salvas)
                        for linha_arquivo in pasta_arquivos.glob('*.csv'):
                        
                            # Convertendo o nome do arquvio em um str que lê - via regex - somente os números.
                            nome_arquivo = re.findall(r'\d+', linha_arquivo.name)

                            if int(nome_arquivo[0]) == int(info_conta.agencia) and int(nome_arquivo[1]) == int(info_conta.conta):

                                # Leitura convencional de um arquivo salvo
                                with open(linha_arquivo, 'r', encoding='utf-8', newline='') as arquivo_salvo:
                                
                                    leitor_arquivo = csv.reader(arquivo_salvo, delimiter=';')

                                    # Ciclo de leitura do arquivo com as transações
                                    for linha_conta in leitor_arquivo:

                                        # Atribuição de valores de Saldo
                                        info_conta.saldo = float(linha_conta[3])

                                        # Atribuição de valores de Extrato
                                        info_transacoes = info_conta.transacao_formatada(float(linha_conta[2]), str(linha_conta[1]), str(linha_conta[4]), False)
                                        info_conta.extrato.append(info_transacoes)

                            else:
                                pass

                # Adicionando cadastro de cliente na Lista_Geral
                self.lista_clientes.append(cadastro)


    def carregar_arquivos_contas(self):

        import re # Regex(Expressão regulares) - Usado para ler caracteres específicos.

        # Transforma a pasta de arquivos em uma lista que pode ser lida em um ciclo
        pasta_arquivos = Path('contas_salvas')

        # Ciclo de leitura dos arquivos presentes na pasta(contas_salvas)
        for linha_arquivo in pasta_arquivos.glob('*.csv'):

            # Convertendo o nome do arquvio em um str que lê - via regex - somente os números.
            nome_arquivo = re.findall(r'\d+', linha_arquivo.name)
            print(linha_arquivo.name)
            print(f'ag: {nome_arquivo[0]} - conta:{nome_arquivo[1]}')

            # Leitura convencional de um arquivo salvo
            with open(linha_arquivo, 'r', encoding='utf-8', newline='') as arquivo_salvo:

                leitor_arquivo = csv.reader(arquivo_salvo, delimiter=';')

                for linha_conta in leitor_arquivo:
                    print(linha_conta)

                
                print()

        # Carregamento de arquivos

        # Ciclo de leitura dos arquivos presentes na pasta(contas_salvas)
        for linha_arquivo in pasta_arquivos.glob('*.csv'):

            # Criação de obejtos Contas para carregamento
            conta_carregar = Conta()

            # Convertendo o nome do arquvio em um str que lê - via regex - somente os números.
            nome_arquivo = re.findall(r'\d+', linha_arquivo.name)

            # Atribuindo valores da conta
            conta_carregar.agencia = int(nome_arquivo[0])
            conta_carregar.conta = int(nome_arquivo[1])

            # Leitura convencional de um arquivo salvo
            with open(linha_arquivo, 'r', encoding='utf-8', newline='') as arquivo_salvo:

                leitor_arquivo = csv.reader(arquivo_salvo, delimiter=';')

                # Ciclo de leitura do arquivo com as transações
                for linha_conta in leitor_arquivo:
                    
                    # Atribuição de valores de transações
                    conta_carregar.limite_transacao_diaria = int(linha_conta[0])
                    conta_carregar.transacao_formatada(float(linha_conta[2]), str(linha_conta[1]))


    def atualizar_arquivo_cadastro(self,posicao_cadastro, posicao_agencia, posicao_conta):

        '''
        Função utilizada para atualizar cadastro sobre o adicionamento de nova conta.
        '''
        # Adiciona as informações da conta vinculada ao arquivo local de cadastros.
        with open ('save_data.csv', 'r', encoding='utf-8', newline='') as save_arquivo:

            # Criação de arquivo de leitura dos dados salvos
            leitor = list(csv.reader(save_arquivo, delimiter=';'))
            # Criação de arquivo que conterá os dados em ordem alfabetica
            leitor_ordenado = list(leitor)
            # Ordenando em ordem alfabética
            leitor_ordenado.sort()
            # Adicionando ao arquivo ordenado a informação de Agência
            leitor_ordenado[posicao_cadastro].append(posicao_agencia)
            # Adicionando ao arquivo ordenado a informação de Conta
            leitor_ordenado[posicao_cadastro].append(posicao_conta)

        # Salva as informações do cadastro atualizado no arquivo de save
        '''
        Lembrando que essa atualização requer a limpeza das informações anteriores para
        a conseguinte subescrição das novas informações.
        '''
        with open ('save_data.csv', 'w', encoding='utf-8', newline='') as save_arquivo:

            escritor = csv.writer(save_arquivo, delimiter=';')
            # Salvando as informações atualizadas em arquivo de salvamento
            for linha_cadastro in leitor_ordenado:
                escritor.writerow(linha_cadastro)
        
        # Criação de arquivos indivíduais para cada conta criada

        # Regula a criação da pasta onde será armazenado as informações de cada conta e evita que outro arquivo da mesma conta seja criado novamente.
        os.makedirs('contas_salvas', exist_ok=True)

         # Save exclusivo para cada conta criada.
        with open (f'contas_salvas/agencia_{int(posicao_agencia)}_conta_{int(posicao_conta)}.csv', 'a+', encoding='utf-8', newline='') as arquivo:
            pass

                
    def atualizar_arquivo_conta(self, info_agencia, info_conta, info_trans_diaria=0, info_tipo=0, info_valor=0, info_saldo=0, info_data=0):
        '''
        info_agencia: Número da agência.
        info_conta: Número da conta.
        info_trans_diaria: Qtd. de transações permitidas durante o dia.
        info_tipo: Tipo de transação - Depósito ou Saque.
        info_valor: Valor da transação.
        info_saldo: Saldo em conta.
        info_data: Data da transação.
        
        '''

        with open (f'contas_salvas/agencia_{int(info_agencia)}_conta_{int(info_conta)}.csv', 'a+', encoding='utf-8', newline='') as arquivo:
            
            escritor = csv.writer(arquivo, delimiter=';')

            escritor.writerow([info_trans_diaria, info_tipo, info_valor, info_saldo, info_data])
            

    def atualizar_arquivo_clientes(self, posicao_modificacao, campo_modificacao, atualizacao_mofificacao, deletar_conta = False):
        '''
        Função responsável por atualizar alterações realizadas nos dados pessoais do cliente.
        
        posicao_modificacao: Recebe a posição do campo a ser alterado na lista geral.
        campo_modificacao: O tipo do campo a ser modificado. Nome, CPF ou Data de nascimento.
        atualizacao_mofificacao: Novo item atualizado.
        deletar_conta: Se True assionará a condicional exclusão de cadastro selecionado. Se False apenas excluirá o campo selecionado.
        '''

        # Condicional para excluir campo selecionado
        if deletar_conta == False:

            with open('save_data.csv', 'r', encoding='utf-8', newline='') as arquivo_r:

                leitor_arquivo = list(csv.reader(arquivo_r, delimiter=';'))
                
                # Ordenando leitor em ordem alfabética
                leitor_arquivo.sort()

                # Modificação de campo selecionado
                leitor_arquivo[posicao_modificacao][campo_modificacao-1] = atualizacao_mofificacao

                # Definindo variável que será utilizada para localizar posição de cliente a partir de CPF
                id_cpf = leitor_arquivo[posicao_modificacao][1]

                # Ordenando dados de arquivo em ordem alfabetica
                leitor_arquivo.sort()

                # Definindo nova posição de cliente modificado em lista geral
                for nova_posicao, info_cliente in enumerate(leitor_arquivo):
                    if int(id_cpf) == int(info_cliente[1]):
                        posicao_modificacao = nova_posicao
                        break

            # Abertura de novo arquivo temporário
            with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8',newline='' ,dir='.') as arquivo_temporario:
            
                escritor = csv.writer(arquivo_temporario, delimiter=';')

                for linha in leitor_arquivo:
                    escritor.writerow(linha)


            os.replace(arquivo_temporario.name, 'save_data.csv')

            return posicao_modificacao

        # Condicional para excluir cadastro
        elif deletar_conta == True:
            with open('save_data.csv', 'r', encoding='utf-8', newline='') as arquivo_r:

                leitor_arquivo = list(csv.reader(arquivo_r, delimiter=';'))
                
                # Ordenando leitor em ordem alfabética
                leitor_arquivo.sort()

                # Armazenamento de valores de agências e contas vinculadas a cadastro para suas respectivas exclusões
                if leitor_arquivo[posicao_modificacao][3:]:
                    lista_contas = leitor_arquivo[posicao_modificacao][3:]
                else:
                    lista_contas = []

                # Modificação de campo selecionado
                del leitor_arquivo[posicao_modificacao]

                # Ordenando dados de arquivo em ordem alfabetica
                leitor_arquivo.sort()

            # Abertura de novo arquivo temporário
            with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8',newline='' ,dir='.') as arquivo_temporario:
            
                escritor = csv.writer(arquivo_temporario, delimiter=';')

                for linha in leitor_arquivo:
                    escritor.writerow(linha)


            os.replace(arquivo_temporario.name, 'save_data.csv')

            # Exclusão de contas vinculadas
            if lista_contas:

                # Variável para leitura de arquivos armazenados em formato de lista
                pasta_contas = Path('contas_salvas')

                # Lista de contas a serem excluídas
                lista_excluir = list()

                # Leitura de lista de arquivos em pasta
                for linha_conta in pasta_contas.glob('*.csv'):

                    # Regex - Encontra apenas o valores numéricos presentes no nome da pasta
                    numero_agencia_conta = re.findall(r'\d+', str(linha_conta))

                    # Condicional para identificar conta a ser excluída:
                    for pos in range(0, len(lista_contas),2):

                        if int(lista_contas[pos]) == int(numero_agencia_conta[0]) and int(lista_contas[pos+1]) == int(numero_agencia_conta[1]):
                            lista_excluir.append(f'contas_salvas/agencia_{lista_contas[pos]}_conta_{lista_contas[pos+1]}.csv')

                # Exclusão de listas selecionadas
                range_lista = len(lista_excluir)
                for i in range(range_lista):
                    if os.path.exists(lista_excluir[i]):
                        os.remove(lista_excluir[i])
                
                else:
                    pass
            

            return posicao_modificacao

#------------------------------------------------------------
if __name__ == "__main__":

    p1 = Cliente('Tay',12312312310, '01/11/1990')
    p2 = Cliente('Fer',12312312311, '06/04/1989')
    p3 = Cliente('Jan',12312312312, '20/01/1997')
    p4 = Cliente('Anf',12312312313, '15/11/1991')

    conta01 = Conta()
    conta02 = Conta()

    lista_teste = Lista_Geral()
    lista_teste.adicionar_cadastros(p1)
    lista_teste.adicionar_cadastros(p2)
    lista_teste.adicionar_cadastros(p3)
    lista_teste.adicionar_cadastros(p4)

    lista_teste.organizar_lista(lista_teste.lista_clientes)

    p4.vincular_conta(conta02)


    #conta02.saldo
    conta02.deposito(200)
    conta02.deposito(300)
    conta02.deposito(500)


    print(conta02.limite_transacao())

    #for cadastro in list(lista_teste.lista_clientes):
    #    print(cadastro)
    #    print()