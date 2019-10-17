import unittest
import DAO
import subprocess
from functools import partial
import os
import json
from datetime import datetime


class TestCase(unittest.TestCase):
    def add_post(self, title, text, img_url, creator_id):
        self.mysql_open_connection()
        self.send_query('START TRANSACTION')
        try:

            self.send_query('CALL add_post("%s","%s","%s",%d)' %
                            (title, img_url, text, creator_id))
            post_id = DAO.get_last_post_id(self.connection)[0]
            for ww in text.split():
                if (ww[0] == "#"):
                    self.send_query('CALL tag_bird(%d,%d)' %
                                    (int(ww[1:]), post_id))
                elif (ww[0] == "@"):
                    self.send_query('CALL tag_user(%d,%d)' %
                                    (int(ww[1:]), post_id))

            self.send_query('COMMIT')
            self.close_connection()
            return True
        except Exception as e:
            self.send_query('ROLLBACK')
            self.close_connection()
            return False

    def list_posts(self):
        result = DAO.run_db_query_with_return(self.connection,
                                              "SELECT * FROM post")
        res = result.fetchall()

    def mysql_open_connection(self):
        try:
            self.connection = DAO.connectMYSQL()
            return True
        except Exception as e:
            print(e)
            return False

    def send_query(self, data):
        try:
            DAO.run_db_query(self.connection, data)
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
            str1 = str('mysql -u ' + d['connection']['user'] + ' -p' +
                       d['connection']['password'])
            for file in sorted(os.listdir('../Scripts/')):
                with open('../Scripts/' + file, 'rb') as f:
                    res = subprocess.run(str1.split(), stdin=f)
                    print(res)

        return super().setUpClass()

    def test00_add_city(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        self.assertTrue(self.send_query('USE ara_ara'))
        self.assertTrue(
            self.send_query('INSERT INTO cidade (Nome) VALUES ("Cardinal")'))
        self.assertTrue(
            self.send_query('INSERT INTO cidade (Nome) VALUES ("São Paulo")'))
        self.assertTrue(
            self.send_query('INSERT INTO cidade (Nome) VALUES ("Curitiba")'))
        self.assertTrue(
            self.send_query('INSERT INTO cidade (Nome) VALUES ("Fortaleza")'))
        self.assertTrue(
            self.send_query(
                'INSERT INTO cidade (Nome) VALUES ("São Jose dos Campos")'))
        self.assertTrue(
            self.send_query('INSERT INTO cidade (Nome) VALUES ("São Carlos")'))
        self.assertTrue(self.send_query('COMMIT'))
        self.close_connection()

    def test01_add_Auser(self):
        self.mysql_open_connection()
        self.send_query('START TRANSACTION')
        try:
            self.assertTrue(self.send_query('USE ara_ara'))
            self.assertTrue(
                self.send_query(
                    '''CALL add_user('Carlos','carlos@carlos.com',1)'''))
            self.assertTrue(
                self.send_query(
                    '''CALL add_user('Rodrigo','rod54@carlos.com',2)'''))
            self.assertTrue(
                self.send_query(
                    '''CALL add_user('Mariana','manAZ@carlos.com',4)'''))
            self.assertTrue(
                self.send_query(
                    '''CALL add_user('Karla','Kls@carlos.com',3)'''))
            self.assertTrue(
                self.send_query('''CALL add_user('Alex','lx@carlos.com',6)'''))
            self.assertTrue(
                self.send_query('''CALL add_user('Pedro','pd90@gg.com',3)'''))
            self.assertTrue(
                self.send_query('''CALL add_user('Juliano','Jll@as.com',1)'''))
            self.assertTrue(
                self.send_query('''CALL add_user('Marcos','mco@cos.com',5)'''))
            self.assertTrue(self.send_query('COMMIT'))

        except Exception as e:
            self.assertTrue(self.send_query('ROLLBACK'))

        self.close_connection()

    def test02_add_bird(self):
        self.assertTrue(self.mysql_open_connection())
        self.send_query('START TRANSACTION')
        self.assertTrue(
            self.send_query('INSERT INTO passaro (Nome) VALUES ("Cacatua")'))
        self.assertTrue(
            self.send_query('INSERT INTO passaro (Nome) VALUES ("Pica-pau")'))
        self.assertTrue(
            self.send_query('INSERT INTO passaro (Nome) VALUES ("Sabiá")'))
        self.assertTrue(
            self.send_query('INSERT INTO passaro (Nome) VALUES ("Cegonha")'))
        self.assertTrue(
            self.send_query('INSERT INTO passaro (Nome) VALUES ("Arara")'))
        self.assertTrue(
            self.send_query(
                'INSERT INTO passaro (Nome) VALUES ("Beija Flor")'))
        self.assertTrue(
            self.send_query('INSERT INTO passaro (Nome) VALUES ("Gavião")'))
        self.assertTrue(
            self.send_query('INSERT INTO passaro (Nome) VALUES ("Condor")'))
        self.assertTrue(
            self.send_query('INSERT INTO passaro (Nome) VALUES ("Agua")'))
        self.send_query('COMMIT')
        self.assertTrue(self.close_connection())

    def test03_add_preference(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        try:
            self.assertTrue(self.send_query('CALL add_preference(1,2)'))
            self.assertTrue(self.send_query('CALL add_preference(3,1)'))
            self.assertTrue(self.send_query('CALL add_preference(6,5)'))
            self.send_query('COMMIT')
        except Exception as e:
            print('Falhou CALL preferencia: ', e)
            self.send_query('ROLLBACK')

        self.close_connection()

    def test04_add_city_wrong(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        self.assertFalse(
            self.send_query('INSERT INTO cidade (Noe) VALUES ("São Paulo")'))
        self.assertTrue(self.send_query('ROLLBACK'))
        self.close_connection()

    def test05_add_post(self):
        self.assertTrue(
            self.add_post(
                'Olha isso',
                '@2 @5 olha esse #3 que está aqui no quintal de casa',
                'img.com', 1))
        self.assertTrue(
            self.add_post(
                'Olha isso',
                '@4 @6 olha essew #6 #4 que está aqui no quintal de casa',
                'iii.ss', 5))
        self.assertTrue(
            self.add_post(
                'Olha isso',
                '@3 @1 olha esse #5 #2 que está aqui no quintal de casa',
                'os.com', 2))

    def test06_add_os(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        self.assertTrue(
            self.send_query('INSERT INTO OS (Nome) VALUES ("Android")'))
        self.assertTrue(
            self.send_query('INSERT INTO OS (Nome) VALUES ("IOS")'))
        self.assertTrue(self.send_query('COMMIT'))
        self.assertTrue(self.close_connection())

    def test07_add_browser(self):
        self.assertTrue(self.mysql_open_connection())
        self.assertTrue(self.send_query('START TRANSACTION'))
        self.assertTrue(
            self.send_query(
                'INSERT INTO browser (Nome) VALUES ("Google Chrome")'))
        self.assertTrue(
            self.send_query('INSERT INTO browser (Nome) VALUES ("Firefox")'))
        self.assertTrue(
            self.send_query('INSERT INTO browser (Nome) VALUES ("Safari")'))
        self.assertTrue(
            self.send_query('INSERT INTO browser (Nome) VALUES ("Opera")'))
        self.assertTrue(self.send_query('COMMIT'))
        self.assertTrue(self.close_connection())

    def test08_visualize_post(self):
        self.assertTrue(self.mysql_open_connection())
        try:
            self.assertTrue(self.send_query('START TRANSACTION'))
            now = datetime.now()
            id = 1
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

            self.assertTrue(
                DAO.add_view(
                    self.connection,
                    "INSERT INTO viu_post (id_usuario, id_post, id_OS, id_browser, IP, horario) VALUES (%s,%s,%s,%s,%s,%s);",
                    (2, 1, 1, 3, "172.195.29.2", formatted_date)))
            self.assertTrue(
                DAO.add_view(
                    self.connection,
                    "INSERT INTO viu_post (id_usuario, id_post, id_OS, id_browser, IP, horario) VALUES (%s,%s,%s,%s,%s,%s);",
                    (4, 1, 2, 1, "192.168.0.12", formatted_date)))
            self.assertTrue(
                DAO.add_view(
                    self.connection,
                    "INSERT INTO viu_post (id_usuario, id_post, id_OS, id_browser, IP, horario) VALUES (%s,%s,%s,%s,%s,%s);",
                    (1, 2, 1, 2, "192.168.1.25", formatted_date)))
            self.assertTrue(
                DAO.add_view(
                    self.connection,
                    "INSERT INTO viu_post (id_usuario, id_post, id_OS, id_browser, IP, horario) VALUES (%s,%s,%s,%s,%s,%s);",
                    (3, 1, 1, 4, "192.168.1.24", formatted_date)))
            self.assertTrue(self.send_query('COMMIT'))
        except Exception as e:
            self.assertTrue(0 == 1)
            self.assertFalse(self.send_query('ROLLBACK'))
            print(e)

    def test09_SELECT_CITY(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_cidade FROM cidade WHERE Nome = "Curitiba" ')
            a = ss.fetchall()
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test10_SELECT_CITY_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_cidade FROM cidade WHERE Nome = "Noe" ')
            a = ss.fetchall()
            self.assertTrue(len(a) == 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test11_CHANGE_CITY(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE cidade SET Nome = "Uberlandia" WHERE Nome = "Cardinal" '
            )
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test12_CHANGE_CITY_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE cidade SET Nome = "Uberlandia" WHERE Nome = "NOPE" ')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test13_DELETE_CITY(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query('DELETE FROM cidade WHERE id_cidade = 1')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test14_SELECT_USER(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_usuario FROM usuario WHERE Nome = "Rodrigo" ')
            a = ss.fetchall()
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test15_SELECT_USER_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_usuario FROM usuario WHERE Nome = "NOPES" ')
            a = ss.fetchall()
            self.assertTrue(len(a) == 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test16_CHANGE_USER(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE usuario SET Nome = "Jonas" WHERE Nome = "Juliano" ')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test17_CHANGE_USER_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE usuario SET Nome = "Juliano" WHERE Nome = "NOPES" ')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test18_DELETE_USER(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query('UPDATE usuario SET ativo=0 WHERE id_usuario = 1')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test19_SELECT_BIRD(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_passaro FROM passaro WHERE Nome = "Cacatua" ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test20_SELECT_BIRD_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_passaro FROM passaro WHERE Nome = "Mss" ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) == 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test21_CHANGE_BIRD(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE passaro SET Nome = "Aguia" WHERE Nome = "Agua" ')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test21_CHANGE_BIRD_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE passaro SET Nome = "Juliano" WHERE Nome = "NOPES" ')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test22_DELETE_BIRD(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query('DELETE FROM passaro WHERE id_passaro = 1')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test23_ADD_PREFERENCES_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query('CALL add_preference(%s,%s)', (9, 1))
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 == 1)
        except Exception as e:
            self.assertTrue(0 != 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test24_SELECT_PREFERENCES(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_passaro FROM preferencia WHERE id_usuario = 3 ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test25_CHANGE_PREFERENCE(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE preferencia SET id_passaro=3 WHERE id_usuario = 1  AND id_passaro=2  '
            )
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test26_CHANGE_PREFERENCE_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE preferencia SET id_passaro=12 WHERE id_usuario = 4  AND id_passaro=2  '
            )
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 == 1)
        except Exception as e:
            self.assertTrue(0 < 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test27_DELETE_PREFERENCE(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'DELETE FROM preferencia WHERE id_passaro = 2 AND id_usuario = 1'
            )
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test28_add_post_WRONG(self):
        try:

            self.assertTrue(
                self.add_post(
                    'Olha isso',
                    '@2 @5 olha esse #3 que está aqui no quintal de casa',
                    'img.com', 99))
            self.assertTrue(1 == 2)

        except Exception as e:
            print(e)
            self.assertTrue(1 == 1)

    def test29_SELECT_POST(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_post FROM post WHERE Imagem = "img.com" ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test30_SELECT_POST_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_post FROM post WHERE Imagem = "imgss.com" ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) == 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test31_CHANGE_POST(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE post SET Imagem="OpaOpaOpa.com" WHERE id_post = 1')
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 == 1)
        except Exception as e:
            self.assertTrue(0 < 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test32_DELETE_POST(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query('UPDATE post SET ativo=0 WHERE id_post = 1')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test33_SELECT_os(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection, 'SELECT id_OS FROM OS WHERE Nome = "IOS" ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test34_SELECT_os_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection, 'SELECT id_OS FROM OS WHERE Nome = "ISO" ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) == 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 0)
            self.close_connection()

    def test35_CHANGE_OS(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query('UPDATE OS SET Nome="ANDROID" WHERE id_OS = 1')
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 < 1)
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test36_CHANGE_OS_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query('UPDATE OS SET Nome="ANDROID" WHERE id_OS = 7')
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 == 1)
        except Exception as e:
            self.assertTrue(0 < 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test37_DELETE_OS(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query('INSERT INTO OS (Nome) VALUES ("WindowsPhone")')
            self.send_query('COMMIT')
            self.send_query('START TRANSACTION')
            self.send_query('DELETE FROM OS WHERE Nome = "WindowsPhone"')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test38_SELECT_browser(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_browser FROM browser WHERE Nome = "Firefox" ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test39_SELECT_browser_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_browser FROM browser WHERE Nome = "Internet Explorer" ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) == 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 0)
            self.close_connection()

    def test40_CHANGE_BROWSER(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE browser SET Nome="DAVINCI" WHERE id_BROWSER = 4')
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 < 1)
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test41_CHANGE_BROWSER_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE browser SET Nome="ANDROID" WHERE id_OS = 7')
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 == 1)
        except Exception as e:
            self.assertTrue(0 < 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test42_DELETE_BROWSER(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'INSERT INTO browser (Nome) VALUES ("Internet Explorer")')
            self.send_query('COMMIT')
            self.send_query('START TRANSACTION')
            self.send_query(
                'DELETE FROM browser WHERE Nome = "Internet Explorer"')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test43_SELECT_VIU_POST(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_post FROM viu_post WHERE id_OS = 1 ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test44_SELECT_viu_post_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_post FROM viu_post WHERE id_OS = 4')
            a = ss.fetchall()
             
            self.assertTrue(len(a) == 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 0)
            self.close_connection()

    def test45_CHANGE_viu_post(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE viu_post SET id_OS=2 WHERE id_OS = 1 AND id_browser = 3 '
            )
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 < 1)
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test46_CHANGE_viu_post_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE viu_post SET id_OS=2 WHERE id_OS = 1 AND id_browser = 9'
            )
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 == 1)
        except Exception as e:
            self.assertTrue(0 < 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test47_DELETE_viu_post(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'DELETE FROM viu_post WHERE id_OS = 1 AND id_post = 2')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    


    def test48_SELECT_MENCIONA_PASSAROS(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_post FROM menciona_passaro WHERE id_passaro = 3 ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test49_SELECT_MENCIONA_PASSAROS_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_post FROM menciona_passaro WHERE id_passaro = 100 '
                )
            a = ss.fetchall()
             
            self.assertTrue(len(a) == 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 0)
            self.close_connection()

    def test50_CHANGE_MENCIONA_PASSAROS(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE menciona_passaro SET id_post=3 WHERE id_post = 2 AND id_passaro = 4 '
            )
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 < 1)
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test51_CHANGE_MENCIONA_PASSAROS_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE menciona_passaro SET id_post=3 WHERE id_post = 0 AND id_passaro = 9'
            )
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 == 1)
        except Exception as e:
            self.assertTrue(0 < 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test52_DELETE_MENCIONA_PASSAROS(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'DELETE FROM menciona_passaro WHERE id_post = 1 AND id_passaro = 3')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    

    def test53_SELECT_MENCIONA_USUARIO(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_post FROM menciona_usuario WHERE id_usuario = 3 ')
            a = ss.fetchall()
             
            self.assertTrue(len(a) > 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.close_connection()

    def test54_SELECT_MENCIONA_USUARIO_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            ss = DAO.run_db_query_with_return(
                self.connection,
                'SELECT id_post FROM menciona_usuario WHERE id_usuario = 100 '
                )
            a = ss.fetchall()
             
            self.assertTrue(len(a) == 0)
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 0)
            self.close_connection()

    def test55_CHANGE_MENCIONA_USUARIO(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE menciona_usuario SET id_post=3 WHERE id_post = 1 AND id_usuario = 2 '
            )
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 < 1)
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test56_CHANGE_MENCIONA_USUARIO_WRONG(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'UPDATE menciona_usuario SET id_post=3 WHERE id_post = 1 AND id_usuario = 29'
            )
            self.send_query('COMMIT')
            self.close_connection()
            self.assertTrue(0 == 1)
        except Exception as e:
            self.assertTrue(0 < 1)
            self.send_query('ROLLBACK')
            self.close_connection()

    def test57_DELETE_MENCIONA_USUARIO(self):
        try:
            self.assertTrue(self.mysql_open_connection())
            self.send_query('START TRANSACTION')
            self.send_query(
                'DELETE FROM menciona_usuario WHERE id_post = 1 AND id_usuario = 5')
            self.send_query('COMMIT')
            self.close_connection()
        except Exception as e:
            self.assertTrue(0 == 1)
            self.send_query('ROLLBACK')
            self.close_connection()



    


if __name__ == "__main__":
    unittest.main()
