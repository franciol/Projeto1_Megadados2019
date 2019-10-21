import requests
import unittest
import json
import subprocess
import os

base_link = "http://127.0.0.1:8000/"


class TestCase(unittest.TestCase):
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

    def test00_add_cidade(self):
        res = requests.post(base_link + "cidade", json={"nome": "São Paulo"})
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "cidade", json={"nome": "São Carlos"})
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "cidade", json={"nome": "Americana"})
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "cidade",
                            json={"nome": "São José dos Campos"})
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "cidade", json={"nome": "Toronto"})
        print(res)
        self.assertTrue(res)

    def test01_add_usuario(self):
        res = requests.post(base_link + "usuario",
                            json={
                                "nome": "Pedro",
                                "email": "Pp@gmail.ccom",
                                "id_cidade": 1
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "usuario",
                            json={
                                "nome": "Paulo",
                                "email": "paa@gmail.ccom",
                                "id_cidade": 2
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "usuario",
                            json={
                                "nome": "Giovana",
                                "email": "gg@gmail.ccom",
                                "id_cidade": 4
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "usuario",
                            json={
                                "nome": "Julia",
                                "email": "jj@NOPE.ccom",
                                "id_cidade": 3
                            })
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "usuario",
                            json={
                                "nome": "Maria",
                                "email": "jj@NOPE.ccom",
                                "id_cidade": 1
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "usuario",
                            json={
                                "nome": "Godofredo",
                                "email": "jj@NOPE.ccom",
                                "id_cidade": 1
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "usuario",
                            json={
                                "nome": "Kermel",
                                "email": "jj@NOPE.ccom",
                                "id_cidade": 1
                            })
        print(res)
        self.assertTrue(res)

    def test02_add_passaro(self):
        res = requests.post(base_link + "passaro", json={"nome": "Cacatua"})
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "passaro", json={"nome": "Aguia"})
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "passaro", json={"nome": "Ganso"})
        print(res)
        self.assertTrue(res)

    def test03_add_post(self):
        res = requests.post(base_link + "post",
                            json={
                                "titulo": "Aí sim, ola isso",
                                "imagem": "img.im",
                                "texto": "@3 olha esse #1 no meu quintal",
                                "id_usuario": 2
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "post",
                            json={
                                "titulo": "Aí sim, olha lá",
                                "imagem": "img.ima",
                                "texto": "@2 olha esse #3 no meu quintal",
                                "id_usuario": 1
                            })
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "post",
                            json={
                                "titulo": "Meu DEUS",
                                "imagem": "issmg.im",
                                "texto": "@2 olha esse #2 no meu quintal",
                                "id_usuario": 2
                            })
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "post",
                            json={
                                "titulo": "Meu DEUS",
                                "imagem": "imgaaa.im",
                                "texto": "@2 olha esse #2 no meu quintal",
                                "id_usuario": 3
                            })
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "post",
                            json={
                                "titulo": "Meu DEUS",
                                "imagem": "oiasj.im",
                                "texto": "@2 olha esse #2 no meu quintal",
                                "id_usuario": 1
                            })
        print(res)
        self.assertTrue(res)

    def test04_add_viu(self):
        res = requests.post(base_link + "visualizacao",
                            json={
                                "id_usuario": 2,
                                "id_post": 1,
                                "OS": "ANDROID",
                                "BROWSER": "CHROME",
                                "IP": "192.168.124.1"
                            })
        print(res)
        self.assertTrue(res)
    
        res = requests.post(base_link + "visualizacao",
                            json={
                                "id_usuario": 3,
                                "id_post": 1,
                                "OS": "IOs",
                                "BROWSER": "SAFARI",
                                "IP": "192.168.124.1"
                            })
        print(res)
        self.assertTrue(res)
    
        res = requests.post(base_link + "visualizacao",
                            json={
                                "id_usuario": 5,
                                "id_post": 1,
                                "OS": "IOs",
                                "BROWSER": "CHROME",
                                "IP": "192.168.124.1"
                            })
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "visualizacao",
                            json={
                                "id_usuario": 4,
                                "id_post": 1,
                                "OS": "ANDROID",
                                "BROWSER": "FIREFOX",
                                "IP": "192.168.124.1"
                            })
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "visualizacao",
                            json={
                                "id_usuario": 4,
                                "id_post": 2,
                                "OS": "ANDROID",
                                "BROWSER": "FIREFOX",
                                "IP": "192.168.124.1"
                            })
        print(res)
        self.assertTrue(res)

        
    def test05_adiciona_preferencia(self):
        res = requests.post(base_link + "preferencia",
                            json={
                                "id_usuario": 2,
                                "id_passaro": 2
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "preferencia",
                            json={
                                "id_usuario": 4,
                                "id_passaro": 1
                            })
        print(res)
        self.assertTrue(res)

    def test06_add_joinhas(self):
        res = requests.post(base_link + "likes",
                            json={
                                "id_usuario": 4,
                                "id_post": 1,
                                "joinha": 1
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "likes",
                            json={
                                "id_usuario": 2,
                                "id_post": 2,
                                "joinha": 0
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "likes",
                            json={
                                "id_usuario": 3,
                                "id_post": 2,
                                "joinha": 1
                            })
        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "likes",
                            json={
                                "id_usuario": 4,
                                "id_post": 2,
                                "joinha": 1
                            })
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "likes",
                            json={
                                "id_usuario": 5,
                                "id_post": 2,
                                "joinha": 1
                            })
        print(res)
        self.assertTrue(res)

        res = requests.post(base_link + "likes",
                            json={
                                "id_usuario": 6,
                                "id_post": 2,
                                "joinha": 1
                            })

        print(res)
        self.assertTrue(res)
        res = requests.post(base_link + "likes",
                            json={
                                "id_usuario": 6,
                                "id_post": 1,
                                "joinha": 1
                            })

        print(res)
        self.assertTrue(res)

    def test07_listar_posts_usuario(self):
        res = requests.get(base_link + "post/user/1")
        print(res)
        self.assertTrue(res)

    def test08_listar_usuario_popular(self):
        res = requests.get(base_link + "popular/1")
        print(res)
        print(res.json())

        self.assertTrue(res)

    def test09_listar_usuario_que_referencia(self):
        res = requests.get(base_link + "usuario/usuario/2")
        print(res.json())
        self.assertTrue(res)

    def test10_listar_passaro_imagem(self):
        res = requests.get(base_link + "passaro/imagem/")
        print(res)
        self.assertTrue(res)

    def test11_add_bio(self):
        res = requests.post(base_link + "usuario/bio/",
                            json={
                                "id_usuario": 1,
                                "Nome_completo": "Pedro Almeida Santos",
                                "Foto_perfil": "foto_perfil.com",
                                "Descricao": "Tímido e sorrateiro"
                            })

        print(res)
        self.assertTrue(res)

    def test12_ver_tabela(self):
        res = requests.get(base_link + "visualizacao/dados/")
        print(res.json())
        self.assertTrue(res)

if __name__ == "__main__":
    unittest.main()