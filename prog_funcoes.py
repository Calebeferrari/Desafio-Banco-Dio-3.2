from prog_interface import*
from prog_class import*

lista_correcao = Lista_Geral()

# Função responsável por pesquisar cadastro
def pesquisar_cadastro(lista_correcao):
    '''
    lista: Lista que contém os cadastros
    '''

    # Validador p/ definir encerramento de pesquisa ou acesso ao item pesquisado
    validador = True

    # Ciclo principal
    while True:
        opc_pesquisa = menu_local('Pesquisa de Cadastros', '1 - Pesquisar por lista geral\n2 - Pesquisar por CPF\n0 - Voltar', 'Opção: ', n1=0, n2=2)

        # Condição de pesquisa por lista
        if opc_pesquisa == 1:

            # Ciclo de pesquisa por lista
            while True:
                posicao_cadastro = opcao_local('Pesquisa por Lista de Cadastros', f'{lista_correcao.visualizar_cadastros()}' if lista_correcao.lista_clientes != [] else 'Sem cadastro de clientes', 'Opção [0 p/ sair]: ', 'int', cls_exit=False)

                # Condição para voltar a menu anterior
                if posicao_cadastro == 0 or posicao_cadastro == None:
                    clear_screem()
                    break

                # Condição para encontrar cadastro pesquisado
                elif posicao_cadastro > len(lista_correcao.lista_clientes):
                    lines()
                    print('Fora da lista... Tente novamente.')
                    sleep_general()
                    clear_screem()
                    continue

                # Condição para alterar o cadastro pela função de correção
                else:
                    return posicao_cadastro-1

        # Condição de pesquisa por CPF
        elif opc_pesquisa == 2:
            # Ciclo de pesquisa por CPF
            while True:
                posicao_cadastro = opcao_local('Pesquisa por CPF', 'Pesquisa de CPF[digite apenas n°s].', 'CPF: ', 'int', cls_exit=False)
                # Condição de encerramento de pesquisa
                if posicao_cadastro == None:
                    clear_screem()
                    break
                
                # Condição para CPF inválido.
                elif len(str(posicao_cadastro)) != 11:
                    lines()
                    print('CPF inválido...')
                    sleep_general()
                    clear_screem()
                    continue

                # Condição para CPF válido
                else:
                    # Formatando pesquisa para padrão de cpf
                    cpf_format = str(posicao_cadastro)[:3] + '.' + str(posicao_cadastro)[3:6] + '.' + str(posicao_cadastro)[6:9] + '-' + str(posicao_cadastro)[9:11]
                    # Validador p/ cpf encontrado
                    validador_pesquisa_cpf = False

                    # Pesquisar cpf em lista geral
                    for posicao, cliente_cadastrado in enumerate(lista_correcao.lista_clientes):
                        if cpf_format == cliente_cadastrado.cpf:
                            posicao_cadastro = posicao
                            validador_pesquisa_cpf = True
                    
                    # Condição para cpf não encontrado
                    if validador_pesquisa_cpf == False:
                        lines()
                        print('CPF não encontrado...')
                        sleep_general()
                        clear_screem()
                        continue

                    # Condição para cpf encontrado
                    else:
                        return posicao_cadastro

        # Condição de encerramento
        elif opc_pesquisa == 0:
            validador = False
            return None

# Função p/ alterar cadastro        
def alterar_cadastro(posicao_lista, lista_ac):

    # Limpando tela anterior
    clear_screem()

    # Ciclo principal de correção
    while True:

        opc_ac = menu_local('Cadastro selecionado', f'{lista_ac.lista_clientes[posicao_lista]}',f'1 - Alterar nome\n2 - Alterar CPF\n3 - Alterar data de nascimento\n4 - Excluir Cadastro\n0 - Voltar\n{'-'*lines(False)}\nOpção: ', n1=0, n2=4)

        # Condição para mudar nome
        if opc_ac == 1:
            # Ciclo para corrigir nome
            while True:
                nome_correcao = opcao_local('Correção de nome', f'Nome atual: {lista_ac.lista_clientes[posicao_lista].nome}', 'Novo nome: ', 'str', cls_exit=False)

                # Condição de entrada vazia p/ encerramento
                if nome_correcao == None:
                    lines()
                    print('Entrada vazia...Encerrando')
                    sleep_general()
                    clear_screem()
                    break
                
                # Condição para atualização de cadastro - Nome
                else:
                    # Atualizando novo nome
                    lista_ac.lista_clientes[posicao_lista].nome = nome_correcao.strip()

                    # Ordenando lista em ordem alfabetica
                    lista_ac.organizar_lista(lista_ac.lista_clientes)

                    # Atualização de modificação em arquivo de save
                    posicao_lista = lista_ac.atualizar_arquivo_clientes(posicao_lista, opc_ac, nome_correcao)

                    # Encerrando correção de nome
                    lines()
                    print('Correção realizada com sucesso.')
                    sleep_general()
                    clear_screem()
                    break

        # Condição para mudar cpf
        elif opc_ac == 2:
            # Ciclo de correção de cpf
            while True:
                cpf_correcao = opcao_local('Correção de CPF', f'CPF atual: {lista_ac.lista_clientes[posicao_lista].cpf}', 'Novo CPF[Apenas n°s]: ', 'str', cls_exit=False)
                
                # Condição de entrada vazia p/ encerramento                
                if cpf_correcao == None:
                    lines()
                    print('Entrada vazia...Encerrando')
                    sleep_general()
                    clear_screem()
                    break
                # Condição que determina se cpf só tem valores numericos
                elif not cpf_correcao.isdecimal():
                    lines()
                    print('Entrada inválida...')
                    sleep_general()
                    clear_screem()
                    continue

                # Condição para CPF com qtd de n°s errada
                elif len(str(cpf_correcao)) != 11:
                    lines()
                    print('CPF inválido...')
                    sleep_general()
                    clear_screem()
                    continue
                
                # Condição p/ cpf repetido
                elif lista_ac.validacao_cpf(str(cpf_correcao)[:3] + '.' + str(cpf_correcao)[3:6] + '.' + str(cpf_correcao)[6:9] + '-' + str(cpf_correcao)[9:11]) == False:
                    lines()
                    print('CPF repetido..')
                    sleep_general()
                    clear_screem()
                    continue

                # Condição para atualização de cadastro - CPF
                else:
                    # Atualizando novo CPF
                    lista_ac.lista_clientes[posicao_lista].cpf = cpf_correcao

                    # Atualização de modificação em arquivo de save
                    posicao_lista = lista_ac.atualizar_arquivo_clientes(posicao_lista, opc_ac, cpf_correcao)

                    # Encerrando correção de CPF
                    lines()
                    print('Correção realizada com sucesso.')
                    sleep_general()
                    clear_screem()
                    break


        # Condição para mudar data de nascimento
        elif opc_ac == 3:
            # Cilco de correção de data de nascimento
            while True:
                nascimento_correcao = opcao_local('Correção Data de Nascimento', f'Data de Nascimento atual: {lista_ac.lista_clientes[posicao_lista].nascimento}', 'Nova data de nascimento [dia/mês/ano]: ', 'date', cls_exit=False)
                
                # Condição de entrada vazia p/ encerramento  
                if nascimento_correcao == None:
                    lines()
                    print('Entrada vazia...Encerrando')
                    sleep_general()
                    clear_screem()
                    break

                # Condição para atualização de data de nascimento
                else:
                    # Atualizando data de nscimento
                    lista_ac.lista_clientes[posicao_lista].nascimento = nascimento_correcao

                    # Atualização de modificação em arquivo de save
                    posicao_lista = lista_ac.atualizar_arquivo_clientes(posicao_lista, opc_ac, nascimento_correcao)

                    # Encerramento de correção de data de nascimento
                    lines()
                    print('Correção realizada com sucesso.')
                    sleep_general()
                    clear_screem()
                    break
        
        # Condição p/ excluir cadastro
        elif opc_ac == 4:
            opc_excluir = menu_local('Área de exclusão de cadastro', f'Nome: {lista_ac.lista_clientes[posicao_lista].nome}\nCPF: {lista_ac.lista_clientes[posicao_lista].cpf}', f'1 - Excluir\n0 - Voltar\n{'-'*lines(False)}\nOpção: ', n1=0, n2=1, cls_exit=False)

            # Condição para exclusão
            if opc_excluir == 1:
                # Mensagem de reforço
                opc_conf = confirmacao('Cadastro será excluído permanentemente.', cls_exit=False)

                # Condição de confirmação de exclusão
                if opc_conf == 1:
                    # Exclusão do cadastro
                    #del lista_ac.lista_clientes[posicao_lista]
                    lista_ac.excluir_cadastro(posicao_lista)

                    lista_ac.atualizar_arquivo_clientes(posicao_lista, None, None, True)

                    # Mensagem de encerramento
                    lines()
                    print('Conta excluída.')
                    sleep_general()
                    clear_screem()
                    break
                # Condição de encerramento sem excluir
                else:
                    clear_screem()

            # Condição de encerramento
            else:
                clear_screem()
             

        # Condição para voltar
        elif opc_ac == 0:
            break

# Função p/ movimentar conta
def movimentar_conta(posicao_lista, lista_ac):
    '''
    posicao_lista: Valor do retorno da função de pesquisa. Corresponde a posição da lista geral
    lista_ac: É a variável que armazena lista geral
    '''
    # Limpar tela anterior
    clear_screem()

    # Ciclo principal - Informações de cliente e contas.
    while True:
        # Variável com informações básicas do cliente e contas cadastradas
        str_info_cadastro = f'Nome: {lista_ac.lista_clientes[posicao_lista].nome}\nCPF: {lista_ac.lista_clientes[posicao_lista].cpf}'

        # Variável com as opções de contas
        if lista_ac.lista_clientes[posicao_lista].contas == []:
            str_info_opcoes = f'Não há contas vinculadas.\n0 - Voltar\n{'-'*lines(False)}\nOpção: '

        else:
            str_info_opcoes = ''
            for pos, conta in enumerate(lista_ac.lista_clientes[posicao_lista].contas, 1):
                str_info_opcoes += f'{pos} - {conta}\n'

            str_info_opcoes += f'0 - Voltar\n{'-'*lines(False)}\nOpção: '

        # Variável p/controle de entrada das opções
        n2_controle = len(lista_ac.lista_clientes[posicao_lista].contas)

        # Entrada local para escolher conta a se movimentar
        opc_movimentar_conta = menu_local('Acesso de Contas', str_info_cadastro, str_info_opcoes, n1=0, n2=n2_controle, cls_exit=False)

        # Condição p/ voltar
        if opc_movimentar_conta == 0:
            clear_screem()
            break
        
        # Condição p/ movimentar conta selecionada
        else:
            # Cliclo p/ transações
            while True:
                # Limpar tela anterior
                clear_screem()

                # Variável str para apresentação de saldo
                saldo_exibicao = f'R$ {float(lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].saldo):.2f}'.replace('.', ',')
                # Variável str com a qtd. de transações disponíveis
                qtd_transacao = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].limite_transacao()

                # Acesso a conta selecionada
                opc_conta_selecioanada = menu_local('Movimentação de conta', f'{str_info_cadastro}\n{lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1]}\nSaldo: {saldo_exibicao}\nLimite de transações: {qtd_transacao}', f'1 - Depósito\n2 - Saque\n3 - Extrato\n0 - Voltar\n{'-'*lines(False)}\nOpção: ', n1=0, n2=3, cls_exit=False)

                # Condição p/ depósito
                if opc_conta_selecioanada == 1:
                    # Limpar Tela anterior
                    clear_screem()

                    # Entrada de depósito
                    opc_deposito = opcao_local('Depósito em conta', f'{str_info_cadastro}\n{lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1]}\nSaldo: {saldo_exibicao}', f'[Entrada de decimais c/vírgula. Entre vazio p/sair]\nValor de Depósito: R$ ', 'float_monetario', cls_exit=False)
                    
                    # Condição p/ efetivação de deposito
                    if opc_deposito != None:
                        # Operação de depósito
                        return_deposito = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].deposito(opc_deposito)
                        lines()

                        # Mensagem p/ limite de transação atingido
                        if return_deposito == 'limite':
                            print('Limite de transação atingido.')

                        # Mensagem p/ depósito realizado
                        else:
                            # Variáveis locais para usar na função 'atualizar_arquivo_conta'.
                            valor_agencia = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].agencia
                            valor_conta = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].conta
                            valor_transacao_diaria = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].limite_transacao()
                            valor_tipo = 'deposito'
                            valor_transacao = opc_deposito
                            valor_saldo = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].saldo
                            valor_data = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].transacao_formatada(valor_transacao, valor_tipo)['Data']
                            
                            
                            # Salvando informações de transação no arquivo da pasta 'contas_salvas'
                            lista_ac.atualizar_arquivo_conta(valor_agencia, valor_conta, valor_transacao_diaria, valor_tipo, valor_transacao, valor_saldo, valor_data)

                            # Mensagem de sucesso na operação                            
                            print('Depósito realizado com sucesso.')

                        # Finalização    
                        sleep_general()
                        clear_screem()

                    # Condição p/ sair sem depositar
                    else:
                        clear_screem()

                # Condição p/ saque
                elif opc_conta_selecioanada == 2:
                    # Limpar Tela anterior
                    clear_screem()

                    # Entrada de depósito
                    opc_saque = opcao_local('Saque em conta', f'{str_info_cadastro}\n{lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1]}\nSaldo: {saldo_exibicao}', f'[Entrada de decimais c/vírgula. Entre vazio p/sair]\nValor de Saque: R$ ', 'float_monetario', cls_exit=False)

                    # Condição p/ efetivação de saque
                    if opc_saque != None:

                        # Operação de saque
                        retorno_saque = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].saque(opc_saque)
                        lines()

                        # Mensagem p/ saldo insuficiente
                        if retorno_saque == False:
                            print('Saldo insuficiente.')

                        # Mensagem p/ limite de transação atingido
                        elif retorno_saque == 'limite':
                            print('Limite de transação atingido.')

                        # Mensagem p/ saque efetuado
                        else:
                            # Variáveis locais para usar na função 'atualizar_arquivo_conta'.
                            valor_agencia = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].agencia
                            valor_conta = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].conta
                            valor_transacao_diaria = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].limite_transacao()
                            valor_tipo = 'saque'
                            valor_transacao = opc_saque
                            valor_saldo = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].saldo
                            valor_data = lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].transacao_formatada(valor_transacao, valor_tipo)['Data']
                            
                            # Salvando informações de transação no arquivo da pasta 'contas_salvas'
                            lista_ac.atualizar_arquivo_conta(valor_agencia, valor_conta, valor_transacao_diaria, valor_tipo, valor_transacao, valor_saldo, valor_data)
                            
                            # Mensagem de sucesso na operação 
                            print('Saque realizado com sucesso.')

                        # Finalização
                        sleep_general()
                        clear_screem()

                    # Condição p/ sair sem sacar
                    else:
                        clear_screem()


                # Condição p/ extrato
                elif opc_conta_selecioanada == 3:
                    # Limpar Tela anterior
                    clear_screem()

                    # Visualização de extrato
                    exibicao_local('Extrato', f'{lista_ac.lista_clientes[posicao_lista].contas[opc_movimentar_conta-1].extrato_bancario()}')

                # Condição p/ voltar
                elif opc_conta_selecioanada == 0:
                    clear_screem()
                    break



#-------------------------------------------------------------
if __name__ == "__main__":

    lista_correcao = Lista_Geral()

    p1 = Cliente('Tay', 12312312310, '01/11/1990')
    p2 = Cliente('Fer', 12312312311, '06/04/1989')
    p3 = Cliente('Jan', 12312312312, '20/01/1997')
    p4 = Cliente('Anf', 12312312313, '15/11/1992')

    lista_correcao.adicionar_cadastros(p1)
    lista_correcao.adicionar_cadastros(p2)
    lista_correcao.adicionar_cadastros(p3)
    lista_correcao.adicionar_cadastros(p4)

    c1 = Conta()
    c2 = Conta()

    p1.vincular_conta(c1)
    p1.vincular_conta(c2)

    while True:
        opc_p = pesquisar_cadastro(lista_correcao)

        if opc_p == None:
            break

        movimentar_conta(opc_p, lista_correcao)

    #print(lista_correcao.lista_clientes)