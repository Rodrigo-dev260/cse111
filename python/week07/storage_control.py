import datetime
import csv

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

def escolher_categoria():
    print("\nCategorias disponíveis:")
    for i, cat in enumerate(CATEGORIAS, start=1):
        print(f"{i}. {cat}")
    escolha = input("Escolha a categoria (número): ")
    if escolha.isdigit() and 1 <= int(escolha) <= len(CATEGORIAS):
        return CATEGORIAS[int(escolha)-1]
    else:
        print("❌ Categoria inválida. Usando 'Estocável' por padrão.")
        return "Estocável"

def cadastrar_produto():
    nome = input('Nome do produto: ')
    categoria = escolher_categoria()
    quantidade = int(input('Quantidade: '))
    validade = input('Data de validade (dd/mm/aaaa): ')

    if quantidade < 0:
        print("❌ Quantidade inválida. Deve ser positiva.")
        return
    if not validar_data(validade):
        print("❌ Data inválida. Use o formato dd/mm/aaaa.")
        return

    produto = {
        'nome': nome,
        'categoria': categoria,
        'quantidade': quantidade,
        'validade': validade
    }

    estoque.append(produto)
    salvar_estoque()
    print(f"\n✅ Produto '{nome}' cadastrado na categoria '{categoria}' com sucesso!\n")

def listar_estoque():
    if not estoque:
        print('\n⚠️ Nenhum produto cadastrado.\n')
        return

    print('\n📦 Relatório completo:')
    for i, produto in enumerate(estoque, start=1):
        print(f"{i}. {produto['nome']} | Categoria: {produto['categoria']} | "
              f"Qtd: {produto['quantidade']} | Validade: {produto['validade']}")
    print()

def registrar_entrada():
    listar_estoque()
    indice  = int(input('Digite o número do produto para entrada: ')) -1
    if 0 <= indice < len(estoque):
        qtd = int(input('Quantidade a adicionar: '))
        if qtd > 0:
            estoque[indice]['quantidade'] += qtd
            salvar_estoque()
            print(f"\n✅ Entrada registrada! Novo estoque de {estoque[indice]['nome']}: {estoque[indice]['quantidade']}\n")
        else:
            print("❌ Quantidade inválida.")
    else:
        print('\n❌ Produto inválido')

def registrar_saida():
    listar_estoque()
    indice = int(input('Digite o número do produto para saída: ')) - 1
    if 0 <= indice < len(estoque):
        qtd = int(input('Quantidade a retirar: '))
        if 0 < qtd <= estoque[indice]['quantidade']:
            estoque[indice]['quantidade'] -= qtd
            salvar_estoque()
            print(f"\n✅ Saída registrada! Novo estoque de {estoque[indice]['nome']}: {estoque[indice]['quantidade']}\n")
        else:
            print('\n❌ Quantidade inválida ou insuficiente.\n')
    else:
        print('\n❌ Produto inválido.\n')

def verificar_alerta():
    hoje = datetime.datetime.today()
    print('\n🚨 Alertas de estoque:')
    alerta_existente = False

    for produto in estoque:
        if produto['quantidade'] < 5:
            print(f"⚠️ Estoque baixo: {produto['nome']} (Qtd: {produto['quantidade']})")
            alerta_existente = True

        try:
            validade = datetime.datetime.strptime(produto['validade'], "%d/%m/%Y")
            dias_restantes = (validade - hoje).days
            if dias_restantes <= 5:
                status = "VENCIDO" if dias_restantes < 0 else f"vence em {dias_restantes} dias"
                print(f"⚠️ Validade próxima: {produto['nome']} ({status})")
                alerta_existente = True
        except ValueError:
            print(f"❌ Data inválida para {produto['nome']}")

    if not alerta_existente:
        print('✅ Nenhum alerta no momento.\n')

def relatorio_por_categoria():
    print("\nCategorias disponíveis para relatório:")
    for i, cat in enumerate(CATEGORIAS, start=1):
        print(f"{i}. {cat}")
    escolha = input("Escolha a categoria (número): ")

    if escolha.isdigit() and 1 <= int(escolha) <= len(CATEGORIAS):
        categoria_escolhida = CATEGORIAS[int(escolha)-1]
        print(f"\n📊 Relatório de produtos da categoria: {categoria_escolhida}")
        print('-'*48)
        encontrado = False
        for produto in estoque:
            if produto['categoria'] == categoria_escolhida:
                print(f"- {produto['nome']} | Qtd: {produto['quantidade']} | Validade: {produto['validade']}")
                encontrado = True
        if not encontrado:
            print(f"⚠️ Nenhum produto da categoria '{categoria_escolhida}' cadastrado.\n")
    else:
        print("❌ Categoria inválida.\n")

def menu():
    carregar_estoque()
    opcoes = {
        "1": cadastrar_produto,
        "2": listar_estoque,
        "3": verificar_alerta,
        "4": registrar_entrada,
        "5": registrar_saida,
        "6": relatorio_por_categoria
    }

    while True:
        print('-'*38)
        print('=== Sistema de Controle de Estoque ===')
        print('-'*38)
        print('1. Cadastrar produto')
        print('2. Relatório completo')
        print('3. Verificar alertas')
        print('4. Registrar entrada')
        print('5. Registrar saída')
        print('6. Relatório por categoria (Estocável ou Congelado)')
        print('7. Sair')

        opcao = input('Escolha uma opção: ')
        if opcao == "7":
            print('\nEncerrando o sistema. Até logo!')
            break
        elif opcao in opcoes:
            opcoes[opcao]()
        else:
            print('\n❌ Opção inválida. Tente novamente.')

if __name__ == '__main__':
    menu()
