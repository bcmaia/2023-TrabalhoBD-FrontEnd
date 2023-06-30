import traceback
from utils import Db


# Variáveis 'globais'
global_state = {'debug': False}


# Inicializando a Base de Dados
print('Inicializando sessão, isso pode demorar um pouco...', end='')
db = Db()
print(' pronto!\n\n', end='')


# Parse params
# Lê uma string e analiza os parametros, filtrando --flags.
def parse_params (params : list[str]):
    if not params: return ({}, [])

    myFlags = {}
    myParams = []

    hungry_flag = ''

    for i in params[1:]:
        if hungry_flag:
            if '--' == i[:2]: raise Exception('[ERRO] Esperava um valor, e não outra flag.')
            myFlags[hungry_flag] = i
            hungry_flag = ''
        elif '--by-' == i[:5]:
            myFlags[i] = True
            hungry_flag = i
        elif '--' == i[:2]:
            myFlags[i] = True
        else:
            myParams.append(i)

    return {'flags': myFlags, 'params': myParams}


# Set Debug
# Essa função permite ativar o modo de debug. Não é muito útil para o usuário 
# final, mas é extremamente útil para os desenvolvedores.
def set_debug(param : list[str], flags : dict[str, any]):
    global_state['debug'] = 'true' == param[0]
    if not param[0] in ['true', 'false']:
        raise Exception(f'[ERRO] Valor não esperado ("{param[0]}").')
    print(f'Debug now set to {global_state["debug"]}')


# No operation
# Não faz nada, mas ela é usada para codificar o comando quit que não é 
# processado da mesma maneira que os outros comandos.
def noop(param : list[str], flags : dict[str, any]):
    pass


# Hello, World!
# Um clássico da programação. Está aqui para auxiliar testes
def hello(param : list[str], flags : dict[str, any]):
    print('Olá, Mundo!')


# Função auxiliar: where_flags
# Ela gera o codigo sql e um dicionario com os parametros necessários.
def where_flags (atrbs : list[str], flags : dict[str, any]):
    where = []
    d = dict()
    for a in atrbs:
        a_low = a.lower()
        a_up = a.upper()
        a_val = flags.get(f'--by-{a_low}')

        if a_val:
            where.append(f'{a_up} = :{a_low}')
            d[a_low] = a_val

    return (where, d)



# INSERT NEW SITE
def insert(params : list[str], flags : dict[str, any]):
    print('CADASTRANDO O NOVO SITE...')

    if 3 > len(params[0]):
        raise Exception(
            '[ERRO] Numero de parametros insuficiente.'
            + ' Para inserir um novo site, é preciso passar, respectivamente,'
            + ' URL, NOME e DONO.'
        )

    db.trans(
        'INSERT INTO SITE(URL, NOME, DONO) VALUES (:url, :nome, :dono)',
        {
            'url': params[0],
            'nome': params[1],
            'dono': params[2],
        },
    ).commit()

    print('Cadastro finalizado com sucesso!')


# SEARCH SITE
def search(params : list[str], flags : dict[str, any]):
    print('BUSCANDO...')

    # Temos o parametro padrão de busca
    val = params[0] if params else None
    
    # Estrutura base da query sql
    sql = 'SELECT NOME, URL, DONO FROM SITE WHERE '

    # Definindo condições de busca
    # Qual as condições? Pode ter mais de uma.
    where = ['URL = :val'] if val else []
    params = {'val': val} if val else {}

    w, d = where_flags(['DONO', 'NOME'], flags)
    where = where + w
    params.update(d)

    # debug
    if global_state['debug']: 
        print('Where value:')
        print(where)
        print('Params value:')
        print(params)

    # Tratando erros
    if not where: raise Exception('[ERRO] Os dados providos são insuficentes.')

    # compondo a query sql final
    sql = sql + ' AND '.join(where)
    
    if global_state['debug']: 
        print('SQL value:')
        print(sql)
    
    # Execuntando a query
    result = db.query(sql, params)
    readable_results = [f'{i}: {v}' for i, v in enumerate(result)]

    print('RESULTADOS: ')
    print('#: (URL, NOME, DONO)')
    print('\n'.join(readable_results))



# LIST ALL SITES
def list_func (params : list[str], flags : dict[str, any]):
    result = db.query('SELECT * FROM SITE')

    print('SITES: ')
    print('\n'.join([f'{i}: {v}' for i, v in enumerate(result)]))
    


# DELETE SITE
def delete(params: list[str], flags : dict[str, any]):
    print('DELETANDO...')

    val = params[0] if params else None
    
    sql = 'DELETE FROM SITE WHERE '

    where = ['URL = :val'] if val else []
    params = {'val': val} if val else {}

    w, d = where_flags(['DONO', 'NOME'], flags)
    where = where + w
    params.update(d)

    if global_state['debug']: 
        print('Where value:')
        print(where)
        print('Params value:')
        print(params)

    if not where: raise Exception('[ERRO] Os dados providos são insuficentes.')

    sql = sql + ' AND '.join(where)
    
    if global_state['debug']: 
        print('SQL value:')
        print(sql)
    
    db.trans(sql, params).commit()
   
    print('Cadastro deletado com sucesso!')


# COMANDOS DISPONÍVEIS
commands = {
    'quit': { # Presente por motivos de completude
        'h': 'Finaliza a sessão.',
        'f': noop, 
    },
    'hello': {
        'h': 'Comando olá mundo :)',
        'f': hello, 
    },
    'search': {
        'h': 'Busca um site em nossa base de dados.',
        'f': search, 
    },
    'list' : {
        'h': 'Lista todos os sites.',
        'f': list_func, 
    },
    'debug': {
        'h': 'Ativa e desativa o modo de debug.',
        'f': set_debug,
    },
    'insert': {
        'h': 'Cadastra um novo site.',
        'f': insert,
    },
    'delete': {
        'h': 'Deleta um site.',
        'f': delete,
    },
}



# MAIN
if '__main__' == __name__:
    print(
        '======================================================='
    + '\n======//  Bem-vindo ao Recursos Mínimos //============='
    + '\n======================================================='
        + '\n\n',
        end=''
    )

    print('Comandos disponíveis:')
    print('\n'.join([f'{k} \t\t:\t\t {v["h"]}' for k, v in commands.items()]))
    print('\n')

    # Loop de execução
    while True:
        i = input('> ')

        # Tratando o input
        params = [x for x in i.split(' ') if x]
        if not params: continue # Avoiding erros

        # qual comando será executado?
        cmd = commands.get(params[0])

        # Saida do loop
        print ('- ', end='')
        if commands['quit'] is cmd: break
        if None == cmd: 
            print('[ERRO] Comando não encontrado...\n')
            continue

        # separando parametros e flags
        temp = parse_params(params)
        params = temp['params']
        flags = temp['flags']

        # Execução do comando
        try:
            cmd['f'](params, flags)
        except Exception as e:
            print("Ops! An error occurred:")
            if global_state['debug']: print(traceback.format_exc())
            print("Error message:", str(e))

        print('')

    print('Finalizando sessão...\n')