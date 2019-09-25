import unittest
import DAO
from functools import partial


class Teste_Implementacao(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Teste_Implementacao, self).__init__(*args, **kwargs)
        print("Abrindo Conexão...")
        try:
            self.connection = DAO.connectMYSQL()
            db = partial(DAO.run_db_query, self.connection)
            print("Conexão Aberta")
        except Exception as e:
            print(e)

    def teste_insercao(self):
        print("oi")

    def test_close_connection(self):
        print("Fechando Conexão...")
        self.connection.close()
        print("Conexão Fechada!!!")


if __name__ == "__main__":
    unittest.main()
