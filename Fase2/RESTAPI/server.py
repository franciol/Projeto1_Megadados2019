from fastapi import FastAPI
import projeto as pj
from pydantic import BaseModel
import datetime


class user(BaseModel):
    nome: str = None
    email: str = None
    id_cidade: int = None
    ativo: int = None

class prefere(BaseModel):
    id_usuario: int = None
    id_passaro: int = None

class city(BaseModel):
    nome: str = None

class joinha(BaseModel):
    id_post : int
    id_usuario : int
    joinha : int

class post(BaseModel):
    titulo: str = None
    imagem: str = None
    texto: str = None
    id_usuario: int = None
    ativo: int = None

class visualizacao(BaseModel):
    id_usuario: int = None
    id_post : int = None
    OS : str = None
    BROWSER : str = None
    IP : str = "127.0.0.1"
    horario : type(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class bio(BaseModel):
    id_usuario: int
    Nome_completo : str
    Foto_perfil : str
    Descricao : str

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"Hello World"}

# USUARIOS
@app.get('/usuario')
async def listar_usuarios():
    conn = pj.connectMYSQL()
    users = pj.lista_usuario(conn)
    conn.close()
    return users


@app.get('/usuario/{id_usuario}')
async def listar_usuarios(id_usuario: int):
    conn = pj.connectMYSQL()
    users = pj.acha_usuario(conn, id_usuario)
    conn.close()
    return users


@app.post('/usuario')
async def adicionar_usuario(usuario: user):
    conn = pj.connectMYSQL()
    pj.adiciona_usuario(conn, usuario.nome, usuario.email, usuario.id_cidade)
    conn.close()


@app.delete('/usuario/{id_usuario}')
async def deletar_usuario(id_usuario: int):
    conn = pj.connectMYSQL()
    pj.remove_usuario(conn, id_usuario)
    conn.close()


@app.patch('/usuario/{id_usuario}')
async def muda_dados_usuario(usuario: user, id_usuario: int = None):
    conn = pj.connectMYSQL()

    pj.muda_dados_usuario(conn, id_usuario, usuario.nome, usuario.email,
                          usuario.id_cidade, usuario.ativo)
    conn.close()


# CIDADE
@app.get('/cidade')
async def lista_cidade():
    conn = pj.connectMYSQL()
    users = pj.lista_cidade(conn)
    conn.close()
    return users


@app.get('/cidade/{id_cidade}')
async def listar_cidade(id_cidade: int):
    conn = pj.connectMYSQL()
    users = pj.acha_cidade(conn, id_cidade)
    conn.close()
    return users


@app.post('/cidade')
async def adicionar_usuario(cidade: city):
    conn = pj.connectMYSQL()
    pj.adiciona_cidade(conn, cidade.nome)
    conn.close()


@app.delete('/cidade/{id_cidade}')
async def deletar_usuario(id_cidade: int):
    conn = pj.connectMYSQL()
    pj.remove_cidade(conn, id_cidade)
    conn.close()


@app.patch('/cidade/{id_cidade}')
async def muda_dados_usuario(cidade: city, id_cidade: int = None):
    conn = pj.connectMYSQL()
    pj.muda_nome_cidade(conn, id_cidade, cidade.nome)
    conn.close()


#PASSAROS
@app.get('/passaro')
async def lista_cidade():
    conn = pj.connectMYSQL()
    users = pj.lista_passaro(conn)
    conn.close()
    return users


@app.get('/passaro/{id_passaro}')
async def listar_cidade(id_passaro: int):
    conn = pj.connectMYSQL()
    users = pj.acha_passaro(conn, id_passaro)
    conn.close()
    return users


@app.post('/passaro')
async def adicionar_usuario(cidade: city):
    conn = pj.connectMYSQL()
    pj.adiciona_passaro(conn, cidade.nome)
    conn.close()


@app.delete('/passaro/{id_passaro}')
async def deletar_usuario(id_passaro: int):
    conn = pj.connectMYSQL()
    pj.remove_passaro(conn, id_passaro)
    conn.close()


@app.patch('/passaro/{id_passaro}')
async def muda_dados_usuario(passaro: city, id_passaro: int = None):
    conn = pj.connectMYSQL()
    pj.muda_nome_passaro(conn, id_passaro, passaro.nome)
    conn.close()


#POST
@app.get('/post')
async def lista_post():
    conn = pj.connectMYSQL()
    users = pj.lista_post(conn)
    conn.close()
    return users

@app.get('/post/user/{id_usuario}')
async def lista_post(id_usuario: int):
    conn = pj.connectMYSQL()
    users = pj.lista_post_usuario(conn,id_usuario)
    conn.close()
    return users


@app.get('/post/{id_post}')
async def listar_cidade(id_post: int):
    conn = pj.connectMYSQL()
    users = pj.acha_post(conn, id_post)
    conn.close()
    return users


@app.post('/post')
async def adicionar_post(post: post):
    conn = pj.connectMYSQL()
    pj.adiciona_post(conn, post.titulo, post.imagem, post.texto,
                     post.id_usuario)
    conn.close()


@app.delete('/post/{id_post}')
async def deletar_post(id_post: int):
    conn = pj.connectMYSQL()
    pj.remove_post(conn, id_post)
    conn.close()


@app.patch('/post/{id_post}')
async def muda_dados_usuario(post: post, id_post: int = None):
    conn = pj.connectMYSQL()
    pj.muda_dados_post(conn, id_post, post.titulo, post.imagem, post.texto,
                       post.ativo)
    conn.close()

#VISUALIZACAO
@app.post('/visualizacao')
async def visu_post(visu: visualizacao):
    conn = pj.connectMYSQL()
    pj.visu_post(conn, visu.id_usuario, visu.id_post, visu.OS, visu.BROWSER, visu.IP)
    conn.close() 

#PREFERENCIA
@app.post('/preferencia')
async def preferencia_add(prefere: prefere):
    conn = pj.connectMYSQL()
    pj.adiciona_preferencia(conn,prefere.id_usuario,prefere.id_passaro)
    conn.close()



#JOINHAS
@app.post("/likes")
async def add_joinhas(joinha: joinha):
    conn = pj.connectMYSQL()
    pj.adiciona_joinhas(conn,joinha.id_post,joinha.id_usuario,joinha.joinha)
    conn.close()

@app.patch("/likes")
async def change_joinhas(joinha: joinha):
    conn = pj.connectMYSQL()
    pj.muda_joinhas(conn,joinha.id_post,joinha.id_usuario,joinha.joinha)
    conn.close()

@app.delete("/likes")
async def apaga_joinhas(joinha: joinha):
    conn = pj.connectMYSQL()
    pj.apaga_joinhas(conn,joinha.id_post,joinha.id_usuario)
    conn.close()

#USUARIO + POPULAR
@app.get("/popular/{id_cidade}")
async def pop_cidade(id_cidade: int):
    conn = pj.connectMYSQL()
    a = pj.popular_cidade(conn,id_cidade)
    conn.close()
    dd = {"id_usuario" : a}
    return dd

#USUARIOS Q REFEREM OUTRO 
@app.get("/usuario/usuario/{id_usuario}")
async def pop_cidade(id_usuario: int):
    conn = pj.connectMYSQL()
    a = pj.usuario_referencia_usuario(conn,id_usuario)
    conn.close()
    return a

#PASSARO IMAGEM
@app.get('/passaro/imagem/')
async def lista_imagem_passaros():
    conn = pj.connectMYSQL()
    a = pj.passaro_imagem(conn)
    conn.close()
    return a

#ADD BIO
@app.post("/usuario/bio/")
async def add_bio(bio: bio):
    conn = pj.connectMYSQL()
    pj.add_bio(conn, bio.id_usuario, bio.Nome_completo, bio.Foto_perfil, bio.Descricao)
    conn.close()
    

#PEGAR TABELA VISUALIZACAO TIPO
@app.get("/visualizacao/dados/")
async def dados_visu():
    conn = pj.connectMYSQL()
    a = pj.dados_visu(conn)
    conn.close()
    return a
    
