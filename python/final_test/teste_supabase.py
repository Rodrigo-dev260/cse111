
import psycopg
from getpass import getpass

HOST = "aws-1-sa-east-1.pooler.supabase.com"
PORTA = 5432
BANCO = "postgres"
USUARIO = "postgres.wtpdtwsplwhataxxpmlq"

print("TESTE DE CONEXÃO COM SUPABASE")
print("-" * 35)

senha = getpass("Digite a senha do banco Supabase: ")

try:
    with psycopg.connect(
        host=HOST,
        port=PORTA,
        dbname=BANCO,
        user=USUARIO,
        password=senha,
        sslmode="require",
        connect_timeout=10
    ) as conexao:

        print("\nConexão com Supabase realizada com sucesso!")

        with conexao.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name IN ('produtos', 'movimentacoes')
                ORDER BY table_name
            """)

            tabelas = cursor.fetchall()

            print("\nTabelas encontradas:")

            for tabela in tabelas:
                print("-", tabela[0])

except psycopg.Error as erro:
    print("\nErro ao conectar com Supabase.")
    print("Tipo de erro:", type(erro).__name__)
    print("Confira a senha, a conexão com a internet e os parâmetros.")
