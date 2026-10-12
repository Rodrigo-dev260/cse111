import os
import sqlite3
import requests
import datetime


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Endereço da API
API_URL = os.getenv(
    "ESTOQUE_API_URL",
    "http://127.0.0.1:8001"
).rstrip("/")

PASTA_PROJETO = os.path.dirname(
    os.path.abspath(__file__)
)

CATEGORIAS = [
    "Estocável",
    "Congelado"
]

BANCO = os.path.join(
    PASTA_PROJETO,
    "estoque.db"
)


def criar_banco():

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_validade TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    """)

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        produto_nome TEXT NOT NULL,
        tipo TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        saldo INTEGER NOT NULL,
        data_hora TEXT NOT NULL
    )
    """)
    

    conexao.commit()

    conexao.close()

# ============================================================
# FUNÇÕES DO ARQUIVO CSV
# ============================================================

def inserir_produto_banco(
    nome,
    quantidade,
    data_validade,
    categoria
):

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

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
            nome,
            quantidade,
            data_validade,
            categoria
        )
    )

    conexao.commit()

    conexao.close()


# ============================================================
# VALIDAR DATA
# ============================================================

def validar_data(data_str):

    try:
        return datetime.datetime.strptime(
            data_str,
            "%d/%m/%Y"
        ).date()

    except ValueError:
        return None


# ============================================================
# APLICAÇÃO KIVY
# ============================================================

def listar_produtos_banco():

    url = "http://127.0.0.1:8000/produtos"

    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()

        dados = resposta.json()

        produtos = []

        for produto in dados:
            produtos.append((
                produto["id"],
                produto["nome"],
                produto["quantidade"],
                produto["data_validade"],
                produto["categoria"]
            ))

        return produtos

    except requests.RequestException as erro:
        print(f"Erro ao consultar API: {erro}")
        return []

def atualizar_produto_banco(
    id_produto,
    nome,
    quantidade,
    data_validade,
    categoria
):
    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

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
            nome,
            quantidade,
            data_validade,
            categoria,
            id_produto
        )
    )

    conexao.commit()
    conexao.close()

def produto_existe_banco(nome):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id
        FROM produtos
        WHERE LOWER(nome) = LOWER(?)
        """,
        (nome,)
    )

    produto = cursor.fetchone()

    conexao.close()

    return produto is not None


def excluir_produto_banco(id_produto):

    url = f"http://127.0.0.1:8000/produtos/{id_produto}"

    try:
        resposta = requests.delete(
            url,
            timeout=5
        )

    except requests.RequestException as erro:
        print(f"Erro ao conectar com a API: {erro}")
        return False

    if resposta.status_code == 404:
        print("Produto não encontrado ou já excluído.")
        return False

    if not resposta.ok:
        print(
            f"Erro ao excluir produto: {resposta.status_code}"
        )
        return False

    return True

def buscar_produto_banco(id_produto):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome,
            quantidade,
            data_validade,
            categoria
        FROM produtos
        WHERE id = ?
        """,
        (id_produto,)
    )

    produto = cursor.fetchone()

    conexao.close()

    return produto

def atualizar_quantidade_banco(id_produto, nova_quantidade):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE produtos
        SET quantidade = ?
        WHERE id = ?
        """,
        (
            nova_quantidade,
            id_produto
        )
    )

    conexao.commit()
    conexao.close()

def registrar_movimentacao_banco(
    produto_id,
    produto_nome,
    tipo,
    quantidade,
    saldo
):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    data_hora = datetime.datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO movimentacoes (
            produto_id,
            produto_nome,
            tipo,
            quantidade,
            saldo,
            data_hora
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            produto_id,
            produto_nome,
            tipo,
            quantidade,
            saldo,
            data_hora
        )
    )

    conexao.commit()
    conexao.close()

def listar_movimentacoes_banco():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute(
        """
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
        """
    )

    movimentacoes = cursor.fetchall()

    conexao.close()

    return movimentacoes

class EstoqueApp(App):


    # --------------------------------------------------------
    # INICIAR APLICATIVO
    # --------------------------------------------------------

    def build(self):

        criar_banco()

        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        self.menu_principal()

        return self.layout

    # --------------------------------------------------------
    # MENU PRINCIPAL
    # --------------------------------------------------------

    def menu_principal(self, instance=None):

        self.layout.clear_widgets()

        titulo = Label(
            text="CONTROLE DE ESTOQUE",
            font_size=24,
            size_hint_y=None,
            height=60
        )

        self.layout.add_widget(titulo)

        botoes = [
            ("Cadastrar Produto", self.tela_cadastro),
            ("Listar Produtos", self.tela_listagem),
            ("Editar Produto", self.tela_editar),
            ("Excluir Produto", self.tela_excluir),
            ("Entrada de Estoque", self.tela_entrada),
            ("Saída de Estoque", self.tela_saida),
            ("Histórico de Movimentações", self.tela_historico),
            ("Relatório", self.tela_relatorio),
            ("Alertas", self.tela_alertas)
        ]

        for texto, funcao in botoes:

            botao = Button(
                text=texto,
                size_hint_y=None,
                height=50
            )

            botao.bind(
                on_press=funcao
            )

            self.layout.add_widget(botao)

    # --------------------------------------------------------
    # CADASTRAR PRODUTO
    # --------------------------------------------------------

    def tela_cadastro(self, instance=None):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="CADASTRAR PRODUTO",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        self.nome_input = TextInput(
            hint_text="Nome do produto",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.quantidade_input = TextInput(
            hint_text="Quantidade inicial",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=50
        )

        self.data_input = TextInput(
            hint_text="Data de validade DD/MM/AAAA",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.categoria_input = Spinner(
            text="Selecione a categoria",
            values=CATEGORIAS,
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(self.nome_input)
        self.layout.add_widget(self.quantidade_input)
        self.layout.add_widget(self.data_input)
        self.layout.add_widget(self.categoria_input)

        btn_salvar = Button(
            text="Cadastrar Produto",
            size_hint_y=None,
            height=50
        )

        btn_salvar.bind(
            on_press=self.salvar_produto
        )

        self.layout.add_widget(btn_salvar)

        self.adicionar_botao_voltar()

    # --------------------------------------------------------
    # SALVAR PRODUTO
    # --------------------------------------------------------

    
    def salvar_produto(self, instance=None):

        nome = self.nome_input.text.strip()
        quantidade_texto = self.quantidade_input.text.strip()
        data_validade = self.data_input.text.strip()
        categoria = self.categoria_input.text.strip()

        if nome == "":
            self.mostrar_mensagem(
                "Digite o nome do produto."
            )
            return

        if quantidade_texto == "":
            self.mostrar_mensagem(
                "Digite a quantidade."
            )
            return

        try:
            quantidade = int(quantidade_texto)

        except ValueError:
            self.mostrar_mensagem(
                "Quantidade inválida."
            )
            return

        if quantidade < 0:
            self.mostrar_mensagem(
                "A quantidade não pode ser negativa."
            )
            return

        if validar_data(data_validade) is None:
            self.mostrar_mensagem(
                "Data inválida.\nUse DD/MM/AAAA."
            )
            return

        if categoria not in CATEGORIAS:
            self.mostrar_mensagem(
                "Categoria inválida."
            )
            return

        dados = {
            "nome": nome,
            "quantidade": quantidade,
            "data_validade": data_validade,
            "categoria": categoria
        }

        try:
            resposta = requests.post(
                "http://127.0.0.1:8000/teste-supabase/produtos",
                json=dados,
                timeout=10
            )

        except requests.RequestException as erro:
            self.mostrar_mensagem(
                f"Erro ao conectar com a API:\n{erro}"
            )
            return

        if resposta.status_code == 409:
            self.mostrar_mensagem(
                f"O produto '{nome}' já está cadastrado."
            )
            return

        if resposta.status_code != 201:
            self.mostrar_mensagem(
                f"Erro ao cadastrar produto.\n"
                f"Código: {resposta.status_code}"
            )
            return

        self.mostrar_mensagem(
            f"Produto cadastrado no Supabase!\n\n"
            f"Produto: {nome}\n"
            f"Quantidade: {quantidade}\n"
            f"Validade: {data_validade}\n"
            f"Categoria: {categoria}"
        )


    # --------------------------------------------------------
    # LISTAR PRODUTOS
    # --------------------------------------------------------

    
    def tela_listagem(self, instance=None):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="LISTA DE PRODUTOS - SUPABASE",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        scroll = ScrollView()

        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )

        # Consulta os produtos na nuvem pelo FastAPI
        try:
            resposta = requests.get(
                f"{API_URL}/teste-supabase/produtos",
                timeout=10
            )

            resposta.raise_for_status()
            produtos = resposta.json()

        except (requests.RequestException, ValueError) as erro:
            self.mostrar_mensagem(
                f"Erro ao consultar produtos no Supabase:\n{erro}"
            )
            produtos = []

        if len(produtos) == 0:

            lista.add_widget(
                Label(
                    text="Nenhum produto encontrado.",
                    size_hint_y=None,
                    height=60
                )
            )

        else:

            for produto in produtos:

                id_produto = produto["id"]
                nome = produto["nome"]
                quantidade = produto["quantidade"]
                data_validade = produto["data_validade"]
                categoria = produto["categoria"]

                texto = (
                    f"ID: {id_produto}\n"
                    f"Produto: {nome}\n"
                    f"Quantidade: {quantidade}\n"
                    f"Validade: {data_validade}\n"
                    f"Categoria: {categoria}"
                )

                lista.add_widget(
                    Label(
                        text=texto,
                        size_hint_y=None,
                        height=120
                    )
                )

        scroll.add_widget(lista)

        self.layout.add_widget(scroll)

        self.adicionar_botao_voltar()


    # --------------------------------------------------------
    # ESCOLHER PRODUTO PARA EDITAR
    # --------------------------------------------------------

    def tela_editar(self, instance=None):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="EDITAR PRODUTO - SUPABASE",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        scroll = ScrollView()

        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )

        try:
            resposta = requests.get(
                "http://127.0.0.1:8000/teste-supabase/produtos",
                timeout=10
            )

            resposta.raise_for_status()
            produtos = resposta.json()

        except (requests.RequestException, ValueError) as erro:
            self.mostrar_mensagem(
                f"Erro ao consultar o Supabase:\n{erro}"
            )
            return

        if len(produtos) == 0:

            lista.add_widget(
                Label(
                    text="Nenhum produto cadastrado.",
                    size_hint_y=None,
                    height=50
                )
            )

        else:

            for produto in produtos:

                id_produto = produto["id"]
                nome = produto["nome"]
                quantidade = produto["quantidade"]

                botao = Button(
                    text=(
                        f"ID: {id_produto} - "
                        f"{nome} - "
                        f"Quantidade: {quantidade}"
                    ),
                    size_hint_y=None,
                    height=50
                )

                # Mantém o formato esperado
                # pela função tela_edicao()
                produto_edicao = (
                    produto["id"],
                    produto["nome"],
                    produto["quantidade"],
                    produto["data_validade"],
                    produto["categoria"]
                )

                botao.bind(
                    on_press=lambda instance, p=produto_edicao:
                    self.tela_edicao(p)
                )

                lista.add_widget(botao)

        scroll.add_widget(lista)

        self.layout.add_widget(scroll)

        self.adicionar_botao_voltar()
 
    # --------------------------------------------------------
    # FORMULÁRIO DE EDIÇÃO
    # --------------------------------------------------------

    def tela_edicao(self, produto):

        self.layout.clear_widgets()

        id_produto = produto[0]
        nome = produto[1]
        quantidade = produto[2]
        data_validade = produto[3]
        categoria = produto[4]

        # Guarda o ID do produto que está sendo editado
        self.edicao_id = id_produto

        self.layout.add_widget(
            Label(
                text=f"EDITAR PRODUTO - ID {id_produto}",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        self.nome_edicao = TextInput(
            text=nome,
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.quantidade_edicao = TextInput(
            text=str(quantidade),
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=50
        )

        self.data_edicao = TextInput(
            text=data_validade,
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.categoria_edicao = TextInput(
            text=categoria,
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(self.nome_edicao)
        self.layout.add_widget(self.quantidade_edicao)
        self.layout.add_widget(self.data_edicao)
        self.layout.add_widget(self.categoria_edicao)

        btn_salvar = Button(
            text="Salvar Alterações",
            size_hint_y=None,
            height=50
        )

        btn_salvar.bind(
            on_press=self.salvar_edicao
        )

        self.layout.add_widget(btn_salvar)

        btn_voltar = Button(
            text="Voltar",
            size_hint_y=None,
            height=50
        )

        btn_voltar.bind(
            on_press=self.tela_editar
        )

        self.layout.add_widget(btn_voltar)

    # --------------------------------------------------------
    # SALVAR EDIÇÃO
    # --------------------------------------------------------

    def salvar_edicao(self, instance=None):

        id_produto = self.edicao_id

        nome = self.nome_edicao.text.strip()
        quantidade_texto = self.quantidade_edicao.text.strip()
        data_validade = self.data_edicao.text.strip()
        categoria = self.categoria_edicao.text.strip()

        if nome == "":
            self.mostrar_mensagem(
                "Digite o nome do produto."
            )
            return

        try:
            quantidade = int(quantidade_texto)

        except ValueError:
            self.mostrar_mensagem(
                "Quantidade inválida."
            )
            return

        if quantidade < 0:
            self.mostrar_mensagem(
                "A quantidade não pode ser negativa."
            )
            return

        if validar_data(data_validade) is None:
            self.mostrar_mensagem(
                "Data inválida.\nUse DD/MM/AAAA."
            )
            return

        if categoria not in CATEGORIAS:
            self.mostrar_mensagem(
                "Categoria inválida.\n"
                "Use Estocável ou Congelado."
            )
            return

        # Consulta o saldo atual no Supabase
        # para não alterar o estoque sem movimentação.
        url = (
            f"http://127.0.0.1:8000"
            f"/teste-supabase/produtos/{id_produto}"
        )

        try:
            consulta = requests.get(
                url,
                timeout=10
            )

            consulta.raise_for_status()
            produto_atual = consulta.json()

        except (requests.RequestException, ValueError):
            self.mostrar_mensagem(
                "Não foi possível consultar o produto.\n"
                "Nenhuma alteração foi enviada."
            )
            return

        # Impede alterar a quantidade pela tela de edição
        if quantidade != produto_atual["quantidade"]:
            self.mostrar_mensagem(
                "Para alterar a quantidade, utilize\n"
                "Entrada ou Saída de Estoque."
            )
            return

        dados = {
            "nome": nome,
            "quantidade": quantidade,
            "data_validade": data_validade,
            "categoria": categoria
        }

        try:
            resposta = requests.put(
                url,
                json=dados,
                timeout=10
            )

        except requests.RequestException as erro:
            self.mostrar_mensagem(
                f"Erro de comunicação com a API:\n{erro}\n\n"
                "Confira os dados antes de tentar novamente."
            )
            return

        if resposta.status_code == 404:
            self.mostrar_mensagem(
                "Produto não encontrado no Supabase."
            )
            return

        if resposta.status_code == 409:
            self.mostrar_mensagem(
                f"Já existe outro produto com o nome '{nome}'."
            )
            return

        if not resposta.ok:
            self.mostrar_mensagem(
                f"Erro ao editar produto.\n"
                f"Código: {resposta.status_code}"
            )
            return

        self.mostrar_mensagem(
            "Produto alterado no Supabase com sucesso!\n\n"
            f"Produto: {nome}\n"
            f"Quantidade: {quantidade}\n"
            f"Validade: {data_validade}\n"
            f"Categoria: {categoria}"
        )


    # --------------------------------------------------------
    # EXCLUIR PRODUTO
    # --------------------------------------------------------

    def tela_excluir(self, instance=None):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="EXCLUIR PRODUTO - SUPABASE",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        scroll = ScrollView()

        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )

        try:
            resposta = requests.get(
                "http://127.0.0.1:8000/teste-supabase/produtos",
                timeout=10
            )

            resposta.raise_for_status()
            produtos = resposta.json()

        except (requests.RequestException, ValueError) as erro:
            self.mostrar_mensagem(
                f"Erro ao consultar o Supabase:\n{erro}"
            )
            return

        if len(produtos) == 0:

            lista.add_widget(
                Label(
                    text="Nenhum produto cadastrado.",
                    size_hint_y=None,
                    height=50
                )
            )

        else:

            for produto in produtos:

                id_produto = produto["id"]
                nome = produto["nome"]
                quantidade = produto["quantidade"]

                botao = Button(
                    text=(
                        f"ID: {id_produto} - "
                        f"{nome} - "
                        f"Quantidade: {quantidade}"
                    ),
                    size_hint_y=None,
                    height=50
                )

                # Formato esperado pela função
                # confirmar_exclusao()
                produto_exclusao = (
                    produto["id"],
                    produto["nome"],
                    produto["quantidade"],
                    produto["data_validade"],
                    produto["categoria"]
                )

                botao.bind(
                    on_press=lambda instance, p=produto_exclusao:
                    self.confirmar_exclusao(p)
                )

                lista.add_widget(botao)

        scroll.add_widget(lista)

        self.layout.add_widget(scroll)

        self.adicionar_botao_voltar()


    # --------------------------------------------------------
    # CONFIRMAR EXCLUSÃO
    # --------------------------------------------------------

    def confirmar_exclusao(self, produto):

        id_produto = produto[0]
        nome = produto[1]
        quantidade = produto[2]

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="CONFIRMAR EXCLUSÃO",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        self.layout.add_widget(
            Label(
                text=(
                    f"Deseja realmente excluir?\n\n"
                    f"ID: {id_produto}\n"
                    f"Produto: {nome}\n"
                    f"Quantidade: {quantidade}"
                ),
                font_size=20
            )
        )

        btn_excluir = Button(
            text="SIM, EXCLUIR",
            size_hint_y=None,
            height=50
        )

        btn_excluir.bind(
            on_press=lambda instance:
            self.excluir_produto(id_produto, nome)
        )

        btn_cancelar = Button(
            text="CANCELAR",
            size_hint_y=None,
            height=50
        )

        btn_cancelar.bind(
            on_press=self.tela_excluir
        )

        self.layout.add_widget(btn_excluir)
        self.layout.add_widget(btn_cancelar)

    # --------------------------------------------------------
    # REALIZAR EXCLUSÃO
    # --------------------------------------------------------

    def excluir_produto(self, id_produto, nome):

        url = (
            f"http://127.0.0.1:8000"
            f"/teste-supabase/produtos/{id_produto}"
        )

        try:
            resposta = requests.delete(
                url,
                timeout=10
            )

        except requests.RequestException as erro:
            self.mostrar_mensagem(
                f"Erro de comunicação com a API:\n{erro}\n\n"
                "Confira a lista de produtos antes "
                "de tentar novamente."
            )
            return

        if resposta.status_code == 404:
            self.mostrar_mensagem(
                "Produto não encontrado ou já desativado."
            )
            return

        if not resposta.ok:
            self.mostrar_mensagem(
                f"Erro ao desativar produto.\n"
                f"Código: {resposta.status_code}"
            )
            return

        self.mostrar_mensagem(
            f"Produto desativado no Supabase!\n\n"
            f"Produto: {nome}\n"
            f"ID: {id_produto}"
        )


    # --------------------------------------------------------
    # ENTRADA DE ESTOQUE
    # --------------------------------------------------------

    
    def tela_entrada(self, instance=None):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="ENTRADA DE ESTOQUE - SUPABASE",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        scroll = ScrollView()

        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )

        # Consulta os produtos ativos no Supabase
        try:
            resposta = requests.get(
                "http://127.0.0.1:8000/teste-supabase/produtos",
                timeout=10
            )

            resposta.raise_for_status()
            produtos = resposta.json()

        except (requests.RequestException, ValueError) as erro:
            self.mostrar_mensagem(
                f"Erro ao consultar o Supabase:\n{erro}"
            )
            return

        if len(produtos) == 0:

            lista.add_widget(
                Label(
                    text="Nenhum produto cadastrado.",
                    size_hint_y=None,
                    height=50
                )
            )

        else:

            for produto in produtos:

                id_produto = produto["id"]
                nome = produto["nome"]
                quantidade = produto["quantidade"]

                botao = Button(
                    text=(
                        f"ID: {id_produto} - "
                        f"{nome} - "
                        f"Estoque atual: {quantidade}"
                    ),
                    size_hint_y=None,
                    height=50
                )

                # Mantém o formato esperado pelo
                # formulário antigo do Kivy
                produto_formulario = (
                    produto["id"],
                    produto["nome"],
                    produto["quantidade"],
                    produto["data_validade"],
                    produto["categoria"]
                )

                botao.bind(
                    on_press=lambda instance, p=produto_formulario:
                    self.formulario_entrada(p)
                )

                lista.add_widget(botao)

        scroll.add_widget(lista)

        self.layout.add_widget(scroll)

        self.adicionar_botao_voltar()


    # --------------------------------------------------------
    # FORMULÁRIO DE ENTRADA
    # --------------------------------------------------------

    def formulario_entrada(self, produto):

        id_produto = produto[0]
        nome = produto[1]
        quantidade = produto[2]

        # Guarda o ID para usar quando registrar a entrada
        self.entrada_id = id_produto

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="REGISTRAR ENTRADA",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        self.layout.add_widget(
            Label(
                text=(
                    f"ID: {id_produto}\n"
                    f"Produto: {nome}\n"
                    f"Estoque atual: {quantidade}"
                ),
                size_hint_y=None,
                height=100
            )
        )

        self.entrada_quantidade = TextInput(
            hint_text="Quantidade que entrou",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(
            self.entrada_quantidade
        )

        btn_registrar = Button(
            text="Registrar Entrada",
            size_hint_y=None,
            height=50
        )

        btn_registrar.bind(
            on_press=self.registrar_entrada
        )

        self.layout.add_widget(btn_registrar)

        btn_voltar = Button(
            text="Voltar",
            size_hint_y=None,
            height=50
        )

        btn_voltar.bind(
            on_press=self.tela_entrada
        )

        self.layout.add_widget(btn_voltar)

    # --------------------------------------------------------
    # REGISTRAR ENTRADA
    # --------------------------------------------------------

    def registrar_entrada(self, instance=None):

        texto = self.entrada_quantidade.text.strip()

        if texto == "":
            self.mostrar_mensagem(
                "Digite a quantidade da entrada."
            )
            return

        try:
            quantidade_entrada = int(texto)

        except ValueError:
            self.mostrar_mensagem(
                "Quantidade inválida."
            )
            return

        if quantidade_entrada <= 0:
            self.mostrar_mensagem(
                "A quantidade deve ser maior que zero."
            )
            return

        id_produto = self.entrada_id

        url = f"http://127.0.0.1:8000/teste-supabase/produtos/{id_produto}/entrada"

        try:
            resposta = requests.post(
                url,
                json={"quantidade": quantidade_entrada},
                timeout=5
            )

            if resposta.status_code == 404:
                self.mostrar_mensagem(
                    "Produto não encontrado na API."
                )
                return

            resposta.raise_for_status()

            # Consultar o estoque atualizado na API
            resposta_produto = requests.get(
                f"http://127.0.0.1:8000/teste-supabase/produtos/{id_produto}",
                timeout=5
            )

            resposta_produto.raise_for_status()

            produto = resposta_produto.json()

        except requests.RequestException as erro:
            self.mostrar_mensagem(
                f"Erro na comunicação com a API:\n{erro}"
            )
            return

        self.mostrar_mensagem(
            f"Entrada registrada!\n\n"
            f"Produto: {produto['nome']}\n"
            f"Entrada: {quantidade_entrada}\n"
            f"Novo estoque: {produto['quantidade']}"
        )

    # --------------------------------------------------------
    # SAÍDA DE ESTOQUE
    # --------------------------------------------------------

    
    def tela_saida(self, instance=None):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="SAÍDA DE ESTOQUE - SUPABASE",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        scroll = ScrollView()

        lista = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )

        # Consultar produtos no Supabase
        try:
            resposta = requests.get(
                "http://127.0.0.1:8000/teste-supabase/produtos",
                timeout=10
            )

            resposta.raise_for_status()
            produtos = resposta.json()

        except (requests.RequestException, ValueError) as erro:
            self.mostrar_mensagem(
                f"Erro ao consultar o Supabase:\n{erro}"
            )
            return

        if len(produtos) == 0:

            lista.add_widget(
                Label(
                    text="Nenhum produto cadastrado.",
                    size_hint_y=None,
                    height=50
                )
            )

        else:

            for produto in produtos:

                id_produto = produto["id"]
                nome = produto["nome"]
                quantidade = produto["quantidade"]

                botao = Button(
                    text=(
                        f"ID: {id_produto} - "
                        f"{nome} - "
                        f"Estoque atual: {quantidade}"
                    ),
                    size_hint_y=None,
                    height=50
                )

                # Converter os dados para o formato
                # esperado pelo formulário de saída
                produto_formulario = (
                    produto["id"],
                    produto["nome"],
                    produto["quantidade"],
                    produto["data_validade"],
                    produto["categoria"]
                )

                botao.bind(
                    on_press=lambda instance, p=produto_formulario:
                    self.formulario_saida(p)
                )

                lista.add_widget(botao)

        scroll.add_widget(lista)

        self.layout.add_widget(scroll)

        self.adicionar_botao_voltar()


    # --------------------------------------------------------
    # FORMULÁRIO DE SAÍDA
    # --------------------------------------------------------

    def formulario_saida(self, produto):
        id_produto = produto[0]
        nome = produto[1]
        quantidade = produto[2]

        # Guarda o ID para usar ao registrar a saída
        self.saida_id = id_produto

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="REGISTRAR SAÍDA",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        self.layout.add_widget(
            Label(
                text=(
                    f"ID: {id_produto}\n"
                    f"Produto: {nome}\n"
                    f"Estoque atual: {quantidade}"
                ),
                size_hint_y=None,
                height=100
            )
        )

        self.saida_quantidade = TextInput(
            hint_text="Quantidade que saiu",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(
            self.saida_quantidade
        )

        btn_registrar = Button(
            text="Registrar Saída",
            size_hint_y=None,
            height=50
        )

        btn_registrar.bind(
            on_press=self.registrar_saida
        )

        self.layout.add_widget(btn_registrar)

        btn_voltar = Button(
            text="Voltar",
            size_hint_y=None,
            height=50
        )

        btn_voltar.bind(
            on_press=self.tela_saida
        )

        self.layout.add_widget(btn_voltar)

    # --------------------------------------------------------
    # REGISTRAR SAÍDA
    # --------------------------------------------------------

    def registrar_saida(self, instance=None):

        texto = self.saida_quantidade.text.strip()

        if texto == "":
            self.mostrar_mensagem(
                "Digite a quantidade da saída."
            )
            return

        try:
            quantidade_saida = int(texto)

        except ValueError:
            self.mostrar_mensagem(
                "Quantidade inválida."
            )
            return

        if quantidade_saida <= 0:
            self.mostrar_mensagem(
                "A quantidade deve ser maior que zero."
            )
            return

        id_produto = self.saida_id

        url = (
            f"http://127.0.0.1:8000"
            f"/teste-supabase/produtos/{id_produto}/saida"
        )

        try:
            resposta = requests.post(
                url,
                json={"quantidade": quantidade_saida},
                timeout=10
            )

        except requests.RequestException as erro:
            self.mostrar_mensagem(
                f"Erro de comunicação com a API:\n{erro}\n\n"
                "Confira o estoque antes de tentar novamente."
            )
            return

        if resposta.status_code == 404:
            self.mostrar_mensagem(
                "Produto não encontrado no Supabase."
            )
            return

        if resposta.status_code == 400:
            self.mostrar_mensagem(
                "Estoque insuficiente para essa saída."
            )
            return

        if not resposta.ok:
            self.mostrar_mensagem(
                f"Erro ao registrar saída.\n"
                f"Código: {resposta.status_code}"
            )
            return

        # A saída foi aceita pela API.
        # Agora consulta o estoque atualizado.
        try:
            resposta_produto = requests.get(
                f"http://127.0.0.1:8000"
                f"/teste-supabase/produtos/{id_produto}",
                timeout=10
            )

            resposta_produto.raise_for_status()
            produto = resposta_produto.json()

        except (requests.RequestException, ValueError):
            self.mostrar_mensagem(
                "Saída aceita pela API!\n\n"
                "Não foi possível consultar o novo estoque.\n"
                "Atualize a lista de produtos para conferir."
            )
            return

        self.mostrar_mensagem(
            f"Saída registrada no Supabase!\n\n"
            f"Produto: {produto['nome']}\n"
            f"Saída: {quantidade_saida}\n"
            f"Novo estoque: {produto['quantidade']}"
        )


        # --------------------------------------------------------
    # HISTÓRICO DE MOVIMENTAÇÕES
    # --------------------------------------------------------

    def tela_historico(self, instance=None):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="HISTÓRICO DE MOVIMENTAÇÕES - SQLITE",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        movimentacoes = listar_movimentacoes_banco()

        if len(movimentacoes) == 0:

            self.layout.add_widget(
                Label(
                    text="Nenhuma movimentação registrada.",
                    size_hint_y=None,
                    height=50
                )
            )

        else:

            scroll = ScrollView()

            lista = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                spacing=10
            )

            lista.bind(
                minimum_height=lista.setter("height")
            )

            for movimentacao in movimentacoes:

                id_movimentacao = movimentacao[0]
                produto_id = movimentacao[1]
                produto_nome = movimentacao[2]
                tipo = movimentacao[3]
                quantidade = movimentacao[4]
                saldo = movimentacao[5]
                data_hora = movimentacao[6]

                if tipo == "ENTRADA":
                    sinal = "+"
                else:
                    sinal = "-"

                texto = (
                    f"{data_hora}\n"
                    f"ID Mov.: {id_movimentacao} | "
                    f"Produto ID: {produto_id}\n"
                    f"{produto_nome}\n"
                    f"{tipo}: {sinal}{quantidade} | "
                    f"Saldo: {saldo}"
                )

                lista.add_widget(
                    Label(
                        text=texto,
                        size_hint_y=None,
                        height=100
                    )
                )

            scroll.add_widget(lista)

            self.layout.add_widget(scroll)

        self.adicionar_botao_voltar()

    # --------------------------------------------------------
    # RELATÓRIO
    # --------------------------------------------------------

    def tela_relatorio(self, instance=None):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="RELATÓRIO DE ESTOQUE - SUPABASE",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        # Consulta os produtos ativos no Supabase
        try:
            resposta = requests.get(
                "http://127.0.0.1:8000/teste-supabase/produtos",
                timeout=10
            )

            resposta.raise_for_status()
            produtos = resposta.json()

        except (requests.RequestException, ValueError) as erro:
            self.mostrar_mensagem(
                f"Erro ao consultar o Supabase:\n{erro}"
            )
            return

        if len(produtos) == 0:

            self.layout.add_widget(
                Label(
                    text="Nenhum produto cadastrado.",
                    size_hint_y=None,
                    height=50
                )
            )

        else:

            total_produtos = len(produtos)

            total_quantidade = sum(
                produto["quantidade"]
                for produto in produtos
            )

            self.layout.add_widget(
                Label(
                    text=(
                        f"Produtos cadastrados: "
                        f"{total_produtos}\n"
                        f"Quantidade total: "
                        f"{total_quantidade}"
                    ),
                    size_hint_y=None,
                    height=80
                )
            )

            # Área com rolagem
            scroll = ScrollView()

            lista = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                spacing=10
            )

            lista.bind(
                minimum_height=lista.setter("height")
            )

            for produto in produtos:

                id_produto = produto["id"]
                nome = produto["nome"]
                quantidade = produto["quantidade"]

                lista.add_widget(
                    Label(
                        text=(
                            f"ID: {id_produto} - "
                            f"{nome} - "
                            f"{quantidade} unidades"
                        ),
                        size_hint_y=None,
                        height=50
                    )
                )

            scroll.add_widget(lista)
            self.layout.add_widget(scroll)

        self.adicionar_botao_voltar()


    # --------------------------------------------------------
    # ALERTAS
    # --------------------------------------------------------

    def tela_alertas(self, instance=None):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text="ALERTAS DE ESTOQUE - SUPABASE",
                font_size=22,
                size_hint_y=None,
                height=50
            )
        )

        # Consulta os produtos ativos no Supabase
        try:
            resposta = requests.get(
                "http://127.0.0.1:8000/teste-supabase/produtos",
                timeout=10
            )

            resposta.raise_for_status()
            produtos = resposta.json()

        except (requests.RequestException, ValueError) as erro:
            self.mostrar_mensagem(
                f"Erro ao consultar o Supabase:\n{erro}"
            )
            return

        hoje = datetime.datetime.now().date()

        alertas = []

        for produto in produtos:

            id_produto = produto["id"]
            nome = produto["nome"]
            quantidade = produto["quantidade"]
            data_validade = produto["data_validade"]

            # ALERTA DE ESTOQUE BAIXO
            if quantidade <= 5:

                alertas.append(
                    f"ESTOQUE BAIXO\n"
                    f"ID: {id_produto} - {nome}\n"
                    f"Quantidade: {quantidade}"
                )

            # ALERTA DE VALIDADE
            try:
                validade = datetime.datetime.strptime(
                    data_validade,
                    "%d/%m/%Y"
                ).date()

                dias_restantes = (
                    validade - hoje
                ).days

                if dias_restantes < 0:

                    alertas.append(
                        f"PRODUTO VENCIDO\n"
                        f"ID: {id_produto} - {nome}\n"
                        f"Validade: {data_validade}"
                    )

                elif dias_restantes <= 30:

                    alertas.append(
                        f"VALIDADE PRÓXIMA\n"
                        f"ID: {id_produto} - {nome}\n"
                        f"Validade: {data_validade}\n"
                        f"Faltam {dias_restantes} dias"
                    )

            except (ValueError, TypeError):

                alertas.append(
                    f"DATA INVÁLIDA\n"
                    f"ID: {id_produto} - {nome}\n"
                    f"Validade: {data_validade}"
                )

        # MOSTRAR ALERTAS
        if len(alertas) == 0:

            self.layout.add_widget(
                Label(
                    text="Nenhum alerta no momento.",
                    size_hint_y=None,
                    height=60
                )
            )

        else:

            scroll = ScrollView()

            lista = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                spacing=10
            )

            lista.bind(
                minimum_height=lista.setter("height")
            )

            for alerta in alertas:

                lista.add_widget(
                    Label(
                        text=alerta,
                        size_hint_y=None,
                        height=110
                    )
                )

            scroll.add_widget(lista)
            self.layout.add_widget(scroll)

        self.adicionar_botao_voltar()


    # --------------------------------------------------------
    # MOSTRAR MENSAGEM
    # --------------------------------------------------------

    def mostrar_mensagem(self, mensagem):

        self.layout.clear_widgets()

        self.layout.add_widget(
            Label(
                text=mensagem,
                font_size=20
            )
        )

        btn_voltar = Button(
            text="Voltar ao Menu",
            size_hint_y=None,
            height=50
        )

        btn_voltar.bind(
            on_press=self.voltar_menu
        )

        self.layout.add_widget(btn_voltar)

    # --------------------------------------------------------
    # BOTÃO VOLTAR
    # --------------------------------------------------------

    def adicionar_botao_voltar(self):

        btn_voltar = Button(
            text="Voltar ao Menu",
            size_hint_y=None,
            height=50
        )

        btn_voltar.bind(
            on_press=self.voltar_menu
        )

        self.layout.add_widget(btn_voltar)

    # --------------------------------------------------------
    # VOLTAR AO MENU
    # --------------------------------------------------------

    def voltar_menu(self, instance=None):

        self.menu_principal()


# ============================================================
# EXECUTAR PROGRAMA
# ============================================================

if __name__ == "__main__":

    print("PROGRAMA INICIANDO...")

    EstoqueApp().run()

    print("PROGRAMA ENCERRADO...")