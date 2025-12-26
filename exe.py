from prog_interface import*
from prog_class import*
from prog_funcoes import*

# Declaração de classe
lista_sistema = Lista_Geral()

# Carregando arquivo salvo
lista_sistema.carregar_arquivo_cadastros()

# Declaração de menu principal
str_menu_principal = '1 - Cadastrar Cliente\n2 - Cadastrar Conta\n3 - Movimentar Conta\n4 - Verificar Cadastros\n5 - Lista Geral\n6 - Área do Programador\n0 - Encerrar'

# Ciclo de Menu principal
while True:

    # Menu principal
    opc_menu_principal = menu_local('Banco Dio 3.0', str_menu_principal, 'Opção: ', n1=0, n2=6)

    # Opção 1 - Cadastrar cliente
    if opc_menu_principal == 1:
        # Variável de validação de cadastro
        validador_cadastro = True

        # Ciclo de cadastro
        while True:

            # CADASTRO DE NOME
            nome_cadastro = opcao_local('Cadastro Nome', 'Informe nome completo.\n[ou entre vazio p/ encerrar]','Nome: ', 'str')
            
            # Encerramento de cadastro se entrada for vazia
            if nome_cadastro == None:
                lines()
                validador_cadastro = False
                print('Entrada vazia...Encerrando cadastro')
                sleep_general()
                clear_screem()
                break
            
            # CADASTRO DE CPF
            while True:
                cpf_cadastro = opcao_local('Cadastro CPF', 'Informe apenas os digitos do cpf.\n[ou entre vazio p/ encerrar]', 'CPF: ', 'str', cls_exit=False)
                
                # Condição de encerramento se entrada for vazia
                if cpf_cadastro == None:
                    lines()
                    validador_cadastro = False
                    print('Entrada vazia...Encerrando cadastro')
                    sleep_general()
                    clear_screem()
                    break
                
                # Condição que determina se cpf só tem valores numericos
                elif not cpf_cadastro.isdecimal():
                    lines()
                    print('Entrada inválida...')
                    sleep_general()
                    clear_screem()
                    continue

                # Condição para CPF com qtd de caracteres errada
                elif len(str(cpf_cadastro)) != 11:
                    lines()
                    print('CPF inválido...')
                    sleep_general()
                    clear_screem()
                    continue
                
                # Condição p/ cpf repetido
                elif lista_sistema.validacao_cpf(str(cpf_cadastro)[:3] + '.' + str(cpf_cadastro)[3:6] + '.' + str(cpf_cadastro)[6:9] + '-' + str(cpf_cadastro)[9:11]) == False:
                    lines()
                    print('CPF repetido..')
                    sleep_general()
                    clear_screem()
                    continue

                # Condição para cpf válido mais formatação de CPF com pontuação
                else:
                    # Confirmar validador, limpar tela e interromper ciclo
                    validador_cadastro = True
                    clear_screem()
                    break

            # Encerrar cadastro em caso de entrada vazia de CPF.    
            if validador_cadastro == False:
                break

            # CADASTRO DATA DE NASCIMENTO
            nascimento_cadastro = opcao_local('Cadastro Data de Nascimento', 'Informe data no padrão: dia/mês/ano.\n[ou entre vazio p/ encerrar]','Data de nascimento: ', 'date')
            
            # Encerramento de cadastro se entrada for vazia
            if nascimento_cadastro == None:
                lines()
                validador_cadastro = False
                print('Entrada vazia...Encerrando cadastro')
                sleep_general()
                clear_screem()
                break


            # Adicionando classe do Cliente a classe de lista de cadastros
            cadastro_atual = Cliente(nome_cadastro, cpf_cadastro, nascimento_cadastro)

            if validador_cadastro == True:
                # Adicionando cadastro a lista do sistema
                lista_sistema.adicionar_cadastros(cadastro_atual)
                
                # Salvando informações em arquivo do tipo csv
                lista_sistema.salvar_arquivo_cadastro(nome_cadastro, cpf_cadastro, nascimento_cadastro)

            else:
                break

            # Organizando lista em ordem alfabética
            lista_sistema.organizar_lista(lista_sistema.lista_clientes)

            # Confirmação de dados cadastrados
            exibicao_local('Cadastro efetivado', f'{cadastro_atual}')

            # Finalizar ciclo de cadastro
            break

    # Opção 2 - Criar conta
    elif opc_menu_principal == 2:

        # Organizando lista em ordem alfabética
        lista_sistema.organizar_lista(lista_sistema.lista_clientes)

        # Ciclo de processo de pesquisa e criação de conta
        while True:
            # Funcão de pesquisa de cadastro
            opc_pc = pesquisar_cadastro(lista_sistema)

            # Condicional para finalizar ciclo
            if opc_pc == None:
                break
            
            # Ciclo de vinculação de conta a cadastro
            while True:
                # Visualização do cadastro a ter conta vinculada
                clear_screem()
                opc_pc_menu_local = menu_local('Dados de Cliente', f'{lista_sistema.lista_clientes[opc_pc]}',f'1 - Criar Conta\n0 - Voltar\n{'-'*lines(False)}\nOpção: ', n1=0, n2=1, cls_exit=False)

                # Condicional para criar conta
                if opc_pc_menu_local == 1:

                    # Confirmação de p/ criação de conta
                    opc_confirmacao_conta = confirmacao('Uma nova conta será criada.', cls_exit=False)

                    # Condicionais de confirmação de criação de conta.
                    if opc_confirmacao_conta == 1:
                        # Criação de conta
                        conta_local = Conta()
                        # Vinculação de conta a cadastro selecionado
                        lista_sistema.lista_clientes[opc_pc].vincular_conta(conta_local)
                        # Salvar atualização em arquivo
                        lista_sistema.atualizar_arquivo_cadastro(opc_pc, conta_local.agencia, conta_local.conta)
                        # Visualização de conta local
                        lines()
                        print('Conta cadastrada com sucesso.')
                        enter_pass()
                        clear_screem()

                    # Condição p/ não criar conta
                    elif opc_confirmacao_conta == 0:
                        lines()
                        print('Criação de conta não realizada.')
                        sleep_general()
                        clear_screem()

                # Condicional para sair da área de criação de conta
                elif opc_pc_menu_local == 0:
                    lines()
                    clear_screem()
                    break

    # Opção 3 - Movimentar conta
    elif opc_menu_principal == 3:

        # Organizando lista em ordem alfabética
        lista_sistema.organizar_lista(lista_sistema.lista_clientes)

        # Ciclo da relação de pesquisa de cadastro e movimentação de contas
        while True:
            opc_pesq_movimentacao = pesquisar_cadastro(lista_sistema)
            # Condição para encerramento de ciclo
            if opc_pesq_movimentacao == None:
                break
            # Função de movimentação de conta selecionada
            movimentar_conta(opc_pesq_movimentacao, lista_sistema)

    # Opção 4 - Pesquisar cadastros
    elif opc_menu_principal == 4:

        # Ciclo de funções de pesquisa e correção de cadastro
        while True:
            # Organizando lista em ordem alfabética
            lista_sistema.organizar_lista(lista_sistema.lista_clientes)
            # Pesquisando cadastros para consulta de dados e correção 
            opc_pc = pesquisar_cadastro(lista_sistema)
            # Condição para encerramento de ciclo
            if opc_pc == None:
                break
            # Função de alteração de cadastro
            alterar_cadastro(opc_pc, lista_sistema)

    # Opção 5 - Verifiar lista de cadastros
    elif opc_menu_principal == 5:

        # Se não houver cadastros
        if lista_sistema.lista_clientes == []:
            exibicao_local('Lista Geral', 'Lista de cadastro vazia')
        
        # Se lista tiver cadastros
        else:
            # Organizando lista em ordem alfabética
            lista_sistema.organizar_lista(lista_sistema.lista_clientes)

            # Visualização rápida de lista geral de cadastros - Apenas nome e cpf
            exibicao_local('Lista Geral', f'{lista_sistema.visualizar_cadastros()}')
    
    # Opção 6 - Área do programador
    elif opc_menu_principal == 6:
        # Organizando lista em ordem alfabética
        #lista_sistema.organizar_lista(lista_sistema.lista_clientes)

        # Visualizar lista geral
        #for pos, cliente_ in enumerate(lista_sistema.lista_clientes):
        #    print(cliente_)
        #    print()
        
        #print(lista_sistema.lista_clientes[0].contas[2].conta)

        lista_sistema.carregar_arquivos_contas()

        # Precione enter para continuar
        enter_pass()
        clear_screem()

    # Opção 0 - Encerrar programa
    elif opc_menu_principal == 0:
        lines()
        print('Encerrando programa...')
        sleep_general()
        clear_screem()
        break