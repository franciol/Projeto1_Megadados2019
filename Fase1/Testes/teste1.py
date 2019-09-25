import unittest
import DAO
import subprocess
from functools import partial
import os
import json


class TestCase(unittest.TestCase):

    def add_post(self):
        pass

    def mysql_open_connection(self):
        try:
            self.connection = DAO.connectMYSQL()
            return True
        except Exception as e:
            print(e)
            return False
        

    def send_query(self,data):
        try:
            DAO.run_db_query(self.connection,data)
            return True
        except Exception as e:
            print(e)
            return False
        

    def close_connection(self):
        try:
            self.connection.close()
            return True
        except Exception as e:
            print(e)
            return False
        self.connection.close()
                
    
    @classmethod
    def setUpClass(cls):
        with open('acesso.json') as json_data:
            d = json.load(json_data)    
            str1 = str('mysql -u '+d['connection']['user']+' -p'+d['connection']['password'])
            for file in sorted(os.listdir('../Scripts/')):
                with open('../Scripts/'+file,'rb') as f:
                    res = subprocess.run(str1.split(),stdin=f)
                    print(res)
        
        return super().setUpClass()


    def test_add_preference(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        try:
            self.assertTrue(self.send_query('CALL add_preference(1,2)'))
            self.assertTrue(self.send_query('CALL add_preference(3,2)'))
            self.assertTrue(self.send_query('CALL add_preference(4,3)'))
            self.send_query('COMMIT')
        except Exception as e:
            print(e)
            self.send_query('ROLLBACK')       
        
        
        self.close_connection()

    def test_add_bird(self):
        self.assertTrue(self.mysql_open_connection())
        self.send_query('START TRANSACTION')
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Cacatua")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Pica-pau")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Sabiá")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Cegonha")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Arara")'))
        self.send_query('COMMIT')
        self.assertTrue(self.close_connection())


    def test_add_user(self):
        self.mysql_open_connection()
        self.send_query('START TRANSACTION')
        try:
            self.assertTrue(self.send_query('USE ara_ara'))
            self.assertTrue(self.send_query('''CALL add_user('Carlos','carlos@carlos.com',1)'''))
            self.assertTrue(self.send_query('''CALL add_user('Rodrigo','rod54@carlos.com',2)'''))
            self.assertTrue(self.send_query('''CALL add_user('Mariana','manAZ@carlos.com',4)'''))
            self.assertTrue(self.send_query('''CALL add_user('Karla','Kls@carlos.com',3)'''))
            self.assertTrue(self.send_query('''CALL add_user('Alex','lx@carlos.com',6)'''))
            self.assertTrue(self.send_query('COMMIT'))
    
        except Exception as e:
            self.assertTrue(self.send_query('ROLLBACK'))

        self.close_connection()
  
    def test_add_city(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        self.assertTrue(self.send_query('USE ara_ara'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("Cardinal")'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("São Paulo")'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("Curitiba")'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("Fortaleza")'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("São Jose dos Campos")'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("São Carlos")'))
        self.assertTrue(self.send_query('COMMIT'))
        self.close_connection()
            
        

    def test_add_city_wrong(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        self.assertTrue(self.send_query('USE ara_ara'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("Cardinal")'))
        self.assertFalse(self.send_query('INSERT INTO cidade (Noe) VALUES ("São Paulo")'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("Curitiba")'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("Fortaleza")'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("São Jose dos Campos")'))
        self.assertTrue(self.send_query('INSERT INTO cidade (Nome) VALUES ("São Carlos")'))
        self.assertTrue(self.send_query('ROLLBACK'))
        self.close_connection()

    
if __name__ == "__main__":
    unittest.main()

