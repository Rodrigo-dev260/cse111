import datetime
import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

ARQUIVO = "estoque.csv"
estoque = []
CATEGORIAS = ["Estocável", "Congelado"]

def carregar_estoque():
    global estoque
    estoque = []
    try:
        with open(ARQUIVO, newline="", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['quantidade'] = int(row['quantidade'])
                estoque.append(row)
    except FileNotFoundError:
        estoque = []

def salvar_estoque():
    with open(ARQUIVO, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['nome', 'categoria', 'quantidade', 'validade']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for produto in estoque:
            writer.writerow(produto)

def validar_data(data_str):
    try:
        datetime.datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

class EstoqueApp(App):
    def build(self):
        carregar_estoque()
        self.layout = BoxLayout(orientation='vertical')

        # Botões principais
        btn_cadastrar = Button(text="Cadastrar Produto")
        btn_listar = Button(text="Listar Estoque")
        btn_relatorio = Button(text="Relatório por Categoria")
        btn_alerta = Button(text="Verificar Alertas")

        btn_cadastrar.bind(on_press=self.tela_cadastro)
        btn_listar.bind(on_press=self.tela_listagem)
        btn_relatorio.bind(on_press=self.tela_relatorio)
        btn_alerta.bind(on_press=self.tela_alertas)

        self.layout.add_widget(btn_cadastrar)
        self.layout.add_widget(btn_listar)
        self.layout.add_widget(btn_relatorio)
        self.layout.add_widget(btn_alerta)

        return self.layout

    def tela_cadastro(self, instance):
        self.layout.clear_widgets()
        self.nome_input = TextInput(hint_text="Nome do produto")
        self.qtd_input = TextInput(hint_text="Quantidade", input_filter="int")
        self.validade_input = TextInput(hint_text="Validade (dd/mm/aaaa)")
        self.cat_input = TextInput(hint_text="Categoria (Estocável ou Congelado)")

        salvar_btn = Button(text="Salvar")
        salvar_btn.bind(on_press=self.salvar_produto)
        voltar_btn = Button(text="Voltar")
        voltar_btn.bind(on_press=self.voltar_menu)

        self.layout.add_widget(Label(text="Cadastro de Produto"))
        self.layout.add_widget(self.nome_input)
        self.layout.add_widget(self.qtd_input)
        self.layout.add_widget(self.validade_input)
        self.layout.add_widget(self.cat_input)
        self.layout.add_widget(salvar_btn)
        self.layout.add_widget(voltar_btn)

    def salvar_produto(self, instance):
        nome = self.nome_input.text
        qtd = int(self.qtd_input.text) if self.qtd_input.text.isdigit() else 0
        validade = self.validade_input.text
        categoria = self.cat_input.text if self.cat_input.text in CATEGORIAS else "Estocável"

        if qtd < 0 or not validar_data(validade):
            self.layout.add_widget(Label(text="❌ Dados inválidos!"))
            return

        produto = {"nome": nome, "categoria": categoria, "quantidade": qtd, "validade": validade}
        estoque.append(produto)
        salvar_estoque()
        self.layout.add_widget(Label(text=f"✅ Produto '{nome}' cadastrado!"))

    def tela_listagem(self, instance):
        self.layout.clear_widgets()
        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        for produto in estoque:
            box.add_widget(Label(text=f"{produto['nome']} | {produto['categoria']} | Qtd: {produto['quantidade']} | Validade: {produto['validade']}"))

        scroll.add_widget(box)
        voltar_btn = Button(text="Voltar")
        voltar_btn.bind(on_press=self.voltar_menu)
        self.layout.add_widget(scroll)
        self.layout.add_widget(voltar_btn)

    def tela_relatorio(self, instance):
        self.layout.clear_widgets()
        btn_estocavel = Button(text="Relatório Estocáveis")
        btn_congelado = Button(text="Relatório Congelados")
        voltar_btn = Button(text="Voltar")

        btn_estocavel.bind(on_press=lambda x: self.mostrar_relatorio("Estocável"))
        btn_congelado.bind(on_press=lambda x: self.mostrar_relatorio("Congelado"))
        voltar_btn.bind(on_press=self.voltar_menu)

        self.layout.add_widget(btn_estocavel)
        self.layout.add_widget(btn_congelado)
        self.layout.add_widget(voltar_btn)

    def mostrar_relatorio(self, categoria):
        self.layout.clear_widgets()
        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        for produto in estoque:
            if produto['categoria'] == categoria:
                box.add_widget(Label(text=f"{produto['nome']} | Qtd: {produto['quantidade']} | Validade: {produto['validade']}"))

        scroll.add_widget(box)
        voltar_btn = Button(text="Voltar")
        voltar_btn.bind(on_press=self.voltar_menu)
        self.layout.add_widget(scroll)
        self.layout.add_widget(voltar_btn)

    def tela_alertas(self, instance):
        self.layout.clear_widgets()
        hoje = datetime.datetime.today()
        box = BoxLayout(orientation='vertical')

        for produto in estoque:
            if produto['quantidade'] < 5:
                box.add_widget(Label(text=f"⚠️ Estoque baixo: {produto['nome']}"))
            try:
                validade = datetime.datetime.strptime(produto['validade'], "%d/%m/%Y")
                dias_restantes = (validade - hoje).days
                if dias_restantes <= 5:
                    status = "VENCIDO" if dias_restantes < 0 else f"vence em {dias_restantes} dias"
                    box.add_widget(Label(text=f"⚠️ Validade: {produto['nome']} ({status})"))
            except ValueError:
                box.add_widget(Label(text=f"❌ Data inválida para {produto['nome']}"))

        voltar_btn = Button(text="Voltar")
        voltar_btn.bind(on_press=self.voltar_menu)
        self.layout.add_widget(box)
        self.layout.add_widget(voltar_btn)

    def voltar_menu(self, instance):
        self.layout.clear_widgets()
        self.build()

if __name__ == "__main__":
    EstoqueApp().run()
