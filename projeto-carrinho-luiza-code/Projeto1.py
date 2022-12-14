from fastapi import FastAPI
from typing import List
from pydantic import BaseModel


app = FastAPI()

OK = "OK"
FALHA = "FALHA"


# ============================================
#  Estrutura de classes / Pydantic
# ============================================

# Classe representando os dados do endereço do cliente
class Endereco(BaseModel):
    rua: str
    cep: str
    cidade: str
    estado: str


# Classe representando os dados do cliente
class Usuario(BaseModel):
    # id: int
    nome: str
    email: str
    senha: str


# Classe representando a lista de endereços de um cliente
class ListaDeEnderecosDoUsuario(BaseModel):
    usuario: Usuario
    enderecos: List[Endereco] = []


# Classe representando os dados do produto
class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float


# Classe representando o carrinho de compras de um cliente com uma lista de produtos
class CarrinhoDeCompras(BaseModel):
    id_usuario: int
    id_produtos: List[Produto] = []
    preco_total: float
    quantidade_de_produtos: int


# ============================================
#  Dicionários
# ============================================
db_usuarios = []
db_produtos = {}
db_end = {}        # enderecos_dos_usuarios
db_carrinhos = {}


def persistencia_criar_usuario(novo_usuario):
    codigo_novo_usuario = len(db_usuarios) + 1
    novo_usuario["codigo"] = codigo_novo_usuario
    db_usuarios.append(novo_usuario)
    return novo_usuario


def persistencia_usuario_pesquisar_pelo_codigo(codigo):
    usuario_id_procurado = None
    for usuario in db_usuarios:
        if usuario["codigo"] == codigo:
            usuario_id_procurado = usuario
            break
    return usuario_id_procurado


def persistencia_usuario_pesquisar_pelo_nome(nome: str):
    usuario_nome_procurado = None
    for usuario in db_usuarios:
        if usuario.index(nome):
            usuario_nome_procurado = usuario
            break
        return usuario_nome_procurado


# ============================================
#  Regras
# ============================================
def regras_criar_usuario(novo_usuario):
    novo_usuario = persistencia_criar_usuario(novo_usuario)
    return novo_usuario


def regras_usuario_pesquisar_pelo_codigo(codigo):
    return persistencia_usuario_pesquisar_pelo_codigo(codigo)


def regras_usuario_pesquisar_pelo_nome(nome: str):
    return persistencia_usuario_pesquisar_pelo_nome(nome)
    

# ============================================
#  API Rest / Controladores
# ============================================
# Criar um usuário,
# se tiver outro usuário com o mesmo ID retornar falha, 
# se o email não tiver o @ retornar falha, 
# senha tem que ser maior ou igual a 3 caracteres, 
# senão retornar OK
@app.post("/usuarios")
async def criar_usuario(novo_usuario: Usuario):
    print("Registrando um novo usuário ", novo_usuario.dict())
    novo_usuario = regras_criar_usuario(novo_usuario.dict())
    return novo_usuario   


# Se o id do usuário existir, retornar os dados do usuário
# senão retornar falha
@app.get("/usuarios/{codigo}")
async def retornar_usuario(codigo: int):
    print("Informe o códio do usuário: ", codigo)
    return regras_usuario_pesquisar_pelo_codigo(codigo)    
    # if id in db_usuarios:
    #     return db_usuarios[id]
    # return FALHA


# Se existir um usuário com exatamente o mesmo nome, retornar os dados do usuário
# senão retornar falha
@app.get("/usuarios/{nome}")
async def retornar_usuario_com_nome(nome: str):
    print("Informe o nome do usuário: ", nome)
    return regras_usuario_pesquisar_pelo_nome(nome)
    # if nome in db_usuarios:
    #     return db_usuarios[nome]
    # return FALHA


# Se o id do usuário existir, deletar o usuário e retornar OK
# senão retornar falha
# ao deletar o usuário, deletar também endereços e carrinhos vinculados a ele
@app.delete("/usuario/")
async def deletar_usuario(id: int):
    return FALHA


# Se não existir usuário com o id_usuario retornar falha, 
# senão retornar uma lista de todos os endereços vinculados ao usuário
# caso o usuário não possua nenhum endereço vinculado a ele, retornar 
# uma lista vazia
### Estudar sobre Path Params (https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/usuario/{id_usuario}/enderecos/")
async def retornar_enderecos_do_usuario(id_usuario: int):
    return FALHA


# Retornar todos os emails que possuem o mesmo domínio
# (domínio do email é tudo que vêm depois do @)
# senão retornar falha
@app.get("/usuarios/emails/")
async def retornar_emails(dominio: str):
    return FALHA


# Se não existir usuário com o id_usuario retornar falha, 
# senão cria um endereço, vincula ao usuário e retornar OK
@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: Endereco, id_usuario: int):
    return OK


# Se não existir endereço com o id_endereco retornar falha, 
# senão deleta endereço correspondente ao id_endereco e retornar OK
# (lembrar de desvincular o endereço ao usuário)
@app.delete("/endereco/{id_endereco}/")
async def deletar_endereco(id_endereco: int):
    return OK


# Se tiver outro produto com o mesmo ID retornar falha,
# senão cria um produto e retornar OK
@app.post("/produto/")
async def criar_produto(produto: Produto):
    return OK


# Se não existir produto com o id_produto retornar falha, 
# senão deleta produto correspondente ao id_produto e retornar OK
# (lembrar de desvincular o produto dos carrinhos do usuário)
@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    return OK


# Se não existir usuário com o id_usuario ou id_produto retornar falha, 
# se não existir um carrinho vinculado ao usuário, crie o carrinho
# e retornar OK
# senão adiciona produto ao carrinho e retornar OK
@app.post("/carrinho/{id_usuario}/{id_produto}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int):
    return OK


# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o carrinho de compras.
@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
    return CarrinhoDeCompras


# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o o número de itens e o valor total do carrinho de compras.
@app.get("/carrinho/{id_usuario}/")
async def retornar_total_carrinho(id_usuario: int):
    numero_itens, valor_total = 0
    return numero_itens, valor_total


# Se não existir usuário com o id_usuario retornar falha, 
# senão deleta o carrinho correspondente ao id_usuario e retornar OK
@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    return OK


@app.get("/")
async def bem_vinda():
    site = "Seja bem vinda"
    return site.replace('\n', '')
