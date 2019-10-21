import pymysql
import json
import datetime


def connectMYSQL():
    with open('acesso.json') as json_data:
        d = json.load(json_data)

        connection = pymysql.connect(host=d['connection']['host'],
                                     user=d['connection']['user'],
                                     password=d['connection']['password'],
                                     database=d['connection']['database'])

        return connection


#Cidade
def adiciona_cidade(conn, nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('START TRANSACTION')
            cursor.execute('INSERT INTO cidade (Nome) VALUES (%s)', (nome))
            cursor.execute('COMMIT')

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela cidade')
            cursor.execute('COMMIT')


def acha_cidade(conn, id_cidade):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM cidade WHERE id_cidade = %s',
                       (id_cidade))
        row_headers = [x[0] for x in cursor.description]
        res = cursor.fetchone()
        dict_user = {}
        if res:
            assa = dict(zip(row_headers, res))
            return assa
        else:
            return None


def muda_nome_cidade(conn, id, novo_nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute('UPDATE cidade SET Nome=%s where id_cidade=%s',
                           (novo_nome, id))
            cursor.execute("COMMIT")
        except pymysql.err.IntegrityError as e:
            cursor.execute("ROLLBACK")
            raise ValueError(
                f'Não posso alterar nome do id {id} para {novo_nome} na tabela perigo'
            )


def remove_cidade(conn, id):
    with conn.cursor() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute('DELETE FROM cidade WHERE id_cidade=%s', (id))
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(e)


def lista_cidade(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from cidade')
        res = cursor.fetchall()
        dict_users = {}
        for i in res:
            dict_users[i[0]] = i[1]

        return dict_users


# Usuario
def adiciona_usuario(conn, nome, email, id_cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute('CALL add_user (%s,%s,%s)' ,
                           (nome, email, id_cidade))
            cursor.execute("COMMIT")
        except pymysql.err.IntegrityError as e:
            cursor.execute("COMMIT")
            raise ValueError(f'Não posso inserir na tabela usuario')


def acha_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s',
                       (id_usuario))

        row_headers = [x[0] for x in cursor.description]
        res = cursor.fetchone()
        dict_user = {}
        assa = dict(zip(row_headers, res))
        if res:
            return assa
        else:
            return None


def muda_dados_usuario(conn, id, novo_nome, novo_email, nova_cidade, ativo):
    with conn.cursor() as cursor:
        try:
            if (novo_nome != None):
                cursor.execute("START TRANSACTION")
                cursor.execute(
                    'UPDATE usuario SET Nome=%s where id_usuario=%s',
                    (novo_nome, id))
                cursor.execute("COMMIT")

            if (novo_email != None):
                cursor.execute("START TRANSACTION")
                cursor.execute(
                    'UPDATE usuario SET Email=%s where id_usuario=%s',
                    (novo_email, id))
                cursor.execute("COMMIT")

            if (nova_cidade != None):
                cursor.execute("START TRANSACTION")
                cursor.execute(
                    'UPDATE usuario SET id_cidade="%s" where id_usuario=%s',
                    (nova_cidade, id))
                cursor.execute("COMMIT")

            if (ativo != None):
                cursor.execute("START TRANSACTION")
                cursor.execute(
                    'UPDATE usuario SET ativo=%s where id_usuario=%s',
                    (ativo, id))
                cursor.execute("COMMIT")
        except pymysql.err.IntegrityError as e:
            cursor.execute("ROLLBACK")
            raise ValueError(
                f'Não posso alterar nome do id {id} para {novo_nome} na tabela usuario'
            )


def remove_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM usuario WHERE id_usuario=%s', (id))


def lista_usuario(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario,Nome from usuario')
        res = cursor.fetchall()
        dict_users = {}
        for i in res:
            dict_users[i[0]] = i[1]

        return dict_users


#Passaros
def adiciona_passaro(conn, nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute('INSERT INTO passaro (Nome) VALUES (%s)', (nome))
            cursor.execute("COMMIT")
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela passaro')
            cursor.execute("ROLLBACK")


def acha_passaro(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM passaro WHERE id_passaro = %s', (nome))
        row_headers = [x[0] for x in cursor.description]
        res = cursor.fetchone()
        dict_user = {}
        if res:
            assa = dict(zip(row_headers, res))
            return assa
        else:
            return None


def muda_nome_passaro(conn, id, novo_nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute('UPDATE passaro SET Nome=%s where id_passaro=%s',
                           (novo_nome, id))
            cursor.execute("COMMIT")
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso alterar nome do id {id} para {novo_nome} na tabela passaro'
            )
            cursor.execute("ROLLBACK")


def remove_passaro(conn, id):
    with conn.cursor() as cursor:
        cursor.execute("START TRANSACTION")
        cursor.execute('DELETE FROM passaro WHERE id_passaro=%s', (id))
        cursor.execute("COMMIT")


def lista_passaro(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from passaro')
        res = cursor.fetchall()
        dict_users = {}
        for i in res:
            dict_users[i[0]] = i[1]
        return dict_users


#POST
def adiciona_post(conn, titulo, imagem, texto, creator_id):
    with conn.cursor() as cursor:
        a = "o"
        cursor.execute(
            "select id_post from post ORDER BY id_post DESC LIMIT 1")
        rs = cursor.fetchone()

        if rs:
            print(rs[0])
            rs = rs[0]
        else:
            rs = 0
        cursor.execute('START TRANSACTION')
        try:
            cursor.execute('CALL add_post("%s","%s","%s",%d)' %
                           (titulo, imagem, texto, creator_id))
            cursor.execute('COMMIT')
            cursor.execute('START TRANSACTION')
            for ww in texto.split():
                if (ww[0] == "#"):
                    cursor.execute('CALL tag_bird(%d,%d)' %
                                   (int(ww[1:]), rs + 1))
                elif (ww[0] == "@"):
                    cursor.execute('CALL tag_user(%d,%d)' %
                                   (int(ww[1:]), rs + 1))
            cursor.execute('COMMIT')

            return True
        except Exception as e:
            print(e)

            cursor.execute('ROLLBACK')
            raise ValueError(a)


def acha_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM post WHERE id_post = %s', (id_post))
        row_headers = [x[0] for x in cursor.description]
        res = cursor.fetchone()
        dict_user = {}
        if res:
            assa = dict(zip(row_headers, res))
            return assa
        else:
            return None


def muda_dados_post(conn,
                    id,
                    novo_titulo=None,
                    nova_imagem=None,
                    novo_texto=None,
                    ativo=None):
    with conn.cursor() as cursor:
        cursor.execute("START TRANSACTION")
        try:
            if (novo_titulo != None):
                cursor.execute('UPDATE post SET Titulo=%s where id_post=%s',
                               (novo_titulo, id))

            if (nova_imagem != None):
                cursor.execute('UPDATE post SET Imagem=%s where id_post=%s',
                               (nova_imagem, id))

            if (novo_texto != None):
                apaga_referencias_de_um_post(conn, id)
                cursor.execute('UPDATE post SET Texto=%s where id_post=%s',
                               (novo_texto, id))

                for ww in novo_texto.split():
                    if (ww[0] == "#"):
                        cursor.execute('CALL tag_bird(%d,%d)' %
                                       (int(ww[1:]), id))
                    elif (ww[0] == "@"):
                        cursor.execute('CALL tag_user(%d,%d)' %
                                       (int(ww[1:]), id))

            if (ativo != None):
                cursor.execute('UPDATE post SET ativo=%s where id_post=%s',
                               (ativo, id))
            cursor.execute("COMMIT")
        except pymysql.err.IntegrityError as e:
            cursor.execute("ROLLBACK")
            raise ValueError(
                f'Não posso alterar nome do id {id} para {novo_nome} na tabela usuario'
            )


def remove_post(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('START TRANSACTION')
        cursor.execute('UPDATE post SET ativo=0 WHERE id_post=%s', (id))
        cursor.execute('COMMIT')


def lista_post(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from post WHERE ativo = 1')
        res = cursor.fetchall()
        dict_users = {}
        for i in res:
            dict_users[i[0]] = i[1]
        return dict_users


def lista_post_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT * from post WHERE ativo = 1 AND id_usuario=%s ORDER BY id_post DESC',
            (id_usuario))
        res = cursor.fetchall()
        dict_users = {}
        for i in res:
            dict_users[i[0]] = i[1]
        return dict_users


def visu_post(conn, id_usuario, id_post, OS, BROWSER, IP, horario=None):
    with conn.cursor() as cursor:
        try:
            a = 0
            cursor.execute("SELECT id_browser from browser WHERE Nome=(%s)",
                           (BROWSER))
            res = cursor.fetchone()
            if res:
                browser_id = res[0]
            else:
                cursor.execute("START TRANSACTION")
                cursor.execute("INSERT INTO browser (Nome) VALUES (%s)",
                               (BROWSER))
                cursor.execute("COMMIT")
                cursor.execute(
                    "SELECT id_browser from browser WHERE Nome=(%s)",
                    (BROWSER))
                res = cursor.fetchone()[0]
                browser_id = res

            cursor.execute("SELECT id_OS from OS WHERE Nome=(%s)", (OS))
            res = cursor.fetchone()
            if res:
                os_id = res[0]
            else:
                cursor.execute("START TRANSACTION")
                cursor.execute("INSERT INTO OS (Nome) VALUES (%s)", (OS))
                cursor.execute("COMMIT")
                cursor.execute("SELECT id_OS from OS WHERE Nome=(%s)", (OS))
                res = cursor.fetchone()[0]
                os_id = res

            cursor.execute("START TRANSACTION")
            a = 1
            cursor.execute(
                "INSERT INTO viu_post (id_usuario,id_post,id_OS,id_browser,IP) VALUES (%d,%d,%d,%d,%s)"
                % (int(id_usuario), int(id_post), int(os_id), int(browser_id),
                   IP))
            a = 2
            cursor.execute("COMMIT")

        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK")
            raise ValueError("ERRO", e, " \nJUMP: ", a)


#REFERENCIAS DO POST


def apaga_referencias_de_um_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute("START TRANSACTION")
        cursor.execute('UPDATE menciona_passaro SET ativo = 0 WHERE id_post=%s',
                       (id_post))
        cursor.execute('UPDATE menciona_usuario SET ativo = 0 WHERE id_post=%s',
                       (id_post))
        cursor.execute("COMMIT")

#PREFERENCIA

def adiciona_preferencia(conn,id_usuario,id_passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("CALL add_preference (%d,%d)"%(id_usuario,id_passaro))
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(e)

#JOINHAS

def adiciona_joinhas(conn,id_post,id_usuario,joinha):
    with conn.cursor() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("CALL add_opinion (%d,%d,%d)"%(id_usuario,id_post,joinha))
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(e)

def altera_joinhas(conn,id_post,id_usuario,joinha):
    with conn.cursor() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("UPDATE joinha SET joinha = %d  WHERE id_post = %d AND id_usuario = %d"%(joinha,id_post,id_usuario))
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(e)

def apaga_joinhas(conn,id_post,id_usuario,joinha=None):
    with conn.cursor() as cursor:
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("DELETE FROM joinha WHERE id_post=%s and id_usuario" % (id_post,id_usuario))
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(e)

#popular de cidade
def popular_cidade(conn,id_cidade):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_usuario FROM usuario WHERE id_cidade = %d" % (id_cidade))
        rs = cursor.fetchall()
        id_usuario = 0
        valor_usuario = 0
        for ss in rs:
            cursor.execute("SELECT SUM(joinha.joinha) FROM post INNER JOIN joinha ON joinha.id_post = post.id_post WHERE post.id_usuario = %d" % (ss[0]))
            res = cursor.fetchone()
            if(res[0]):
                if(res[0] > valor_usuario):
                    id_usuario = ss[0]
        return id_usuario

#usuario_referencia_usuario
def usuario_referencia_usuario(conn,id_usuario):
    with conn.cursor() as cursor:
        cursor.execute("SELECT post.id_usuario FROM post INNER JOIN menciona_usuario ON post.id_post = menciona_usuario.id_post WHERE menciona_usuario.id_usuario = %d" % (id_usuario))
        res = cursor.fetchall()
        deict = {}
        for i in range(len(res)):
            deict[i] = {"usuario" : res[i][0]}
        return deict

def passaro_imagem(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT post.Imagem,id_passaro  FROM post INNER JOIN menciona_passaro ON post.id_post = menciona_passaro.id_post")
        res = cursor.fetchall()
        
        
        return res

