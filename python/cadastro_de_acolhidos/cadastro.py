import json
import mimetypes
import os
import sqlite3
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def exibir_ficha_formatada(p):
    # Cria uma tabela bonita para os dados pessoais
    table = Table(
        title=f"Ficha Nº: {p['numero_ficha']} - {p['nome']}",
        show_header=False,
        header_style="bold magenta",
    )
    table.add_column("Campo", style="cyan")
    table.add_column("Valor", style="white")

    table.add_row("Documento", str(p["documento"]))
    table.add_row("Data de Nasc.", str(p["data_nascimento"]))
    table.add_row("Mãe", str(p["mae"]))
    table.add_row("Endereço", f"{p['endereco']} - {p['cidade']}")

    console.print(Panel(table, title="[bold green]CADASTRO DO ACOLHIDO[/bold green]"))

# 1. Carrega as variáveis do arquivo .env para o ambiente Python
load_dotenv()

# 2. O SDK do Gemini lê automaticamente a chave da variável GEMINI_API_KEY do .env
client = genai.Client()

# ----------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA IA E BANCO DE DADOS
# ----------------------------------------------------------------------
DB_NAME = "albergue_municipal.db"


def inicializar_banco():
    """Cria o banco de dados e as tabelas baseadas na ficha impressa."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabela de dados cadastrais fixos da pessoa
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_ficha TEXT,
        nome TEXT NOT NULL,
        estado_civil TEXT,
        data_nascimento TEXT,
        cor TEXT,
        sexo TEXT,
        religiao TEXT,
        pai TEXT,
        mae TEXT,
        endereco TEXT,
        cidade TEXT,
        documento TEXT,
        naturalidade TEXT,
        escolaridade TEXT,
        observacoes_gerais TEXT
    )
    """)

    # Tabela de histórico de entradas/passagens
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_estadias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pessoa_id INTEGER,
        data_entrada TEXT,
        encaminhamento TEXT,
        horario TEXT,
        rotatividade TEXT,
        motivo_obs TEXT,
        data_saida TEXT,
        FOREIGN KEY(pessoa_id) REFERENCES pessoas(id)
    )
    """)

    conn.commit()
    conn.close()


def salvar_pessoa_no_banco(dados):
    """Insere os dados cadastrais e as passagens no banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO pessoas (
            numero_ficha, nome, estado_civil, data_nascimento, cor, sexo,
            religiao, pai, mae, endereco, cidade, documento, naturalidade,
            escolaridade, observacoes_gerais
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            dados.get("numero_ficha"),
            dados.get("nome"),
            dados.get("estado_civil"),
            dados.get("data_nascimento"),
            dados.get("cor"),
            dados.get("sexo"),
            dados.get("religiao"),
            dados.get("pai"),
            dados.get("mae"),
            dados.get("endereco"),
            dados.get("cidade"),
            dados.get("documento"),
            dados.get("naturalidade"),
            dados.get("escolaridade"),
            dados.get("observacoes_gerais"),
        ),
    )

    pessoa_id = cursor.lastrowid

    # Se a ficha extraída contiver registros de histórico/estadias
    if "historico_estadias" in dados and isinstance(
        dados["historico_estadias"], list
    ):
        for e in dados["historico_estadias"]:
            cursor.execute(
                """
                INSERT INTO historico_estadias (
                    pessoa_id, data_entrada, encaminhamento, horario, rotatividade, motivo_obs, data_saida
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    pessoa_id,
                    e.get("data_entrada"),
                    e.get("encaminhamento"),
                    e.get("horario"),
                    e.get("rotatividade"),
                    e.get("motivo_obs"),
                    e.get("data_saida"),
                ),
            )

    conn.commit()
    conn.close()
    return pessoa_id


# ----------------------------------------------------------------------
# 2. PROCESSAMENTO AUTOMÁTICO DE FICHA COM IA (OCR/Visão)
# ----------------------------------------------------------------------
def extrair_dados_com_ia(caminho_imagem, tentativas_max=5):
    """Lê a imagem da ficha manuscrita e extrai os campos estruturados em JSON."""
    if not os.path.exists(caminho_imagem):
        print(f"Erro: Arquivo '{caminho_imagem}' não encontrado.")
        return None

    # Detecta o tipo da imagem automaticamente
    mime_type, _ = mimetypes.guess_type(caminho_imagem)
    if not mime_type:
        mime_type = "image/jpeg"

    # Lista de modelos alternativos em ordem de preferência
    modelos = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"]

    try:
        with open(caminho_imagem, "rb") as f:
            imagem_bytes = f.read()

        prompt = """
        Analise a imagem desta ficha manuscrita do Albergue Municipal e extraia as informações no seguinte formato JSON estrito:
        {
            "numero_ficha": "texto ou null",
            "nome": "texto ou null",
            "estado_civil": "texto ou null",
            "data_nascimento": "texto ou null",
            "cor": "texto ou null",
            "sexo": "texto ou null",
            "religiao": "texto ou null",
            "pai": "texto ou null",
            "mae": "texto ou null",
            "endereco": "texto ou null",
            "cidade": "texto ou null",
            "documento": "texto ou null",
            "naturalidade": "texto ou null",
            "escolaridade": "texto ou null",
            "observacoes_gerais": "texto ou null",
            "historico_estadias": [
                {
                    "data_entrada": "texto ou null",
                    "encaminhamento": "texto ou null",
                    "horario": "texto ou null",
                    "rotatividade": "texto ou null",
                    "motivo_obs": "texto ou null",
                    "data_saida": "texto ou null"
                }
            ]
        }
        """

        for tentativa in range(1, tentativas_max + 1):
            modelo_atual = modelos[(tentativa - 1) % len(modelos)]
            try:
                chat = client.chats.create(
                    model=modelo_atual,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    ),
                )

                response = chat.send_message([
                    types.Part.from_bytes(
                        data=imagem_bytes, mime_type=mime_type
                    ),
                    prompt,
                ])

                texto_resposta = response.text.strip()

                if texto_resposta.startswith("```"):
                    texto_resposta = texto_resposta.strip("`")
                    if texto_resposta.startswith("json"):
                        texto_resposta = texto_resposta[4:].strip()

                return json.loads(texto_resposta)

            except Exception as e:
                espera = tentativa * 3
                if ("503" in str(e) or "404" in str(e)) and tentativa < tentativas_max:
                    print(
                        f"Instabilidade com modelo '{modelo_atual}'. Alternando modelo em {espera}s (Tentativa {tentativa}/{tentativas_max})..."
                    )
                    time.sleep(espera)
                else:
                    raise e

    except Exception as e:
        print(f"Erro ao processar imagem com a API: {e}")
        return None


def cadastrar_via_foto():
    """Captura a imagem da ficha, extrai os dados, permite validação e salva no banco."""
    print("\n--- CADASTRO AUTOMÁTICO VIA FOTO ---")
    caminho_imagem = (
        input("Digite o caminho ou nome do arquivo de imagem (ex: ficha.jpg): ")
        .strip()
    )

    print("\nLendo ficha e extraindo dados com IA... Aguarde.")
    dados = extrair_dados_com_ia(caminho_imagem)

    if not dados:
        print("Não foi possível extrair dados da imagem.")
        return

    print("\n" + "=" * 50)
    print(" DADOS EXTRAÍDOS DA FICHA")
    print("=" * 50)
    for chave, valor in dados.items():
        if chave != "historico_estadias":
            print(f"{chave.replace('_', ' ').capitalize()}: {valor}")

    if dados.get("historico_estadias"):
        print("\nPassagens identificadas:")
        for idx, h in enumerate(dados["historico_estadias"], 1):
            print(
                f"  {idx}. Entrada: {h.get('data_entrada')} | Encaminhamento:"
                f" {h.get('encaminhamento')} | Horário: {h.get('horario')}"
            )

    confirma = (
        input("\nOs dados estão corretos para salvar? (S/N): ").strip().upper()
    )
    if confirma == "S":
        salvar_pessoa_no_banco(dados)
        print("Ficha cadastrada com sucesso!")
    else:
        print("Operação cancelada. Faça o cadastro manual se preferir.")


def pessoa_ja_cadastrada(documento):
    """Verifica se o documento já existe no banco antes de salvar."""
    if not documento:
        return False
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM pessoas WHERE documento = ?", (documento,))
    existe = cursor.fetchone()
    conn.close()
    return existe is not None


# ----------------------------------------------------------------------
# 3. CADASTRO MANUAL E CONSULTAS
# ----------------------------------------------------------------------
def cadastrar_pessoa_manual():
    """Formulário manual para digitação completa da ficha."""
    print("\n--- NOVO CADASTRO MANUAL ---")
    dados = {
        "numero_ficha": input("Nº da Ficha: ").strip(),
        "nome": input("Nome completo: ").strip(),
        "estado_civil": input("Estado Civil: ").strip(),
        "data_nascimento": input("Data de Nasc. (DD/MM/AAAA): ").strip(),
        "cor": input("Cor/Raça: ").strip(),
        "sexo": input("Sexo: ").strip(),
        "religiao": input("Religião: ").strip(),
        "pai": input("Nome do Pai: ").strip(),
        "mae": input("Nome da Mãe: ").strip(),
        "endereco": input("Endereço: ").strip(),
        "cidade": input("Cidade: ").strip(),
        "documento": input("Documentação (RG/CPF/RNE): ").strip(),
        "naturalidade": input("Naturalidade: ").strip(),
        "escolaridade": input("Escolaridade: ").strip(),
        "observacoes_gerais": input("Observações Gerais: ").strip(),
        "historico_estadias": [],
    }

    salvar_pessoa_no_banco(dados)
    print(f"\nCadastro de '{dados['nome']}' realizado com sucesso!")


def registrar_nova_entrada():
    """Registra uma nova passagem/estadia permitindo buscar por nome ou documento."""
    termo = input(
        "\nDigite o NOME ou DOCUMENTO para registrar nova entrada: "
    ).strip()

    if not termo:
        print("Entrada inválida.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, numero_ficha, nome, documento FROM pessoas WHERE nome LIKE ? OR documento LIKE ?",
        (f"%{termo}%", f"%{termo}%"),
    )
    resultados = cursor.fetchall()

    if not resultados:
        print("Nenhum cadastro encontrado.")
        conn.close()
        return

    print("\nPessoas encontradas:")
    for p in resultados:
        print(f"ID: {p[0]} | Ficha Nº: {p[1]} | Nome: {p[2]} | Doc: {p[3]}")

    pessoa_id = input("\nDigite o ID da pessoa: ").strip()

    agora = datetime.now()
    data_padrao = agora.strftime("%d/%m/%Y")
    hora_padrao = agora.strftime("%H:%M")

    data_e = input(f"Data de Entrada [{data_padrao}]: ").strip() or data_padrao
    horario = input(f"Horário [{hora_padrao}]: ").strip() or hora_padrao
    encaminhamento = input("Encaminhamento: ").strip()
    rotatividade = input("Rotatividade (ex: 1ª vez): ").strip()
    motivo = input("Observação/Motivo: ").strip()

    cursor.execute(
        """
        INSERT INTO historico_estadias (pessoa_id, data_entrada, horario, encaminhamento, rotatividade, motivo_obs)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (pessoa_id, data_e, horario, encaminhamento, rotatividade, motivo),
    )

    conn.commit()
    conn.close()
    print("\nNova entrada registrada com sucesso!")


def buscar_pessoa_por_nome():
    """Busca os dados e todo o histórico de entradas pelo nome."""
    termo = input("\nDigite o nome ou parte dele para pesquisar: ").strip()

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas WHERE nome LIKE ?", (f"%{termo}%",))
    pessoas = cursor.fetchall()

    if not pessoas:
        print("Nenhum cadastro encontrado.")
        conn.close()
        return

    for p in pessoas:
        print("\n" + "=" * 50)
        print(f"FICHA Nº: {p['numero_ficha']} | NOME: {p['nome']}")
        print("-" * 50)
        print(
            f"Data Nasc: {p['data_nascimento']} | Cor: {p['cor']} | Sexo:"
            f" {p['sexo']} | Estado Civil: {p['estado_civil']}"
        )
        print(
            f"Documento: {p['documento']} | Naturalidade: {p['naturalidade']} |"
            f" Escolaridade: {p['escolaridade']}"
        )
        print(f"Pai: {p['pai']} | Mãe: {p['mae']}")
        print(f"Endereço: {p['endereco']} | Cidade: {p['cidade']}")
        print(f"Obs Gerais: {p['observacoes_gerais']}")

        cursor.execute(
            """
            SELECT data_entrada, horario, encaminhamento, rotatividade, motivo_obs, data_saida 
            FROM historico_estadias WHERE pessoa_id = ?
            """,
            (p["id"],),
        )
        estadias = cursor.fetchall()

        if estadias:
            print("\n  --- HISTÓRICO DE PASSAGENS ---")
            for e in estadias:
                saida_str = e["data_saida"] if e["data_saida"] else "Em aberto"
                print(
                    f"  Entrada: {e['data_entrada']} às {e['horario']} | Encaminhado por:"
                    f" {e['encaminhamento']} | Rotatividade: {e['rotatividade']}"
                )
                print(f"  Motivo/Obs: {e['motivo_obs']} | Saída: {saida_str}")
                print("  " + "-" * 40)
        else:
            print("\n  [Nenhum histórico de passagem registrado]")

    conn.close()


def buscar_pessoa_por_documento():
    """Busca um acolhido e todo o seu histórico pelo número do documento (RG, CPF, etc)."""
    documento_informado = input(
        "\nDigite o número do documento para pesquisar (RG/CPF): "
    ).strip()

    if not documento_informado:
        print("Documento inválido.")
        return

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM pessoas WHERE documento LIKE ?",
        (f"%{documento_informado}%",),
    )
    pessoas = cursor.fetchall()

    if not pessoas:
        print("\nNenhum cadastro encontrado com este documento.")
        conn.close()
        return

    for p in pessoas:
        print("\n" + "=" * 50)
        print(f"FICHA Nº: {p['numero_ficha']} | NOME: {p['nome']}")
        print("-" * 50)
        print(
            f"Documento: {p['documento']} | Data Nasc: {p['data_nascimento']} |"
            f" Sexo: {p['sexo']}"
        )
        print(f"Mãe: {p['mae']} | Pai: {p['pai']}")
        print(f"Endereço: {p['endereco']} | Cidade: {p['cidade']}")
        print(f"Obs Gerais: {p['observacoes_gerais']}")

        cursor.execute(
            """
            SELECT data_entrada, horario, encaminhamento, rotatividade, motivo_obs, data_saida 
            FROM historico_estadias WHERE pessoa_id = ?
            """,
            (p["id"],),
        )
        estadias = cursor.fetchall()

        if estadias:
            print("\n  --- HISTÓRICO DE PASSAGENS ---")
            for e in estadias:
                saida_str = e["data_saida"] if e["data_saida"] else "Em aberto"
                print(
                    f"  Entrada: {e['data_entrada']} às {e['horario']} | Encaminhado por: {e['encaminhamento']}"
                )
                print(f"  Motivo/Obs: {e['motivo_obs']} | Saída: {saida_str}")
                print("  " + "-" * 40)
        else:
            print("\n  [Nenhum histórico de passagem registrado]")

    conn.close()


# ----------------------------------------------------------------------
# 4. MENU PRINCIPAL
# ----------------------------------------------------------------------
def menu():
    inicializar_banco()

    while True:
        print("\n==============================================")
        print("   SISTEMA ALBERGUE MUNICIPAL - GESTÃO FICHA  ")
        print("==============================================")
        print("1. Buscar Cadastro por Nome")
        print("2. Buscar Cadastro por Documento (Evita Homônimos)")
        print("3. Registrar Nova Entrada/Passagem")
        print("4. Digitalizar Ficha Automática (via Foto)")
        print("5. Novo Cadastro Manual")
        print("6. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            buscar_pessoa_por_nome()
        elif opcao == "2":
            buscar_pessoa_por_documento()
        elif opcao == "3":
            registrar_nova_entrada()
        elif opcao == "4":
            cadastrar_via_foto()
        elif opcao == "5":
            cadastrar_pessoa_manual()
        elif opcao == "6":
            print("\nEncerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()