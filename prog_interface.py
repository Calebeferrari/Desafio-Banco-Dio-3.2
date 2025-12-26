import os
from time import sleep
from datetime import datetime

# Funções de apresentação
def lines(exibir = True):
    '''
    exibir: True p/ mostrar linhas na tenha. False apenas retorna o número(int) de linhas.
    '''
    global linhas
    linhas = 50
    if exibir == True:
        print('-'*linhas)
    else:
        return linhas

def title(nome_titulo):
    lines()
    print(f'|{nome_titulo:^{linhas-2}}|')
    lines()

def clear_screem():
    if os.name == "nt":
       os.system("cls")

    else:
       os.system("clear")
       
def enter_pass():
    input('Pressione enter p/ continuar.')

def sleep_general():
    sleep(1.5)

# Funções locais
def menu_local(title_str, msg_str, input_str, n1, n2, cls_exit=True):
    '''
    title_str: Informação do título
    msg_str: Informação entre título e opções de entrada.
    input_str: Informação do input.
    msg_return: Informação opcional em caso de confirmação de entrada.
    n1: Valor mínimo de entrada do menu
    n2: Valor máximo de entrada do menu
    cls_exit: True limpa a tela automaticamente para próxima exibição. False não faz essa limpeza
    que pode ser utilizada para gerar uma mensagem específica para ser exibida na mudança de tela. 
    '''
    

    # Ciclo principal
    while True:
        
        # Título
        title(title_str)

        # Mensagem informativa
        print(msg_str)
        lines()

        # Mensagem de IMPUT
        try:
            opc_menu = int(input(input_str))

            if opc_menu < n1 or opc_menu > n2:
                raise ValueError

        except:
            lines()
            print('Entrada inválida.')
            sleep_general()
            clear_screem()

        else:
            if cls_exit == True:
                clear_screem()
                return opc_menu
            
            else:
                return opc_menu

def opcao_local(title_str, msg_str, input_str, type_input, cls_exit=True):
    '''
    title_str: Informação do título.
    msg_str: Informação entre título e opções de entrada.
    input_str: Informação do input.
    msg_return: Informação opcional em caso de confirmação de entrada.
    type: Determina o tipo de entrada que será aceita. 'str', 'int', 'float', 'float_monetario' e 'date'.
    cls_exit: True limpa a tela automaticamente para próxima exibição. False não faz essa limpeza
    que pode ser utilizada para gerar uma mensagem específica para ser exibida na mudança de tela.
    '''
    # Ciclo principal
    while True:
        # Título
        title(title_str)

        # Mensagem informativa
        print(msg_str)
        lines()

        # Input local - entrada da mensagem
        opc_local = input(input_str).strip()

        # Condição de entrada vazia
        if opc_local == '':
            return None

        # Tratamento de erros para entradas específicas
        try:
            # Condições para str
            if type_input == 'str':
                result = opc_local.strip().title()

            # Condições para int
            elif type_input == 'int':
                result = int(opc_local)

            # Condições para float
            elif type_input == 'float':
                result = float(opc_local)
            
            # Condição para float monetário - P/ entrada de decimais com virgula - Retorna float normal
            elif type_input == 'float_monetario':
                if '.' in opc_local:
                    raise ValueError
                else:
                    result = opc_local.replace(',', '.')
                    result = float(result)
            
            # Condições para date
            elif type_input == 'date':
                date_convertion = datetime.strptime(opc_local, '%d/%m/%Y').date()
                result = date_convertion.strftime('%d/%m/%Y')
            
        except:
            lines()
            print('Entrada inválida.')
            sleep_general()
            clear_screem()

        else:

            if cls_exit == True:
                clear_screem()
                return result
            
            else:
                return result

def exibicao_local(title_str, msg_str):
    '''
    title_str: Informação do título.
    msg_str: Informação entre título e opções de entrada.
    '''
    # Título
    title(title_str)

    # Mensagem informativa
    print(msg_str)

    # Finalização
    lines()
    enter_pass()
    clear_screem()


def confirmacao(msg_str, cls_exit=True):
    '''
    msg_str: Mensagem de atenção p/ ação a ser executada.
    cls_exit: True p/ limpar tela ao sair e False para não limpar tela.
    '''

    while True:
        try:
            lines()
            print(msg_str)
            opc_confirmacao = int(input(f'Deseja continuar?\n1 - Sim\n0 - Não\n{'-'*lines(False)}\nOpção: '))
        except:
            lines()
            print('Erro... Tente novamente')
            sleep_general()
            clear_screem()
        
        else:
            if cls_exit == True:
                clear_screem()
                return opc_confirmacao
            else:
                return opc_confirmacao


#-----------------------------------------------------------------------------------------

if __name__ == "__main__":
    opc = confirmacao('O arquivo será excluído.', False)

    print(opc)