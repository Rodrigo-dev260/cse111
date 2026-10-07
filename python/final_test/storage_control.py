import datetime
import csv

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

ARQUIVO = "estoque.csv"

CATEGORIAS = [
"Estocável",
"Congelado"
]

estoque = []

# ==========================================

# CARREGAR ESTOQUE

# ==========================================

def carregar_estoque():
    global estoque


estoque = []

try:
    with open(ARQUIVO, "r", newline="", encoding="utf-8") as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:

            produto = {
                "nome": linha["nome"],
                "quantidade": int(linha["quantidade"]),
                "data_validade": linha["data_validade"],
                "categoria": linha["categoria"]
            }

            estoque.append(produto)

except FileNotFoundError:

    estoque = []


# ==========================================

# SALVAR ESTOQUE

# ==========================================

def salvar_estoque():


    with open(
        ARQUIVO,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        campos = [
            "nome",
            "quantidade",
            "data_validade",
            "categoria"
        ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=campos
    )

    escritor.writeheader()

    for produto in estoque:
        escritor.writerow(produto)


# ==========================================

# VALIDAR DATA

# ==========================================

def validar_data(data_str):

    try:

        return datetime.datetime.strptime(
            data_str,
            "%d/%m/%Y"
        ).date()

    except ValueError:

        return None

# ==========================================

# CLASSE PRINCIPAL

# ==========================================

class EstoqueApp(App):

# ======================================
# BUILD
# ======================================

    def build(self):

        carregar_estoque()

        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        self.menu_principal()

        return self.layout


# ======================================
# MENU PRINCIPAL
# ======================================

def menu_principal(self, instance=None):

    self.layout.clear_widgets()

    titulo = Label(
        text="CONTROLE DE ESTOQUE",
        font_size=24,
        size_hint_y=None,
        height=60
    )

    self.layout.add_widget(titulo)

    btn_cadastrar = Button(
        text="Cadastrar Produto",
        size_hint_y=None,
        height=50
    )

    btn_listar = Button(
        text="Listar Produtos",
        size_hint_y=None,
        height=50
    )

    btn_editar = Button(
        text="Editar Produto",
        size_hint_y=None,
        height=50
    )

    btn_excluir = Button(
        text="Excluir Produto",
        size_hint_y=None,
        height=50
    )

    btn_entrada = Button(
        text="Entrada de Estoque",
        size_hint_y=None,
        height=50
    )

    btn_saida = Button(
        text="Saída de Estoque",
        size_hint_y=None,
        height=50
    )

    btn_relatorio = Button(
        text="Relatório",
        size_hint_y=None,
        height=50
    )

    btn_alertas = Button(
        text="Alertas",
        size_hint_y=None,
        height=50
    )

    btn_cadastrar.bind(
        on_press=self.tela_cadastro
    )

    btn_listar.bind(
        on_press=self.tela_listagem
    )

    btn_editar.bind(
        on_press=self.tela_editar
    )

    btn_excluir.bind(
        on_press=self.tela_excluir
    )

    btn_entrada.bind(
        on_press=self.tela_entrada
    )

    btn_saida.bind(
        on_press=self.tela_saida
    )

    btn_relatorio.bind(
        on_press=self.tela_relatorio
    )

    btn_alertas.bind(
        on_press=self.tela_alertas
    )

    self.layout.add_widget(btn_cadastrar)
    self.layout.add_widget(btn_listar)
    self.layout.add_widget(btn_editar)
    self.layout.add_widget(btn_excluir)
    self.layout.add_widget(btn_entrada)
    self.layout.add_widget(btn_saida)
    self.layout.add_widget(btn_relatorio)
    self.layout.add_widget(btn_alertas)


# ======================================
# CADASTRO
# ======================================

def tela_cadastro(self, instance):

    self.layout.clear_widgets()

    titulo = Label(
        text="CADASTRAR PRODUTO",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    self.layout.add_widget(titulo)

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

    self.categoria_input = TextInput(
        hint_text="Categoria: Estocável ou Congelado",
        multiline=False,
        size_hint_y=None,
        height=50
    )

    btn_salvar = Button(
        text="Salvar Produto",
        size_hint_y=None,
        height=50
    )

    btn_voltar = Button(
        text="Voltar",
        size_hint_y=None,
        height=50
    )

    btn_salvar.bind(
        on_press=self.salvar_produto
    )

    btn_voltar.bind(
        on_press=self.voltar_menu
    )

    self.layout.add_widget(self.nome_input)
    self.layout.add_widget(self.quantidade_input)
    self.layout.add_widget(self.data_input)
    self.layout.add_widget(self.categoria_input)
    self.layout.add_widget(btn_salvar)
    self.layout.add_widget(btn_voltar)


def salvar_produto(self, instance):

    nome = self.nome_input.text.strip()
    quantidade = self.quantidade_input.text.strip()
    data = self.data_input.text.strip()
    categoria = self.categoria_input.text.strip()

    if not nome:

        self.mostrar_mensagem(
            "Digite o nome do produto."
        )

        return

    if not quantidade:

        self.mostrar_mensagem(
            "Digite a quantidade."
        )

        return

    quantidade = int(quantidade)

    if quantidade < 0:

        self.mostrar_mensagem(
            "A quantidade não pode ser negativa."
        )

        return

    data_validade = validar_data(data)

    if not data_validade:

        self.mostrar_mensagem(
            "Data inválida. Use DD/MM/AAAA."
        )

        return

    if categoria not in CATEGORIAS:

        self.mostrar_mensagem(
            "Categoria inválida."
        )

        return

    produto = {
        "nome": nome,
        "quantidade": quantidade,
        "data_validade": data,
        "categoria": categoria
    }

    estoque.append(produto)

    salvar_estoque()

    self.mostrar_mensagem(
        "Produto cadastrado com sucesso!"
    )


# ======================================
# LISTAGEM
# ======================================

def tela_listagem(self, instance):

    self.layout.clear_widgets()

    titulo = Label(
        text="LISTA DE PRODUTOS",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    self.layout.add_widget(titulo)

    scroll = ScrollView()

    lista = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        spacing=5
    )

    lista.bind(
        minimum_height=lista.setter("height")
    )

    if not estoque:

        lista.add_widget(
            Label(
                text="Nenhum produto cadastrado.",
                size_hint_y=None,
                height=50
            )
        )

    else:

        for produto in estoque:

            texto = (
                f"{produto['nome']} | "
                f"Quantidade: {produto['quantidade']} | "
                f"Validade: {produto['data_validade']} | "
                f"{produto['categoria']}"
            )

            lista.add_widget(
                Label(
                    text=texto,
                    size_hint_y=None,
                    height=60
                )
            )

    scroll.add_widget(lista)

    self.layout.add_widget(scroll)

    btn_voltar = Button(
        text="Voltar",
        size_hint_y=None,
        height=50
    )

    btn_voltar.bind(
        on_press=self.voltar_menu
    )

    self.layout.add_widget(btn_voltar)


# ======================================
# EDITAR
# ======================================

def tela_editar(self, instance=None):

    self.layout.clear_widgets()

    titulo = Label(
        text="EDITAR PRODUTO",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    self.layout.add_widget(titulo)

    scroll = ScrollView()

    lista = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        spacing=5
    )

    lista.bind(
        minimum_height=lista.setter("height")
    )

    if not estoque:

        lista.add_widget(
            Label(
                text="Nenhum produto cadastrado.",
                size_hint_y=None,
                height=50
            )
        )

    else:

        for indice, produto in enumerate(estoque):

            btn = Button(
                text=(
                    f"{produto['nome']} - "
                    f"Quantidade: {produto['quantidade']}"
                ),
                size_hint_y=None,
                height=60
            )

            btn.bind(
                on_press=lambda x, i=indice:
                self.tela_edicao(i)
            )

            lista.add_widget(btn)

    scroll.add_widget(lista)

    self.layout.add_widget(scroll)

    btn_voltar = Button(
        text="Voltar",
        size_hint_y=None,
        height=50
    )

    btn_voltar.bind(
        on_press=self.voltar_menu
    )

    self.layout.add_widget(btn_voltar)


def tela_edicao(self, indice):

    self.layout.clear_widgets()

    produto = estoque[indice]

    titulo = Label(
        text=f"EDITANDO: {produto['nome']}",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    self.layout.add_widget(titulo)

    self.editar_nome = TextInput(
        text=produto["nome"],
        multiline=False,
        size_hint_y=None,
        height=50
    )

    self.editar_quantidade = TextInput(
        text=str(produto["quantidade"]),
        multiline=False,
        input_filter="int",
        size_hint_y=None,
        height=50
    )

    self.editar_data = TextInput(
        text=produto["data_validade"],
        multiline=False,
        size_hint_y=None,
        height=50
    )

    self.editar_categoria = TextInput(
        text=produto["categoria"],
        multiline=False,
        size_hint_y=None,
        height=50
    )

    btn_salvar = Button(
        text="Salvar Alterações",
        size_hint_y=None,
        height=50
    )

    btn_voltar = Button(
        text="Cancelar",
        size_hint_y=None,
        height=50
    )

    btn_salvar.bind(
        on_press=lambda x:
        self.salvar_edicao(indice)
    )

    btn_voltar.bind(
        on_press=self.tela_editar
    )

    self.layout.add_widget(self.editar_nome)
    self.layout.add_widget(self.editar_quantidade)
    self.layout.add_widget(self.editar_data)
    self.layout.add_widget(self.editar_categoria)
    self.layout.add_widget(btn_salvar)
    self.layout.add_widget(btn_voltar)


def salvar_edicao(self, indice):

    nome = self.editar_nome.text.strip()
    quantidade = self.editar_quantidade.text.strip()
    data = self.editar_data.text.strip()
    categoria = self.editar_categoria.text.strip()

    if not nome:

        self.mostrar_mensagem(
            "Digite o nome do produto."
        )

        return

    if not quantidade:

        self.mostrar_mensagem(
            "Digite a quantidade."
        )

        return

    quantidade = int(quantidade)

    if quantidade < 0:

        self.mostrar_mensagem(
            "A quantidade não pode ser negativa."
        )

        return

    if not validar_data(data):

        self.mostrar_mensagem(
            "Data inválida. Use DD/MM/AAAA."
        )

        return

    if categoria not in CATEGORIAS:

        self.mostrar_mensagem(
            "Categoria inválida."
        )

        return

    estoque[indice] = {
        "nome": nome,
        "quantidade": quantidade,
        "data_validade": data,
        "categoria": categoria
    }

    salvar_estoque()

    self.mostrar_mensagem(
        "Produto atualizado com sucesso!"
    )


# ======================================
# EXCLUIR
# ======================================

def tela_excluir(self, instance=None):

    self.layout.clear_widgets()

    titulo = Label(
        text="EXCLUIR PRODUTO",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    self.layout.add_widget(titulo)

    scroll = ScrollView()

    lista = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        spacing=5
    )

    lista.bind(
        minimum_height=lista.setter("height")
    )

    if not estoque:

        lista.add_widget(
            Label(
                text="Nenhum produto cadastrado.",
                size_hint_y=None,
                height=50
            )
        )

    else:

        for indice, produto in enumerate(estoque):

            btn = Button(
                text=(
                    f"{produto['nome']} - "
                    f"Quantidade: {produto['quantidade']}"
                ),
                size_hint_y=None,
                height=60
            )

            btn.bind(
                on_press=lambda x, i=indice:
                self.confirmar_exclusao(i)
            )

            lista.add_widget(btn)

    scroll.add_widget(lista)

    self.layout.add_widget(scroll)

    btn_voltar = Button(
        text="Voltar",
        size_hint_y=None,
        height=50
    )

    btn_voltar.bind(
        on_press=self.voltar_menu
    )

    self.layout.add_widget(btn_voltar)


def confirmar_exclusao(self, indice):

    self.layout.clear_widgets()

    produto = estoque[indice]

    titulo = Label(
        text="CONFIRMAR EXCLUSÃO",
        font_size=22,
        size_hint_y=None,
        height=60
    )

    mensagem = Label(
        text=(
            f"Você deseja excluir:\n\n"
            f"{produto['nome']}\n\n"
            f"Quantidade: {produto['quantidade']}"
        )
    )

    btn_confirmar = Button(
        text="SIM, EXCLUIR",
        size_hint_y=None,
        height=50
    )

    btn_cancelar = Button(
        text="CANCELAR",
        size_hint_y=None,
        height=50
    )

    btn_confirmar.bind(
        on_press=lambda x:
        self.excluir_produto(indice)
    )

    btn_cancelar.bind(
        on_press=self.tela_excluir
    )

    self.layout.add_widget(titulo)
    self.layout.add_widget(mensagem)
    self.layout.add_widget(btn_confirmar)
    self.layout.add_widget(btn_cancelar)


def excluir_produto(self, indice):

    produto = estoque[indice]

    nome = produto["nome"]

    del estoque[indice]

    salvar_estoque()

    self.mostrar_mensagem(
        f"Produto '{nome}' excluído com sucesso!"
    )


# ======================================
# ENTRADA DE ESTOQUE
# ======================================

def tela_entrada(self, instance=None):

    self.layout.clear_widgets()

    titulo = Label(
        text="ENTRADA DE ESTOQUE",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    self.layout.add_widget(titulo)

    scroll = ScrollView()

    lista = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        spacing=5
    )

    lista.bind(
        minimum_height=lista.setter("height")
    )

    if not estoque:

        lista.add_widget(
            Label(
                text="Nenhum produto cadastrado.",
                size_hint_y=None,
                height=50
            )
        )

    else:

        for indice, produto in enumerate(estoque):

            btn = Button(
                text=(
                    f"{produto['nome']} | "
                    f"Estoque atual: {produto['quantidade']}"
                ),
                size_hint_y=None,
                height=60
            )

            btn.bind(
                on_press=lambda x, i=indice:
                self.formulario_entrada(i)
            )

            lista.add_widget(btn)

    scroll.add_widget(lista)

    self.layout.add_widget(scroll)

    btn_voltar = Button(
        text="Voltar",
        size_hint_y=None,
        height=50
    )

    btn_voltar.bind(
        on_press=self.voltar_menu
    )

    self.layout.add_widget(btn_voltar)


def formulario_entrada(self, indice):

    self.layout.clear_widgets()

    produto = estoque[indice]

    titulo = Label(
        text=f"ENTRADA: {produto['nome']}",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    estoque_atual = Label(
        text=f"Estoque atual: {produto['quantidade']}",
        font_size=18,
        size_hint_y=None,
        height=50
    )

    self.entrada_input = TextInput(
        hint_text="Quantidade que entrou",
        multiline=False,
        input_filter="int",
        size_hint_y=None,
        height=50
    )

    btn_confirmar = Button(
        text="Confirmar Entrada",
        size_hint_y=None,
        height=50
    )

    btn_voltar = Button(
        text="Cancelar",
        size_hint_y=None,
        height=50
    )

    btn_confirmar.bind(
        on_press=lambda x:
        self.registrar_entrada(indice)
    )

    btn_voltar.bind(
        on_press=self.tela_entrada
    )

    self.layout.add_widget(titulo)
    self.layout.add_widget(estoque_atual)
    self.layout.add_widget(self.entrada_input)
    self.layout.add_widget(btn_confirmar)
    self.layout.add_widget(btn_voltar)


def registrar_entrada(self, indice):

    quantidade = self.entrada_input.text.strip()

    if not quantidade:

        self.mostrar_mensagem(
            "Digite a quantidade da entrada."
        )

        return

    quantidade = int(quantidade)

    if quantidade <= 0:

        self.mostrar_mensagem(
            "A entrada deve ser maior que zero."
        )

        return

    estoque[indice]["quantidade"] += quantidade

    salvar_estoque()

    self.mostrar_mensagem(
        f"Entrada registrada!\n\n"
        f"Quantidade adicionada: {quantidade}\n"
        f"Novo estoque: {estoque[indice]['quantidade']}"
    )


# ======================================
# SAÍDA DE ESTOQUE
# ======================================

def tela_saida(self, instance=None):

    self.layout.clear_widgets()

    titulo = Label(
        text="SAÍDA DE ESTOQUE",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    self.layout.add_widget(titulo)

    scroll = ScrollView()

    lista = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        spacing=5
    )

    lista.bind(
        minimum_height=lista.setter("height")
    )

    if not estoque:

        lista.add_widget(
            Label(
                text="Nenhum produto cadastrado.",
                size_hint_y=None,
                height=50
            )
        )

    else:

        for indice, produto in enumerate(estoque):

            btn = Button(
                text=(
                    f"{produto['nome']} | "
                    f"Estoque atual: {produto['quantidade']}"
                ),
                size_hint_y=None,
                height=60
            )

            btn.bind(
                on_press=lambda x, i=indice:
                self.formulario_saida(i)
            )

            lista.add_widget(btn)

    scroll.add_widget(lista)

    self.layout.add_widget(scroll)

    btn_voltar = Button(
        text="Voltar",
        size_hint_y=None,
        height=50
    )

    btn_voltar.bind(
        on_press=self.voltar_menu
    )

    self.layout.add_widget(btn_voltar)


def formulario_saida(self, indice):

    self.layout.clear_widgets()

    produto = estoque[indice]

    titulo = Label(
        text=f"SAÍDA: {produto['nome']}",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    estoque_atual = Label(
        text=f"Estoque disponível: {produto['quantidade']}",
        font_size=18,
        size_hint_y=None,
        height=50
    )

    self.saida_input = TextInput(
        hint_text="Quantidade que saiu",
        multiline=False,
        input_filter="int",
        size_hint_y=None,
        height=50
    )

    btn_confirmar = Button(
        text="Confirmar Saída",
        size_hint_y=None,
        height=50
    )

    btn_voltar = Button(
        text="Cancelar",
        size_hint_y=None,
        height=50
    )

    btn_confirmar.bind(
        on_press=lambda x:
        self.registrar_saida(indice)
    )

    btn_voltar.bind(
        on_press=self.tela_saida
    )

    self.layout.add_widget(titulo)
    self.layout.add_widget(estoque_atual)
    self.layout.add_widget(self.saida_input)
    self.layout.add_widget(btn_confirmar)
    self.layout.add_widget(btn_voltar)


def registrar_saida(self, indice):

    quantidade = self.saida_input.text.strip()

    if not quantidade:

        self.mostrar_mensagem(
            "Digite a quantidade da saída."
        )

        return

    quantidade = int(quantidade)

    if quantidade <= 0:

        self.mostrar_mensagem(
            "A saída deve ser maior que zero."
        )

        return

    estoque_atual = estoque[indice]["quantidade"]

    if quantidade > estoque_atual:

        self.mostrar_mensagem(
            f"Estoque insuficiente!\n\n"
            f"Estoque disponível: {estoque_atual}\n"
            f"Você tentou retirar: {quantidade}"
        )

        return

    estoque[indice]["quantidade"] -= quantidade

    salvar_estoque()

    self.mostrar_mensagem(
        f"Saída registrada!\n\n"
        f"Quantidade retirada: {quantidade}\n"
        f"Novo estoque: {estoque[indice]['quantidade']}"
    )


# ======================================
# RELATÓRIO
# ======================================

def tela_relatorio(self, instance):

    self.layout.clear_widgets()

    titulo = Label(
        text="RELATÓRIO",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    self.layout.add_widget(titulo)

    scroll = ScrollView()

    conteudo = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        spacing=10
    )

    conteudo.bind(
        minimum_height=conteudo.setter("height")
    )

    total_produtos = len(estoque)

    quantidade_total = sum(
        produto["quantidade"]
        for produto in estoque
    )

    conteudo.add_widget(
        Label(
            text=f"Produtos cadastrados: {total_produtos}",
            size_hint_y=None,
            height=50
        )
    )

    conteudo.add_widget(
        Label(
            text=(
                f"Quantidade total em estoque: "
                f"{quantidade_total}"
            ),
            size_hint_y=None,
            height=50
        )
    )

    for produto in estoque:

        texto = (
            f"{produto['nome']} | "
            f"Quantidade: {produto['quantidade']}"
        )

        conteudo.add_widget(
            Label(
                text=texto,
                size_hint_y=None,
                height=50
            )
        )

    scroll.add_widget(conteudo)

    self.layout.add_widget(scroll)

    btn_voltar = Button(
        text="Voltar",
        size_hint_y=None,
        height=50
    )

    btn_voltar.bind(
        on_press=self.voltar_menu
    )

    self.layout.add_widget(btn_voltar)


# ======================================
# ALERTAS
# ======================================

def tela_alertas(self, instance):

    self.layout.clear_widgets()

    titulo = Label(
        text="ALERTAS",
        font_size=22,
        size_hint_y=None,
        height=50
    )

    self.layout.add_widget(titulo)

    scroll = ScrollView()

    lista = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        spacing=10
    )

    lista.bind(
        minimum_height=lista.setter("height")
    )

    hoje = datetime.date.today()

    encontrou_alerta = False

    for produto in estoque:

        data_validade = validar_data(
            produto["data_validade"]
        )

        if data_validade:

            dias = (
                data_validade - hoje
            ).days

            if dias <= 30:

                encontrou_alerta = True

                if dias < 0:

                    texto = (
                        f"{produto['nome']} - "
                        f"VENCIDO"
                    )

                else:

                    texto = (
                        f"{produto['nome']} - "
                        f"vence em {dias} dias"
                    )

                lista.add_widget(
                    Label(
                        text=texto,
                        size_hint_y=None,
                        height=50
                    )
                )

        if produto["quantidade"] <= 5:

            encontrou_alerta = True

            lista.add_widget(
                Label(
                    text=(
                        f"{produto['nome']} - "
                        f"ESTOQUE BAIXO "
                        f"({produto['quantidade']})"
                    ),
                    size_hint_y=None,
                    height=50
                )
            )

    if not encontrou_alerta:

        lista.add_widget(
            Label(
                text="Nenhum alerta no momento.",
                size_hint_y=None,
                height=50
            )
        )

    scroll.add_widget(lista)

    self.layout.add_widget(scroll)

    btn_voltar = Button(
        text="Voltar",
        size_hint_y=None,
        height=50
    )

    btn_voltar.bind(
        on_press=self.voltar_menu
    )

    self.layout.add_widget(btn_voltar)


# ======================================
# MENSAGEM
# ======================================

def mostrar_mensagem(self, mensagem):

    self.layout.clear_widgets()

    label = Label(
        text=mensagem,
        font_size=20
    )
