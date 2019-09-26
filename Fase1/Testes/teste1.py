import unittest
import DAO
import subprocess
from functools import partial
import os
import json
from datetime import datetime


class TestCase(unittest.TestCase):

    

    def add_post(self,title,text,img_url,creator_id):
        self.mysql_open_connection()
        self.send_query('START TRANSACTION')
        try:

            self.send_query('CALL add_post("%s","%s","%s",%d)' % (title,img_url,text,creator_id))
            post_id = DAO.get_last_post_id(self.connection)[0]
            for ww in text.split():
                if(ww[0]=="#"):
                    self.send_query('CALL tag_bird(%d,%d)' % (int(ww[1:]), post_id))
                elif(ww[0]=="@"):
                    self.send_query('CALL tag_user(%d,%d)' % (int(ww[1:]), post_id))

            self.send_query('COMMIT')
            self.close_connection()
            return True
        except Exception as e:
            self.send_query('ROLLBACK')
            self.close_connection()
            return False
        

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


    
    def test0_add_city(self):
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

    def test1_add_Auser(self):
        self.mysql_open_connection()
        self.send_query('START TRANSACTION')
        try:
            self.assertTrue(self.send_query('USE ara_ara'))
            self.assertTrue(self.send_query('''CALL add_user('Carlos','carlos@carlos.com',1)'''))
            self.assertTrue(self.send_query('''CALL add_user('Rodrigo','rod54@carlos.com',2)'''))
            self.assertTrue(self.send_query('''CALL add_user('Mariana','manAZ@carlos.com',4)'''))
            self.assertTrue(self.send_query('''CALL add_user('Karla','Kls@carlos.com',3)'''))
            self.assertTrue(self.send_query('''CALL add_user('Alex','lx@carlos.com',6)'''))
            self.assertTrue(self.send_query('''CALL add_user('Pedro','pd90@gg.com',3)'''))
            self.assertTrue(self.send_query('''CALL add_user('Juliano','Jll@as.com',1)'''))
            self.assertTrue(self.send_query('''CALL add_user('Marcos','mco@cos.com',5)'''))
            self.assertTrue(self.send_query('COMMIT'))
    
        except Exception as e:
            self.assertTrue(self.send_query('ROLLBACK'))

        self.close_connection()

    def test2_add_bird(self):
        self.assertTrue(self.mysql_open_connection())
        self.send_query('START TRANSACTION')
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Cacatua")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Pica-pau")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Sabiá")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Cegonha")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Arara")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Beija Flor")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Gavião")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Condor")'))
        self.assertTrue(self.send_query('INSERT INTO passaro (Nome) VALUES ("Aguia")'))
        self.send_query('COMMIT')
        self.assertTrue(self.close_connection())

    def test3_add_preference(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        try:
            self.assertTrue(self.send_query('CALL add_preference(1,2)'))
            self.assertTrue(self.send_query('CALL add_preference(3,1)'))
            self.assertTrue(self.send_query('CALL add_preference(6,5)'))
            self.send_query('COMMIT')
        except Exception as e:
            print('Falhou CALL preferencia: ',e)
            self.send_query('ROLLBACK')       
        
        
        self.close_connection()

    
    def test4_add_city_wrong(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        self.assertFalse(self.send_query('INSERT INTO cidade (Noe) VALUES ("São Paulo")'))
        self.assertTrue(self.send_query('ROLLBACK'))
        self.close_connection()

    def test5_add_post(self):
        self.assertTrue(self.add_post('Olha isso','@2 @5 olha esse #3 que está aqui no quintal de casa','img.com',1))
        self.assertTrue(self.add_post('Olha isso','@4 @6 olha essew #6 #4 que está aqui no quintal de casa','iii.ss',5))
        self.assertTrue(self.add_post('Olha isso','@3 @1 olha esse #5 #2 que está aqui no quintal de casa','os.com',2))


    def test6_add_os(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        self.assertTrue(self.send_query('INSERT INTO OS (Nome) VALUES ("Android")'))
        self.assertTrue(self.send_query('INSERT INTO OS (Nome) VALUES ("IOS")'))
        self.assertTrue(self.send_query('COMMIT'))
        self.assertTrue(self.close_connection())

    def test7_add_browser(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        self.assertTrue(self.send_query('INSERT INTO browser (Nome) VALUES ("Google Chrome")'))
        self.assertTrue(self.send_query('INSERT INTO browser (Nome) VALUES ("Firefox")'))
        self.assertTrue(self.send_query('INSERT INTO browser (Nome) VALUES ("Safari")'))
        self.assertTrue(self.send_query('INSERT INTO browser (Nome) VALUES ("Opera")'))
        self.assertTrue(self.send_query('COMMIT'))
        self.assertTrue(self.close_connection())

    def test8_visualize_post(self):
        self.assertTrue(self.mysql_open_connection())
        try:
            self.assertTrue(self.send_query('START TRANSACTION'))
            now = datetime.now()
            id = 1
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            print("NOW : ",now)
            self.assertTrue(DAO.add_view(self.connection,"INSERT INTO viu_post (id_usuario, id_post, id_OS, id_browser, IP, horario) VALUES (%s,%s,%s,%s,%s,%s);",(2,1,1,3,"172.195.29.2",formatted_date)))
            self.assertTrue(DAO.add_view(self.connection,"INSERT INTO viu_post (id_usuario, id_post, id_OS, id_browser, IP, horario) VALUES (%s,%s,%s,%s,%s,%s);",(4,1,2,1,"192.168.0.12",formatted_date)))
            self.assertTrue(DAO.add_view(self.connection,"INSERT INTO viu_post (id_usuario, id_post, id_OS, id_browser, IP, horario) VALUES (%s,%s,%s,%s,%s,%s);",(1,2,1,2,"192.168.1.25",formatted_date)))
            self.assertTrue(DAO.add_view(self.connection,"INSERT INTO viu_post (id_usuario, id_post, id_OS, id_browser, IP, horario) VALUES (%s,%s,%s,%s,%s,%s);",(3,1,1,4,"192.168.1.24",formatted_date)))
            self.assertTrue(self.send_query('COMMIT'))
        except Exception as e:
            self.assertFalse(self.send_query('ROLLBACK'))
            print(e)    

    def test9_info_post(self):
        pass


if __name__ == "__main__":
    unittest.main()

