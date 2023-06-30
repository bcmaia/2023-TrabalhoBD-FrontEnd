# EXECUTE `pip install -r requirements.txt` PARA INSTALAR BIBLIOTECAS 
# NECESSÁRIAS

import os
from dotenv import load_dotenv

# IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS PARA CONECTAR AO ORACLE
import oracledb
import getpass


print('Inicializando sessão...')
print('Versão do oracle:', oracledb.__version__)





# LEITURA DAS VARIÁVEIS DE AMBIENTE PARA BUSCAR CREDENCIAIS DA CONEXÃO
def load_env():
    load_dotenv()

    user = os.environ.get('BD_USER')
    pw = os.environ.get('BD_PW')

    print('')
    if None == user: user = input('USER NAME: ')
    if None == pw: pw = getpass.getpass('Password: ')

    print('Conectando...')

    return {'user': user, 'pw': pw}





class Db:
    __DNS = 'orclgrad1.icmc.usp.br/pdb_elaine.icmc.usp.br'

    def __init__(
        self, 
        cred = None, 
        dns = None,
    ) -> None:
        self.__dns = Db.__DNS if None == dns else dns
        self.__cred = load_env() if None == cred else cred
        self.__active = False
        
        self.connect()
    
    def connect(self):
        if self.__active: raise Exception('ERROR: Already connected.')

        # ESPECIFICAÇÃO DE DSN (NÃO ALTERAR)

        self.__con = oracledb.connect(
            user = self.__cred['user'], 
            password = self.__cred['pw'], 
            dsn = self.__dns
        ) # CONECTA-SE AO BANCO DE DADOS

        # CRIAÇÃO DE UM PONTEIRO
        self.__cur = self.__con.cursor()

        # INICIANDO TRANSAÇÃO
        self.__con.begin()

        self.__active = True
        return self
    
    def validate(self):
        if not self.__active: raise Exception('ERROR: Connection lost.')
        return self
    
    def query (self, query, vals = None):
        if None == vals: self.validate().__cur.execute(query)
        else: self.validate().__cur.execute(query, vals)
        res = self.__cur.fetchall()
        return res
    
    def trans (self, query, vals = None):
        if None == query: self.validate().__cur.execute(query)
        else: self.validate().__cur.execute(query, vals)
        return self
    
    def commit(self):
        self.validate().__con.commit()
        return self

    def rollback(self):
        self.validate().__con.rollback()
        return self

    def disconnect (self):
        self.__cur.close()
        self.__con.close()
        self.__active = False

        return self
