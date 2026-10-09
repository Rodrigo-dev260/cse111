from pydantic import BaseModel, Field, field_validator
import sqlite3
import os
import requests

from fastapi import FastAPI

app = FastAPI()

PASTA_PROJETO = os.path.dirname(
    os.path.abspath(__file__)
)

BANCO = os.getenv(
    "BANCO_SQLITE",
    os.path.join(
        PASTA_PROJETO,
        "estoque_teste.db"
    )
)

def proteger_nomes_duplicados():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_produtos_nome_unico
        ON produtos (LOWER(nome))
    """)

    conexao.commit()
    conexao.close()

proteger_nomes_duplicados()

def adicionar_coluna_ativo():
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("PRAGMA table_info(produtos)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    if "ativo" not in colunas:
        cursor.execute(
            "ALTER TABLE produtos ADD COLUMN ativo INTEGER NOT NULL DEFAULT 1"
        )
        conexao.commit()

    conexao.close()


adicionar_coluna_ativo()

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ProdutoNovo(BaseModel):
    nome: str = Field(min_length=1)
    quantidade: int = Field(ge=0)
    data_validade: str
    categoria: Literal["Estocável", "Congelado"]

    @field_validator("nome")
    @classmethod
    
    def validar_nome(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("O nome não pode estar vazio.")

        return valor

    @field_validator("data_validade")
    @classmethod
    
    def validar_validade(cls, valor):
        try:
            datetime.strptime(valor, "%d/%m/%Y")
        except ValueError:
            raise ValueError(
                "Data inválida. Use DD/MM/AAAA."
            )

        return valor

class MovimentacaoNova(BaseModel):
    quantidade: int = Field(gt=0)


@app.get("/")
def pagina_inicial():
    return {
        "mensagem": "API do Controle de Estoque funcionando!"
    }


@app.get("/produtos")
def consultar_produtos():

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, 
        nome, 
        quantidade, 
        data_validade, 
        categoria
        FROM produtos
        WHERE ativo = 1
    """)

    registros = cursor.fetchall()

    conexao.close()

    produtos = []

    for registro in registros:
        produtos.append({
            "id": registro[0],
            "nome": registro[1],
            "quantidade": registro[2],
            "data_validade": registro[3],
            "categoria": registro[4]
        })

    return produtos
from fastapi import HTTPException


@app.get("/produtos/{produto_id}")
def consultar_produto(produto_id: int):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, 
        nome, 
        quantidade, 
        data_validade, 
        categoria
        FROM produtos
        WHERE id = ? AND ativo = 1
    """, (produto_id,))

    produto = cursor.fetchone()
    conexao.close()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return {
        "id": produto[0],
        "nome": produto[1],
        "quantidade": produto[2],
        "data_validade": produto[3],
        "categoria": produto[4]
    }

@app.post("/produtos", status_code=201)
def cadastrar_produto(produto: ProdutoNovo):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO produtos (
                nome,
                quantidade,
                data_validade,
                categoria
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                produto.nome,
                produto.quantidade,
                produto.data_validade,
                produto.categoria
            )
        )

        conexao.commit()
        novo_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        conexao.rollback()

        raise HTTPException(
            status_code=409,
            detail="Produto já cadastrado."
        )

    finally:
        conexao.close()
    return {
        "mensagem": "Produto cadastrado com sucesso!",
        "id": novo_id
    }

@app.put("/produtos/{produto_id}")
def editar_produto(produto_id: int, produto: ProdutoNovo):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id
        FROM produtos
        WHERE id = ? AND ativo = 1
        """,
        (produto_id,)
    )

    existente = cursor.fetchone()

    if existente is None:
        conexao.close()
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    try:
        cursor.execute(
            """
            UPDATE produtos
            SET nome = ?,
                quantidade = ?,
                data_validade = ?,
                categoria = ?
            WHERE id = ?
            """,
            (
                produto.nome,
                produto.quantidade,
                produto.data_validade,
                produto.categoria,
                produto_id
            )
        )

        conexao.commit()

    except sqlite3.IntegrityError:
        conexao.rollback()
        raise HTTPException(
            status_code=409,
            detail="Já existe outro produto com esse nome."
        )

    finally:
        conexao.close()

    return {
        "mensagem": "Produto atualizado com sucesso!",
        "id": produto_id
    }

@app.delete("/produtos/{produto_id}")
def desativar_produto(produto_id: int):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE produtos
        SET ativo = 0
        WHERE id = ? AND ativo = 1
        """,
        (produto_id,)
    )

    conexao.commit()
    alterados = cursor.rowcount
    conexao.close()

    if alterados == 0:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado ou já desativado."
        )

    return {
        "mensagem": "Produto desativado com sucesso!",
        "id": produto_id
    }

@app.get("/movimentacoes")
def consultar_movimentacoes():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            produto_id,
            produto_nome,
            tipo,
            quantidade,
            saldo,
            data_hora
        FROM movimentacoes
        ORDER BY id DESC
    """)

    registros = cursor.fetchall()
    conexao.close()

    movimentacoes = []

    for registro in registros:
        movimentacoes.append({
            "id": registro[0],
            "produto_id": registro[1],
            "produto_nome": registro[2],
            "tipo": registro[3],
            "quantidade": registro[4],
            "saldo": registro[5],
            "data_hora": registro[6]
        })

    return movimentacoes

@app.post("/produtos/{produto_id}/entrada")
def registrar_entrada(produto_id: int, movimentacao: MovimentacaoNova):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    try:
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute("""
            SELECT nome, quantidade
            FROM produtos
            WHERE id = ? AND ativo = 1
        """, (produto_id,))

        produto = cursor.fetchone()

        if produto is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado ou desativado."
            )

        nome, saldo_atual = produto
        novo_saldo = saldo_atual + movimentacao.quantidade

        cursor.execute("""
            UPDATE produtos
            SET quantidade = ?
            WHERE id = ?
        """, (novo_saldo, produto_id))

        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        cursor.execute("""
            INSERT INTO movimentacoes (
                produto_id,
                produto_nome,
                tipo,
                quantidade,
                saldo,
                data_hora
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            produto_id,
            nome,
            "ENTRADA",
            movimentacao.quantidade,
            novo_saldo,
            data_hora
        ))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()

    return {
        "mensagem": "Entrada registrada com sucesso!",
        "produto_id": produto_id,
        "quantidade_entrada": movimentacao.quantidade,
        "novo_saldo": novo_saldo
    }

@app.post("/produtos/{produto_id}/saida")
def registrar_saida(produto_id: int, movimentacao: MovimentacaoNova):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    try:
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute("""
            SELECT nome, quantidade
            FROM produtos
            WHERE id = ? AND ativo = 1
        """, (produto_id,))

        produto = cursor.fetchone()

        if produto is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado ou desativado."
            )

        nome, saldo_atual = produto

        if movimentacao.quantidade > saldo_atual:
            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente."
            )

        novo_saldo = saldo_atual - movimentacao.quantidade

        cursor.execute("""
            UPDATE produtos
            SET quantidade = ?
            WHERE id = ?
        """, (novo_saldo, produto_id))

        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        cursor.execute("""
            INSERT INTO movimentacoes (
                produto_id,
                produto_nome,
                tipo,
                quantidade,
                saldo,
                data_hora
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            produto_id,
            nome,
            "SAÍDA",
            movimentacao.quantidade,
            novo_saldo,
            data_hora
        ))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()

    return {
        "mensagem": "Saída registrada com sucesso!",
        "produto_id": produto_id,
        "quantidade_saida": movimentacao.quantidade,
        "novo_saldo": novo_saldo
    }   